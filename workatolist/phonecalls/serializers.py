from datetime import datetime

from rest_framework import serializers

from workatolist.phonecalls.models import Call


class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        exclude = ['price']

    def __init__(self, *args, **kwargs):
        if kwargs.get('transform_data', None):
            data = kwargs.get('data')
            kwargs['data'] = self.transform_data(data)
            del kwargs['transform_data']
        super(CallSerializer, self).__init__(*args, **kwargs)

    def transform_data(self, data):
        if not self._validate_input(data):
            raise serializers.ValidationError(detail='The fields don\'t match with those expected')
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
    def _validate_input(data):
        if not data.get('type', None):
            return False

        start_keys = {'id', 'type', 'timestamp', 'source', 'destination', 'call_id'}
        end_keys = {'id', 'type', 'timestamp', 'call_id'}

        expected = {'start': start_keys, 'end': end_keys}
        data_keys = set(data.keys())

        return data_keys == expected[data['type']]
