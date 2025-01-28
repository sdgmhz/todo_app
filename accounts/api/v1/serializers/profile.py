from rest_framework import serializers
from ....models import Profile

# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields=["id", "email", "first_name", "last_name"]
    # check if user is verified or not. this is necessary in patch and put
    def validate(self, attrs):
        user = self.context.get("user")
        if not user.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is not verified"}
            )
        return super().validate(attrs)