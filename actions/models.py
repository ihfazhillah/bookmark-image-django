from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import datetime
from django.utils import timezone

# Create your models here.

class ActionManager(models.Manager):
    def create_action(self, user, verb, target=None):
        now = timezone.now()
        last_minute = now - datetime.timedelta(seconds=60)
        similiar_actions = self.get_queryset().filter(user_id=user.id,
                                                      verb=verb,
                                                      created__gte=last_minute)

        if target:
            target_ct = ContentType.objects.get_for_model(target)
            similiar_actions = similiar_actions.filter(target_ct=target_ct,
                                                       target_id=target.id)

        if not similiar_actions:
            action = self.model(user=user, verb=verb, target=target)
            action.save()
            return True
        return False

class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='actions',
                             db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  related_name='target_obj',
                                  blank=True,
                                  null=True)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)

    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    objects = ActionManager()

    class Meta:
        ordering = ('-created',)


