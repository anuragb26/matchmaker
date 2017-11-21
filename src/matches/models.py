import datetime
from decimal import Decimal
from django.db import models
from django.conf import settings
from .utils import get_match
from django.utils import timezone



class MatchQuerySet(models.query.QuerySet):
	def matches(self,user):
		q1 = self.filter(user_a=user)
		q2 = self.filter(user_b=user)
		return (q1 | q2).distinct()



# Create your models here.
class MatchManager(models.Manager):
	
	def get_queryset(self):
		return MatchQuerySet(self.model,using=self._db)

	def get_or_create_match(self,user_a=None,user_b=None):
		print "inside"
		try:
			obj1 = self.get(user_a=user_a,user_b=user_b)
		except:
			obj1 = None
		try:
			obj2 = self.get(user_a=user_b,user_b=user_a)
		except:
			obj2 = None
		
		if obj1 and not obj2:
			obj1.check_update()
			return obj1,False
		if obj2 and not obj1:
			obj2.check_update()
			return obj2,False
		if not (obj1 and obj2):
			obj = self.create(user_a = user_a,user_b=user_b)
			obj.do_match()
			return obj,True
		else:
			return obj1,False
		# match_decimal,questions_answered = get_match(user_a=user_a,user_b=user_b)
		# #add match percentage
		# obj.match_decimal = match_decimal
		# obj.questions_answered = questions_answered
		# obj.save()

	def update_all(self):
		queryset = self.all()
		now = timezone.now()
		offset1 = now - datetime.timedelta(hours=12)
		offset2 = now - datetime.timedelta(hours=36)
		queryset.filter(updated__gt=offset2).filter(updated__lt=offset1)
		#print queryset
		if queryset.count() > 0:
			for i in queryset:
				i.check_update()

	def matches_all(self,user):
		return self.get_queryset().matches(user)


class Match(models.Model):
	user_a = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='match_user_a')
	user_b = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='match_user_b')
	match_decimal = models.DecimalField(decimal_places=8,max_digits=16,default=0.0)
	questions_answered = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)


	def do_match(self):
		user_a = self.user_a
		user_b = self.user_b
		match_decimal,questions_answered = get_match(user_a=user_a,user_b=user_b)
		self.match_decimal = match_decimal
		self.questions_answered = questions_answered
		self.save()

	@property
	def get_percent(self):
		new_decimal = self.match_decimal*Decimal(100)
		return "{0:4.2f}".format(new_decimal) + "%"
	


	def check_update(self):
		now = timezone.now()
		time_diff = datetime.timedelta(seconds=12)
		offset = now - time_diff
		if(self.updated <= offset):
			print "in update"
			self.do_match()
		else:
			print "already updated"


	def __unicode__(self):
		return "{0:4.2f}".format(self.match_decimal)

	objects = MatchManager()