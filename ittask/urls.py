from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("", views.login_view, name="login"),   # root -> login page
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("dashboard/", views.dashboard, name="dashboard"),   # redirect after login
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("viewer-dashboard/", views.viewer_dashboard, name="viewer_dashboard"),

    # Tickets
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/update/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/delete/", views.ticket_delete, name="ticket_delete"),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),


    # User Management (Admin only)
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:user_id>/update/", views.user_update, name="user_update"),
]
