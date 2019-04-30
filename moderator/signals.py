from Ars.models import Option, Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from . import presentationViews
from asgiref.sync import async_to_sync
from aioredis.errors impot ConnectionClosedError


@receiver(post_save, sender= Comment)
def announce_comment_create(sender, instance, created, **kwargs):
    print("comment signal dispatched...\n")
    if created:
        channel_layer = get_channel_layer()
        topic = instance.topic
        presentation_name = topic.presentation_name
        not_sent = True
        if presentation_name is not None or presentation_name is not "null":
            while not_sent:
                try:
                    presentationViews.makeTopicpresentation(topic.id, name = presentation_name)
                    async_to_sync(channel_layer.group_send)(
                        f"moderator_{presentation_name}",{
                            "type":"moderator.announce",
                            "event": "comment created"
                        }
                    )
                except ConnectionClosedError:
                    print("redis error on comments","connection closed")
                else:
                    not_sent = False
    else:
        print("channel message not sent on comments........")

@receiver(post_save, sender= Option)
def announce_option_create(sender, instance, created, **kwargs):
    print("signal dispatched ...... \n")
    if instance:
        channel_layer = get_channel_layer()
        question = instance.question
        presentation_name = question.presentation_name
        not_sent = True
        if presentation_name is not None:
            while not_sent:
                try:
                    presentationViews.makeQuestionPresentation(question.id, name = presentation_name)
                    async_to_sync(channel_layer.group_send)(
                        f"moderator_{presentation_name}",{
                            "type":"moderator.announce",
                            "event": "Options Update"
                        }
                    )
                except ConnectionClosedError:
                    print("redis error on options","connection closed")
                else:
                    not_sent = False

    else:
        print("Channel message not sent on options::......")
