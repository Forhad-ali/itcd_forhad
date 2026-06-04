from django.db import models


class Facility(models.Model):
    fid = models.AutoField(primary_key=True)
    facility = models.CharField(max_length=100, unique=True)
    facility_title = models.CharField(max_length=255)

    def __str__(self):
        return self.facility


class System(models.Model):
    sid = models.AutoField(primary_key=True)
    system_code = models.CharField(max_length=50, unique=True)
    system_title = models.CharField(max_length=255)

    def __str__(self):
        return self.system_code


class Room(models.Model):
    rmid = models.AutoField(primary_key=True)

    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name='rooms'
    )

    room_kks = models.CharField(max_length=100, unique=True)
    room_title = models.CharField(max_length=255)

    def __str__(self):
        return self.room_kks

class RoomWiseDevice(models.Model):
    rid = models.AutoField(primary_key=True)

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='devices'
    )

    system = models.ForeignKey(
        System,
        on_delete=models.PROTECT,
        related_name='devices'
    )

    device_kks = models.CharField(max_length=255)
    device_title = models.CharField(max_length=500)
    ms_id = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.device_kks


class Equipment(models.Model):

    eid = models.AutoField(primary_key=True)

    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name='equipments'
    )

    equipment_name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.equipment_name


class FacilitySystem(models.Model):

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE
    )

    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('facility', 'system')

    def __str__(self):
        return f"{self.facility} - {self.system}"