from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Asiakas

def asiakas_profiili(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		Asiakas.objects.create(
			user=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)