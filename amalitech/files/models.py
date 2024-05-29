from django.db import models
from django.conf import settings


class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def download_count(self):
        return Download.objects.filter(file=self).count()

    def email_count(self):
        return EmailSent.objects.filter(file=self).count()
    


class Download(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.file.title}"
    
    def download_count(self):
        return Download.objects.filter(file=self).count()
    

class EmailSent(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email sent by {self.user.username} for {self.file.title}"