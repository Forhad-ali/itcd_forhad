from django.urls import path
from . import views

app_name = 'camera_app'

urlpatterns = [
    path('', views.recent_image, name='recent_image'),

    # Gallery
    path('gallery/', views.image_list, name='image_list'),

    # API upload (used by OpenCV / script)
    path('api/upload/', views.upload_image, name='upload_api'),

    # Web form upload (NEW)
    path('upload/', views.upload_image_form, name='upload_form'),
]