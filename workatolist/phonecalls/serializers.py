from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from workatolist.phonecalls.models import Call


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
            real_data['source'] = data['source']
            real_data['destination'] = data['destination']
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
