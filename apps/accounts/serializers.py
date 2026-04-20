from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
   

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'] 
        )
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 

from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['user']


class CategorySummarySerializer(serializers.Serializer):
    category = serializers.CharField()
    total = serializers.FloatField()


class ExpenseSummarySerializer(serializers.Serializer):
    total_expense = serializers.FloatField()
    category_wise = CategorySummarySerializer(many=True)

class AnalyticsQuerySerializer(serializers.Serializer):
    month = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)