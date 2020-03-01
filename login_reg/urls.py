from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('success',views.success),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('logout/', views.logout),
]