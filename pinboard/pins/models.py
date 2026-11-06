from pathlib import Path

from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

IMAGE_EXT = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXT = {"mp4", "webm", "mov"}


class Pin(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pins")
    title = models.CharField("título", max_length=120)
    description = models.TextField("descripción", blank=True, max_length=1000)
    media = models.FileField(
        "archivo",
        upload_to="pins/%Y/%m/",
        validators=[FileExtensionValidator(sorted(IMAGE_EXT | VIDEO_EXT))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pin_detail", args=[self.pk])

    @property
    def is_video(self):
        return Path(self.media.name).suffix.lower().lstrip(".") in VIDEO_EXT

    def delete(self, *args, **kwargs):
        media = self.media
        super().delete(*args, **kwargs)
        media.delete(save=False)  # borra el archivo del disco


class Rating(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["pin", "user"], name="one_rating_per_user_per_pin")]

    def __str__(self):
        return f"{self.user} → {self.pin}: {self.stars}★"
