from datetime import datetime

from rest_framework import serializers

from workatolist.phonecalls.models import Call


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        exclude = ['price']
