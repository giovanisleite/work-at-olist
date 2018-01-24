from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from workatolist.phonecalls.models import Call
from workatolist.phonecalls.serializers import CallSerializer

class CallView(APIView):

    def post(self, request, format=None):
        try:
            instance = Call.objects.get(id=request.data['call_id'])
        except ObjectDoesNotExist as e:
            instance = None
        serializer = CallSerializer(instance=instance, data=request.data, transform_data=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
