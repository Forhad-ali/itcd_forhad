from django.urls import path
from . import views

urlpatterns = [

    # Facility
    path('facility/add/', views.facility_add, name='facility_add'),
    path('facility/list/', views.facility_list, name='facility_list'),
    path('facility/edit/<int:pk>/',views.facility_edit,name='facility_edit'),
    path('facility/delete/<int:pk>/',views.facility_delete,name='facility_delete'),

    # System
    path('system/add/', views.system_add, name='system_add'),
    path('system/list/', views.system_list, name='system_list'),

    # Room
    path('room/list/', views.room_list, name='room_list'),
    path('facility/<int:facility_id>/rooms/',views.facility_rooms,name='facility_rooms'),
    path('room/add/<int:facility_id>/',views.room_add,name='room_add'),
    path('room/edit/<int:pk>/',views.room_edit,name='room_edit'),
    path('room/delete/<int:pk>/',views.room_delete,name='room_delete'),

    path('facility/<int:fid>/systems/',views.facility_system_setup,name='facility_system_setup'),

    # Device
    path('device/add/<int:facility_id>/',views.device_add,name='device_add'),
    path('device/list/', views.device_list, name='device_list'),
    path('device/bulk/<int:facility_id>/',views.bulk_device_add,name='bulk_device_add'),
    path("facility/<int:facility_id>/devices/view/",views.device_view,name="device_view"),

    path('equipment/add/<int:system_id>/',views.equipment_add,name='equipment_add'),
    path('equipment/edit/<int:pk>/',views.equipment_edit,name='equipment_edit'),
    path('equipment/delete/<int:pk>/',views.equipment_delete,name='equipment_delete'),

]