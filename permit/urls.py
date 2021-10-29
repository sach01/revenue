from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    #path('<int:pk>/', views.stall, name='stall'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
   # path('<int:question_id>/', views.detail, name='detail'),
]