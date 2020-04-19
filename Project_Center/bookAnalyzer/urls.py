from django.urls import path
from . import views

app_name = 'bookAnalyzer'

urlpatterns = [
    path('', views.home,name='home'),
    path('bookPre',views.bookPre,name='bookPre'),
    path('bookDetails',views.bookDetails,name="bookDetails"),
    path('books/<int:books_pk>', views.viewBooks,name = 'viewBooks'),
    #path('books/<int:books_pk>/explore/', views.explore,name = 'explore'),
]
