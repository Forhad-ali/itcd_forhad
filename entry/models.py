from django.db import models

# Choices for type (used in Facility and EquipmentEntry)
TYPE_CHOICES = (
    ('Core', 'Core'),
    ('Terminal', 'Terminal'),
    ('Associate', 'Associate')
)

# ---------------------- Facility ----------------------
class Facility(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.code

# ---------------------- System ----------------------
class System(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.code

# ---------------------- Assignment Table ----------------------
class SystemFacilityAssignment(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('system', 'facility')  # Prevent duplicates

    def __str__(self):
        return f"{self.system.code} → {self.facility.code}"

# ---------------------- EquipmentEntry (Old Model) ----------------------
class EquipmentEntry(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=100)
    equipment_brand = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.system.code})"

# ---------------------- EquipmentDocument ----------------------
class EquipmentDocument(models.Model):
    equipment = models.ForeignKey(EquipmentEntry, on_delete=models.CASCADE, related_name='documents')
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------------------- SystemEquipmentQuantity (New Model) ----------------------
from django.db import models

class SystemEquipmentQuantity(models.Model):
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    facility = models.ForeignKey('Facility', on_delete=models.CASCADE, null=True, blank=True)  # allow null for migration
    equipment_name = models.CharField(max_length=255)
    equipment_entry = models.ForeignKey(EquipmentEntry, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    doc_reference_code = models.CharField(max_length=100, blank=True)
    doc_version = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('system', 'facility', 'equipment_name')

    def __str__(self):
        return f"{self.system.code} - {self.facility.code if self.facility else 'No Facility'} - {self.equipment_name}"


#MS Incoming Act
class MSIncoActEntry(models.Model):
    ms_id = models.CharField(max_length=100)
    incoming_act = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ms_id


# ---------------------- learning_category ----------------------
class Learning_Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class TopicsEntry(models.Model):
    learning_category = models.ForeignKey(Learning_Category, on_delete=models.CASCADE)
    topics = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topics


class LearningStep(models.Model):
    topics_entry = models.ForeignKey(TopicsEntry, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
