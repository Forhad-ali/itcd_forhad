from django.db import models

class Installation(models.Model):

    id = models.AutoField(primary_key=True)

    ms_id_full = models.CharField(max_length=255)
    ms_id = models.CharField(max_length=255)

    status = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    abd_number = models.CharField(max_length=100)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    system = models.CharField(max_length=255)
    facility = models.CharField(max_length=255)

    saw_program = models.CharField(max_length=255)

    unit = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)

    def __str__(self):
        return self.ms_id_full


class P4ID(models.Model):

    p4_id = models.CharField(max_length=255)

    ms_ids = models.ManyToManyField(
        Installation,
        related_name="p4_entries"
    ) 
    saw_programs = models.CharField(max_length=255)
    associate_ms = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.p4_id



class P8ID(models.Model):

    p8_id = models.CharField(max_length=255)

    p4_ids = models.ManyToManyField(
        P4ID,
        related_name="p8_entries"
    )

    p2_id = models.CharField(max_length=255)

    completed = models.BooleanField(default=False)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.p8_id




class P9ID(models.Model):

    p9_id = models.CharField(max_length=255)

    p8_ids = models.ManyToManyField(
        P8ID,
        related_name="p9_entries"
    )

    completed = models.BooleanField(default=False)

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.p9_id