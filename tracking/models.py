from django.db import models
from shorturl.models import ShortURL
from django.contrib.auth.models import User

class URLTracking(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    host = models.CharField(max_length=200)
    click_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click for {self.short_url.short_url} from {self.ip_address}"
