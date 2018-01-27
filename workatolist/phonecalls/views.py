from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from workatolist.phonecalls.models import Call
from workatolist.phonecalls.serializers import CallSerializer


class CallView(APIView):

    def post(self, request, format=None):
        try:
            if not request.data.get('call_id', None):
                raise ValidationError('The fields don\'t match with those expected')
            instance = Call.objects.get(id=request.data['call_id'])
        except ObjectDoesNotExist as e:
            instance = None
        try:
            serializer = CallSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
