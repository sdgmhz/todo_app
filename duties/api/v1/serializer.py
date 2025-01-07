from rest_framework import serializers
from django.utils import timezone

from ...models import Duty

""" model serializer for Duty"""
class DutyModelSerializer(serializers.ModelSerializer):
    """ a read only filed to see if a not done duty is overdue or not"""
    deadline_status = serializers.SerializerMethodField()

    """ a read only field to get the url of duty instance"""
    absolute_url = serializers.SerializerMethodField()

    """ a field to show a summary of description in list page"""
    snippet = serializers.ReadOnlyField(source="get_snippet")

    class Meta:
        model = Duty
        fields = [
            'id',
            'author',
            'title',
            'snippet',
            'description',
            'absolute_url',
            'done_status',
            'deadline_date',
            'deadline_status',
            'created_date',
            'updated_date'
            ]
        

    """ method to determine a duty status which is overdue or not"""
    def get_deadline_status(self, duty):
        if duty.done_status != 'not':
            return 'Duty is done!'
        if duty.deadline_date > timezone.now().date():
            return 'Deadline has not expired yet!'
        return 'Deadline is over!'
    
    def get_absolute_url(self, duty):
        request = self.context.get('request')
        return request.build_absolute_uri(duty.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs'):
            rep.pop('snippet', None)
        else:
            rep.pop('description', None)
        return rep