from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CameraImage

# API upload (with optional title & date)
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        title = request.POST.get('title', 'Untitled')
        capture_date = request.POST.get('capture_date')

        img = CameraImage.objects.create(
            image=request.FILES['file'],
            title=title,
            capture_date=capture_date if capture_date else None
        )
        return JsonResponse({'status': 'success', 'id': img.id})
    return JsonResponse({'status': 'failed'})


# ✅ Form Upload View (NEW)
def upload_image_form(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        capture_date = request.POST.get('capture_date')

        if image:
            CameraImage.objects.create(
                image=image,
                title=title,
                capture_date=capture_date if capture_date else None
            )
            return redirect('camera_app:image_list')

    return render(request, 'camera_app/upload.html')


# ✅ Show latest image
def recent_image(request):
    img = CameraImage.objects.order_by('-created_at').first()
    return render(request, 'camera_app/recent_image.html', {'image': img})


# ✅ Show all images
def image_list(request):
    images = CameraImage.objects.all().order_by('-created_at')
    return render(request, 'camera_app/image_list.html', {'images': images})