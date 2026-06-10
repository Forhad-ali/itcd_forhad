from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # INSTALLATION MAIN LIST
    # =========================
    path(
        '',
        views.installation_list,
        name='installation_list'
    ),

    # =========================
    # ADD NEW INSTALLATION
    # =========================
    path(
        'add/',
        views.add_installation,
        name='add_installation'
    ),

    # =========================
    # EDIT INSTALLATION
    # =========================
    path(
        'edit/<int:pk>/',
        views.edit_installation,
        name='edit_installation'
    ),

    # =========================
    # DELETE INSTALLATION
    # =========================
    path(
        'delete/<int:pk>/',
        views.delete_installation,
        name='delete_installation'
    ),

    # =========================
    # INLINE UPDATE (AJAX FIELD UPDATE)
    # =========================
    path(
        'update-entry/<int:pk>/',
        views.update_entry,
        name='update_entry'
    ),

    # =========================
    # F2 TB PAGE (SEARCH + FORM UI)
    # =========================
    path(
        'f2-tb/',
        views.f2_tb,
        name='f2_tb'
    ),

    # =========================
    # F2 TB SAVE (BULK UPDATE / CREATE)
    # =========================
    path(
        'f2-tb/save/',
        views.f2_tb_save,
        name='f2_tb_save'
    ),

    # =========================
    # OPTIONAL SEARCH API
    # =========================
    path(
        'f2-tb/search/',
        views.f2_tb_search,
        name='f2_tb_search'
    ),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("dashboard/filter/", views.dashboard_filter, name="dashboard_filter"),
    path('facility_dashboard/', views.facility_dashboard, name='facility_dashboard'),

    path('p4/add/', views.p4_create, name='p4_entry'),
    path('p4/list/', views.p4_list, name='p4_display_list'),
    path('search-ms/', views.search_ms, name='search_ms'),
    path('p4/edit/<int:id>/', views.p4_edit, name='p4_edit'),
    path('p4/delete/<int:id>/', views.p4_delete, name='p4_delete'),
    path('p4_facility_dashboard/',views.p4_facility_dashboard,name='p4_facility_dashboard'),

    path('p8/add/', views.p8_create, name='p8_entry'),
    path('p8/list/', views.p8_list, name='p8_display_list'),
    path('search-p4/', views.search_p4, name='search_p4'),
    path('p8/edit/<int:id>/', views.p8_edit, name='p8_edit'),
    path('p8/delete/<int:id>/', views.p8_delete, name='p8_delete'),
    path('p8_facility_dashboard/',views.p8_facility_dashboard,name='p8_facility_dashboard'),

    path('p9/add/', views.p9_create, name='p9_entry'),
    path('p9/list/', views.p9_list, name='p9_display_list'),
    path('search-p8/', views.search_p8, name='search_p8'),
    path('p9/edit/<int:id>/', views.p9_edit, name='p9_edit'),
    path('p9/delete/<int:id>/', views.p9_delete, name='p9_delete'),
    path('p9_facility_dashboard/',views.p9_facility_dashboard,name='p9_facility_dashboard'),

    path('facility_dashboard_all/', views.facility_dashboard_all, name='facility_dashboard_all'),
    path("p4/dashboard/", views.p4_dashboard, name="p4_dashboard"),
    path("p4/dashboard/filter/", views.p4_dashboard_filter, name="p4_dashboard_filter"),

    path("p8/dashboard/", views.p8_dashboard, name="p8_dashboard"),
    path("p8/dashboard/filter/", views.p8_dashboard_filter, name="p8_dashboard_filter"),

    path("p9/dashboard/", views.p9_dashboard, name="p9_dashboard"),
    path("p9/dashboard/filter/", views.p9_dashboard_filter, name="p9_dashboard_filter"),
]