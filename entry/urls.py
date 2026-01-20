# entry/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Facility Section
    path('add_facility/', views.add_facility, name='add_facility'),
    path('facility_grid/', views.facility_grid, name='facility_grid'),
    path('facilities/', views.facility_list, name='facility_list'),
    path('facilities/<int:facility_id>/systems/', views.systems_by_facility, name='systems_by_facility'),
    path('facilities/<int:facility_id>/add-system/', views.add_system_to_facility, name='add_system_to_facility'),

    # System Section
    path('add_system', views.add_system, name='add_system'),  # Home - Add System
    path('', views.system_grid, name='system_grid'),

    # Equipment Section
    path('equipment-entry/<int:system_id>/', views.equipment_entry, name='equipment_entry'),
    path('equipment/<int:equipment_id>/', views.equipment_detail_view, name='equipment_detail'),
    path('equipment/<int:equipment_id>/', views.equipment_detail_view, name='equipment_detail_view'),
    path('equipment/<int:pk>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<int:pk>/delete/', views.delete_equipment, name='delete_equipment'),
    path('equipment/<int:pk>/detail/edit/', views.edit_equipment_detail, name='edit_equipment_detail'),
    path('facility/<int:facility_id>/assign-systems/', views.assign_systems_to_facility, name='assign_systems_to_facility'),
    path('system/<int:system_id>/facility/<int:facility_id>/equipments/', views.system_equipment_quantity_view, name='system_equipment_quantity'),
    path('export/facility-equipment-report/', views.export_facility_equipment_report, name='export_facility_equipment_report'),
    path('report/facility-equipment/', views.facility_equipment_report_view, name='facility_equipment_report'),
    path('report/export-pdf/', views.export_equipment_pdf, name='export_equipment_pdf'),
    
    path('ms-inco-act/', views.ms_inco_act_entry_view, name='ms_inco_act_entry'),
    path('ms-inco-act/add/', views.add_incoming_act_view, name='add_incoming_act'),
    
    
    # Learning Category Section
    path('learning_category_add', views.learning_category_add, name='learning_category_add'),  # Home - Add System
    path('learning_category_display', views.learning_category_display, name='learning_category_display'),
    path('topics-entry/<int:learning_category_id>/', views.topics_entry, name='topics_entry'),
    path('topics/<int:pk>/edit/', views.edit_topics, name='edit_topics'),
    path('topics/<int:pk>/delete/', views.delete_topics, name='delete_topics'),
    path('topics/<int:topic_id>/steps/', views.learning_steps_view, name='learning_steps_view'),
    path('learning-steps/delete/<int:step_id>/', views.delete_step, name='delete_step'),
    path('learning-steps/edit/<int:step_id>/', views.edit_step, name='edit_step'),

]


