from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .signals import user_logged_in
from .utils import get_client_ip

User = get_user_model()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=120,)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        try:
            Session.objects.get(pk=self.session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_reciever(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(
            user=instance.user).exclude(id=instance.id)
        for i in qs:
            i.end_session()

    if not instance.active and not instance.ended:
        instance.end_session()


post_save.connect(post_save_session_reciever, sender=UserSession)


def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user, ip_address=ip_address, session_key=session_key)


user_logged_in.connect(user_logged_in_reciever)
