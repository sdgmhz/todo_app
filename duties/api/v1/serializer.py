from rest_framework import serializers
from django.utils import timezone

from ...models import Duty
from accounts.models import Profile

""" model serializer for Duty """
class DutyModelSerializer(serializers.ModelSerializer):
    """ a read only filed to see if a not done duty is overdue or not """
    deadline_status = serializers.SerializerMethodField()

    """ a read only field to get the url of duty instance """
    absolute_url = serializers.SerializerMethodField()

    """ a field to show a summary of description in list page """
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
        read_only_fields = ['author']
        

    """ method to determine a duty status which is overdue or not """
    def get_deadline_status(self, duty):
        if duty.done_status != 'not':
            return 'Duty is done!'
        if duty.deadline_date > timezone.now().date():
            return 'Deadline has not expired yet!'
        return 'Deadline is over!'
    
    def get_absolute_url(self, duty):
        request = self.context.get('request')
        return request.build_absolute_uri(duty.pk)
    
    """ separate representation in list and detail """
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs'):
            """ omit snippet in detail page """
            rep.pop('snippet', None)
        else:
            """ remove description in list """
            rep.pop('description', None)
        return rep
    
    """ override create method in order to get the author from authentication data """
    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(user__id=self.context.get("request").user.id)
        return super().create(validated_data)