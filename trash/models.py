from django.db import models
import uuid


class TrashGeoLoc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=2058)

    def __str__(self):
        return self.location


class TrashMaterial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=2058)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TrashBin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=2058)
    color = models.CharField(max_length=64)
    created_date = models.DateTimeField(auto_now_add=True)
    # optional foreign key for open data trashbin locations
    trash_loc = models.ForeignKey(TrashGeoLoc, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class TrashItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=2058)
    material = models.ForeignKey(TrashMaterial, default=None, on_delete=models.CASCADE)
    bin = models.ForeignKey(TrashBin, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    # scan code
    sc_code = models.CharField(max_length=2058, default=None)
    # optional image file for image recognition
    item_img = models.CharField(max_length=2058, default=None)

    def __str__(self):
        return self.name
