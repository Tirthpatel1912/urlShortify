from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone

class ClickLog(models.Model):
    short_url = models.ForeignKey('ShortURL', related_name='click_logs', on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)  # Record the time of the click

    def __str__(self):
        return f"Click on {self.short_url.slug} at {self.clicked_at}"

class ShortURL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(unique=True, null=False, default=False)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates when saved
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    click_count = models.PositiveIntegerField(default=0)  # Field to store the number of clicks

    def __str__(self):
        return self.slug

    def generate_qr_code(self):
        if not self.is_private:
            qr_img = qrcode.make(self.long_url)
            qr_io = BytesIO()
            qr_img.save(qr_io, format='PNG')
            qr_img_file = File(qr_io, name=f'{self.short_url}_qr.png')
            self.qr_code.save(qr_img_file.name, qr_img_file)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = str(uuid.uuid4())[:8]  # Generate unique short URL
        super().save(*args, **kwargs)
        if not self.qr_code and not self.is_private:
            self.generate_qr_code()

    def increment_click_count(self):
        """Increment the click count and log the click time."""
        self.click_count += 1
        self.save(update_fields=['click_count'])  # Save only the click_count field

        # Log the click
        ClickLog.objects.create(short_url=self)  # Create a new ClickLog entry
