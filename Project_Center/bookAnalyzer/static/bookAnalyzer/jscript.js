

$(document).ready(function (){

})
var arr=eval($("#words")[0].innerText)



var y=800
var pages = ((arr.length / y) >> 0)+1
$(".pages")[1].innerText=" of "+pages
$(".pages")[0].innerText = " "

$('[name=Prev]').on('click',function () {
  // TODO: get page number from elemet go to the page with the pager
})
$('[name=Next]').on('click',function () {
  // TODO: get page number from elemet go to the page with the pager
})

$("#pager").on('keypress',function(e) {
    if(e.which == 13) {

      pager($("#pager").val())


    }
});
function pager(page){
  var arr=eval($("#words")[0].innerText)
  text2=``
  var p=page*y
  for (i = (page-1)*y; i < p; i++) {
    if (page*y>arr.length) {
          p=arr.length
        }
        if (arr[i]===`\n`) {
          arr[i]=`<br>`
        }
    text2 += `

        <span class='bookWords'> `+arr[i]+` </span>

    `
  }
  text=`
    <div id="bookOutput">
      `+text2+`
      </div>
    `

  $(".console")[0].innerHTML =text
  $(".bookWords").on('click',function() {

          var data = {
            "csrfmiddlewaretoken" : csrf,
            "query":$(this)[0].innerText,
            "code":"definition",
          }

          $.post(url,data,function(response){
            if (response.hasOwnProperty("definition")){
              text=response["definition"];
              $(".output")[0].innerHTML=text;
            } else if (response.hasOwnProperty("matches")) {

              arr2=response["matches"];

              var z =""
              for (i = 0; i < arr2.length; i++) {

                z += `
                    <span class='bookWords2'> `+arr2[i]+` </span><br>
                `
              }



              $(".output")[0].innerHTML=z;
              $(".bookWords2").on('click',function() {

                      var data = {
                        "csrfmiddlewaretoken" : csrf,
                        "query":$(this)[0].innerText,
                        "code":"definition",
                      }

                      $.post(url,data,function(response){

                        text=response["definition"];
                        $(".output")[0].innerHTML=text;

                    })

              });
            }




        })

  });
}

/*$(".bookWords").on('click',function() {

        var data = {
          "csrfmiddlewaretoken" : csrf,
          "query":$(this)[0].innerText,
          "code":"definition",
        }

        $.post(url,data,function(response){

          text=response["definition"];
          $(".output")[0].innerHTML=text;

      })

});*/
$(".inp").on('keypress',function(e) {
    if(e.which == 13) {
        var data = {
          "csrfmiddlewaretoken" : csrf,
          "query":$(".inp")[0].value,
          "code":"context",
        }
        $.post(url,data,function(response){

          arr=response["context"];
          text2=``
          for (i = 0; i < arr.length; i++) {
            text2 += `
              <tr>
                <td class="contextWords"> `+arr[i]+` </td>
              </tr>
            `
          }
          text=`
            <table id = "Phrases">
              <tr>
              <th ><h6>Phrases in which the word occured.</h6></th>
              `+text2+`
            </tr>
            </table>
            `
          $(".output")[0].innerHTML=text;
          $(".console")[0].innerHTML = response["definition"]

          if (response.hasOwnProperty("matches")) {

            var matches = response["matches"]

            text=""
            for (var i = 0; i < matches.length; i++) {
              text += `<span class = "matches">`+matches[i]+`</span><br>`
            }
            $(".console")[0].innerHTML = text
            $(".matches").on("click", function(){

              var data = {
                "csrfmiddlewaretoken" : csrf,
                "query":$(this)[0].innerText,
                "code":"definition",
              }
              console.log(data)
              $.post(url,data,function(response){
                $(".console")[0].innerHTML = response["definition"]
              })
            })
          }
      })
    }
});
$('.inpFT').on('keypress',function(e) {
  length=$("[name='length']").innerText
  console.log(length)

    if(e.which == 13) {
      if (length!=="") {
        var data = {
          "csrfmiddlewaretoken" : csrf,
          "up":$(".inpFT")[0].value,
          'low':$(".inpFT")[1].value,
          "code":"explore",
          "length":length,
        }
      } else {
          var data = {
            "csrfmiddlewaretoken" : csrf,
            "up":$(".inpFT")[0].value,
            'low':$(".inpFT")[1].value,
            "code":"explore",
            "length":"",
        }
      }


        $.post(url,data,function(response){


          arr=response["Word"];
          arr2 = response['Freq'];
          text2=``


          for (i = 0; i < arr.length; i++) {
            text2 += `
              <tr>
                <td class = "Word"> `+arr[i]+` </td>
                <td>`+arr2[i]+`</td>
              </tr>
            `
          }
          text=`
            <table id = "WF">
              <tr>
              <th><h6>Word</h6></th>
              <th><h6>Frequency</h6></th>
              `+text2+`
            </tr>
            </table>
            `

          $(".output")[0].innerHTML=text;
          $(".Word").on('click',function() {

                  var data = {
                    "csrfmiddlewaretoken" : csrf,
                    "query":$(this)[0].innerText,
                    "code":"definition",
                  }

                  $.post(url,data,function(response){
                    if (response.hasOwnProperty("definition")){
                      text=response["definition"];
                      $(".console")[0].innerHTML=text;
                    } else if (response.hasOwnProperty("matches")) {

                        arr2=response["matches"];

                        var z =""
                        for (i = 0; i < arr2.length; i++) {

                          z += `

                              <span class="Word2"> `+arr2[i]+` </span>

                          `
                        }


                        $(".Word2").off()
                        $(".console")[0].innerHTML=z;
                        $(".Word2").on('click',function() {

                                var data = {
                                  "csrfmiddlewaretoken" : csrf,
                                  "query":$(this)[0].innerText,
                                  "code":"definition",
                                }

                                $.post(url,data,function(response){

                                  text=response["definition"];
                                  $(".console")[0].innerHTML=text;

                              })

                        });
                      }

                })
      })
    })
}
})
