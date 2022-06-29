from conf.settings_private import EMAIL_FROM
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Comment


@receiver(pre_save, sender=Comment)
def send_new_comment_email(sender, instance: Comment, **kwargs) -> None:
    if instance.id is None:
        send_mail(
            subject=f"Новый комментарий к посту",
            message=f"Новый комментарий к посту '{instance.post.title}':\n {instance.text}",
            from_email=EMAIL_FROM,
            recipient_list=[instance.post.author.user.email],
        )
    else:
        old_instance: Comment = Comment.objects.get(pk=instance.id)
        if old_instance.is_ack != instance.is_ack:
            send_mail(
                subject=f"Ваш комментарий принят",
                message=f"Ваш комментарий к посту '{instance.post.title}' принят.",
                from_email=EMAIL_FROM,
                recipient_list=[instance.author.user.email],
            )
