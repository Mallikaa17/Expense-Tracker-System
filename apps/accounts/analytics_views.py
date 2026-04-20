from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import serializers

from django.utils.timezone import now
from django.db.models import Sum

from drf_yasg.utils import swagger_auto_schema

from .models import Expense, Income


# 🔹 Query Serializer
class AnalyticsQuerySerializer(serializers.Serializer):
    month = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)


class AnalyticsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]


    # 🔹 Monthly Expense
    @swagger_auto_schema(
        operation_description="Get total expense for a month",
        query_serializer=AnalyticsQuerySerializer
    )
    @action(detail=False, methods=['get'])
    def monthly_expense(self, request):

        serializer = AnalyticsQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        month = serializer.validated_data.get('month')
        year = serializer.validated_data.get('year')

        today = now()

        month = month if month else today.month
        year = year if year else today.year

        total = Expense.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "month": month,
            "year": year,
            "total_expense": total
        })


    # 🔹 Category Breakdown
    @swagger_auto_schema(
        operation_description="Category-wise expense breakdown",
        query_serializer=AnalyticsQuerySerializer
    )
    @action(detail=False, methods=['get'])
    def category_breakdown(self, request):

        serializer = AnalyticsQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        month = serializer.validated_data.get('month')
        year = serializer.validated_data.get('year')

        queryset = Expense.objects.filter(user=request.user)

        if month:
            queryset = queryset.filter(date__month=month)
        if year:
            queryset = queryset.filter(date__year=year)

        data = queryset.values('category__name') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')

        return Response(data)


    # 🔹 Income vs Expense
    @swagger_auto_schema(
        operation_description="Compare total income vs expense"
    )
    @action(detail=False, methods=['get'])
    def income_vs_expense(self, request):

        total_income = Income.objects.filter(user=request.user) \
            .aggregate(total=Sum('amount'))['total'] or 0

        total_expense = Expense.objects.filter(user=request.user) \
            .aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense
        })