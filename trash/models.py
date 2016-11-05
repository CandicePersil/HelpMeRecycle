from django.db import models
import uuid


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

    def __str__(self):
        return self.name


class TrashItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=2058)
    material = models.ForeignKey(TrashMaterial, default=None, on_delete=models.CASCADE)
    bin = models.ForeignKey(TrashBin, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
