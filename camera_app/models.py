from django.db import models

class CameraImage(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='captures/')
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp
    capture_date = models.DateField(null=True, blank=True)  # manual date (optional)

    def __str__(self):
        return f"{self.title} - {self.created_at}"