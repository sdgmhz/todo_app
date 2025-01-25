from rest_framework import serializers
from ....models import Profile

# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields=["id", "email", "first_name", "last_name"]

    def validate(self, attrs):
        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is not verified"}
            )
        return super().validate(attrs)