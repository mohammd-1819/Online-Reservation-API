import re
from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'fullname', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("لطفاً یک ایمیل معتبر وارد کنید.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("رمز عبور باید شامل حروف و اعداد باشد.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            fullname=validated_data.get('fullname', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

