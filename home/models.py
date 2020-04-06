from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=150)
    adress = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=150)
    fax = models.CharField(blank=True,max_length=150)
    email = models.CharField(blank=True,max_length=150)
    smtpserver = models.CharField(blank=True,max_length=150)
    smptemail = models.CharField(blank=True,max_length=150)
    smptpassword = models.CharField(blank=True,max_length=150)
    smptport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook   = models.CharField(blank=True,max_length=150)
    instagram = models.CharField(blank=True,max_length=150)
    twitter = models.CharField(blank=True,max_length=150)

    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)

    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title