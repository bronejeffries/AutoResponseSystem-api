from Ars.models import Option
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from . import presentationViews
from asgiref.sync import async_to_sync


@receiver(post_save, sender= Option)
def announce_option_create(sender, instance, created, **kwargs):
    print("signal dispatched ...... \n")
    if created:
        channel_layer = get_channel_layer()
        question = instance.question
        presentation_name = question.presentation_name
        if presentation_name is not None:
            try:
                presentationViews.makeQuestionPresentation(question.id, name = presentation_name)
                async_to_sync(channel_layer.group_send)(
                    "moderators",{
                        "type":"moderator.announce",
                        "event": "Options Update"
                    }
                )
            except ConnectionClosedError:
                print("redis error","connection closed")
