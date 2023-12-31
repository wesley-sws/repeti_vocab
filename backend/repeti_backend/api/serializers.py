from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import *


class AppSynsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSynset
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserListSerializer(serializers.ModelSerializer):
    synset = AppSynsetSerializer(read_only=True)
    class Meta:
        model = UserList
        fields = ['word', 'synset']


class WordReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordReview
        fields = '__all__'


class MCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQOption
        fields = '__all__'
