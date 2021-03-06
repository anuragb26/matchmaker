from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
User = settings.AUTH_USER_MODEL


def upload_location(instance,filename):
	location = str(instance.user.username)
	return "{}/{}".format(location,filename)


class Profile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=120,null=True,blank=True)
	picture = models.ImageField(upload_to=upload_location,null=True,blank=True)


	def __unicode__(self):
		return self.user.username

	def get_absolute_url(self):
		url = reverse("profile",kwargs={"username":self.user.username})
		#return "/profile/{0}".format(self.user.username)
		return url