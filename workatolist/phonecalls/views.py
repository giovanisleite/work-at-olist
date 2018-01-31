from datetime import datetime, timedelta

from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from workatolist.phonecalls.models import Call, Subscriber
from workatolist.phonecalls.serializers import CallSerializer, BillSerializer


class CallView(APIView):

    def post(self, request):
        try:
            if not request.data.get('call_id', None):
                raise ValidationError('The fields don\'t match with those expected')
            instance = Call.objects.get(id=request.data['call_id'])
        except ObjectDoesNotExist:
            instance = None
        try:
            serializer = CallSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)


class BillView(generics.RetrieveAPIView):
    serializer_class = BillSerializer
    lookup_field = 'phone'

    def get_queryset(self):
        last_month = datetime.today().replace(day=1) - timedelta(days=1)
        default_period = last_month.strftime("%m/%Y")
        period = self.request.query_params.get('period', default_period)
        month, year = period.split('/')

        related_queryset = Call.objects.filter(started_at__isnull=False,
                                               finished_at__month=month,
                                               finished_at__year=year)

        queryset = Subscriber.objects.prefetch_related(Prefetch('outgoing_calls',
                                                                queryset=related_queryset))

        return queryset
