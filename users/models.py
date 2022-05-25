import profile
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=500,blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    short_intro = models.CharField(max_length=200,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profile/default.png')
    github = models.CharField(max_length=200,blank=True,null=True)
    linkedin = models.CharField(max_length=200,blank=True,null=True)
    twitter = models.CharField(max_length=200,blank=True,null=True)
    portfolio = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.name)   


@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profiles = Profile.objects.create(
            user=user,
            email=user.email,
            name=user.first_name
        )
        subject = 'Welcome to Developers House'
        message = 'xD'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profiles.email],
            fail_silently=False
        )

@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,created,**kwargs):
    user = instance.user
    user.delete()

@receiver(post_save,sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# post_save.connect(profileUpdated,sender=Profile)
 
class Skill(models.Model):
    owner = models.ForeignKey(Profile,blank=True,on_delete=models.CASCADE,null=True)
    name =  models.CharField(max_length=200,blank=True,null=True)
    description = models.CharField(max_length=200,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)                      


class Messages(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    receiver = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name='messages')
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    is_read=models.BooleanField(default=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read','-created']    
