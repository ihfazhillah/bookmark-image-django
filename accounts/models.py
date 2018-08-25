from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(
            self.user.username)

    def get_absolute_url(self):
        return reverse('accounts:detail', args=[self.user.username])

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

    class Meta:
        ordering = ('-created',)

User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))


def profile_create_after_user_created(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(profile_create_after_user_created, sender=settings.AUTH_USER_MODEL)
