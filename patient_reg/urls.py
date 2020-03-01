from django.urls import path
from . import views

urlpatterns = [
     path('patient/', views.register),
     path('process_patient', views.process_patient),
     path('edit_patient/<int:myInt>', views.edit_patient),
     path('delete_patient', views.delete_patient),
     path('edit_template/<int:myInt>', views.edit_template),
     path('process_edit', views.process_edit),
     path('go_edit', views.go_edit),
]