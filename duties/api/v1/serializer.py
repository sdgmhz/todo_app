from rest_framework import serializers
from django.utils import timezone

from ...models import Duty

""" model serializer for Duty"""
class DutyModelSerializer(serializers.ModelSerializer):
    """ a read only filed to see if a not done duty is overdue or not"""
    deadline_status = serializers.SerializerMethodField()

    class Meta:
        model = Duty
        fields = [
            'id',
            'author',
            'title',
            'description',
            'done_status',
            'deadline_date',
            'deadline_status',
            'created_date',
            'updated_date'
            ]
        read_only_fields = ['deadline_status']

    """ method to determine a duty status which is overdue or not"""
    def get_deadline_status(self, duty):
        if duty.done_status != 'not':
            return 'Duty is done!'
        if duty.deadline_date > timezone.now().date():
            return 'Deadline has not expired yet!'
        return 'Deadline is over!'
