from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from workatolist.phonecalls.models import Call, Subscriber


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        exclude = ['price']

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        kwargs['data'] = self.to_internal_values(data)
        super(CallSerializer, self).__init__(*args, **kwargs)

    def to_internal_values(self, data):
        self.validate_input(data)
        real_data = {'id': data['call_id']}
        if data['type'] == 'start':
            started_at = datetime.fromtimestamp(int(data['timestamp']))
            real_data['started_at'] = started_at.strftime('%Y-%m-%d %H:%M:%S')
            real_data['source'] = Subscriber.objects.get(phone=data['source']).id
            real_data['destination'] = Subscriber.objects.get(phone=data['destination']).id
        else:
            finished_at = datetime.fromtimestamp(int(data['timestamp']))
            real_data['finished_at'] = finished_at.strftime('%Y-%m-%d %H:%M:%S')
        return real_data

    @staticmethod
    def validate_input(data):
        start_keys = {'id', 'type', 'timestamp', 'source', 'destination', 'call_id'}
        end_keys = {'id', 'type', 'timestamp', 'call_id'}

        expected = {'start': start_keys, 'end': end_keys}
        data_keys = set(data.keys())

        if not data.get('type', False) or not data_keys == expected[data['type']]:
            raise ValidationError('The fields don\'t match with those expected')


class CallRecordSerializer(serializers.ModelSerializer):
    call_start_date = serializers.SerializerMethodField()
    call_start_time = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ['destination', 'call_start_date', 'call_start_time', 'duration', 'price']
        read_only_fields = fields

    def get_call_start_date(self, obj):
        return obj.started_at.date()

    def get_call_start_time(self, obj):
        return obj.started_at.time()


class BillSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    calls = CallRecordSerializer(source='outgoing_calls', many=True)

    class Meta:
        model = Subscriber
        fields = ['name', 'period', 'calls']
        read_only_fields = fields

    def get_period(self, obj):
        period = self.context['request'].query_params.get('period', None)
        if not period:
            last_month = datetime.today().replace(day=1) - timedelta(days=1)
            period = last_month.strftime("%m/%Y")
        self.validate_period(period)
        return period

    @staticmethod
    def validate_period(period):
        month, year = (int(p) for p in period.split('/'))
        now = datetime.now()
        if year > now.year or month >= now.month and year >= now.year:
            raise ValidationError('It\'s only possible to get a telephone bill after '
                                  'the reference month has ended')
