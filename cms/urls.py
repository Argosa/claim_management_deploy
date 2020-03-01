from django.urls import path
from . import views

urlpatterns = [
    path('claim_entry/', views.claim_entry),
    path('process_claim', views.process_claim),
    path('create_claim', views.create_claim),
    path('claim_dashboard/', views.claim_dashboard),
    path('view_claim/<int:myInt>', views.view_claim),
    path('process_action', views.process_action),
    path('view_action/<int:myInt>', views.view_action),
    path('change_follow' , views.change_follow),
    path('close_action', views.close_action),
    path('edit_claim/<int:myInt>', views.edit_claim),
    path('process_claim_edit', views.process_claim_edit),
    path('add_action_note', views.add_action_note),
    path('delete_claim', views.delete_claim),
    path('go_view_action', views.go_view_action),
]