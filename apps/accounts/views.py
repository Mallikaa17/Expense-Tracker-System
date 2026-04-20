from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
from .serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UpdateUserSerializer
from .models import Expense
from .serializers import ExpenseSerializer, ExpenseSummarySerializer

def add_expense_page(request):
    return render(request, "account/add-expense.html")

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response({
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)

            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer) 
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={200: UpdateUserSerializer}
    )
    def patch(self, request):
        user = request.user   

        serializer = UpdateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class AddExpenseView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [JSONParser]

#     @swagger_auto_schema(request_body=ExpenseSerializer)

#     def post(self, request):
#         serializer = ExpenseSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({
#                 "message": "Expense added successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ListExpenseView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         expenses = Expense.objects.filter(user=request.user).order_by('-date')
#         serializer = ExpenseSerializer(expenses, many=True)

#         return Response(serializer.data)
    
# class UpdateExpenseView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, pk):
#         try:
#             expense = Expense.objects.get(id=pk, user=request.user)
#         except Expense.DoesNotExist:
#             return Response({"error": "Not found"}, status=404)

#         serializer = ExpenseSerializer(expense, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Expense updated",
#                 "data": serializer.data
#             })

#         return Response(serializer.errors, status=400)
    
# class DeleteExpenseView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             expense = Expense.objects.get(id=pk, user=request.user)
#         except Expense.DoesNotExist:
#             return Response({"error": "Not found"}, status=404)

#         expense.delete()
#         return Response({"message": "Deleted successfully"})
    
# class FilterExpenseView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'category',
#                 openapi.IN_QUERY,
#                 description="Filter by category",
#                 type=openapi.TYPE_STRING
#             ),
#             openapi.Parameter(
#                 'start_date',
#                 openapi.IN_QUERY,
#                 description="Start date (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING
#             ),
#             openapi.Parameter(
#                 'end_date',
#                 openapi.IN_QUERY,
#                 description="End date (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING
#             ),
#         ]
#     )
#     def get(self, request):
#         expenses = Expense.objects.filter(user=request.user)

#         category = request.query_params.get('category')
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')

#         if category:
#             expenses = expenses.filter(category=category)

#         if start_date and end_date:
#             expenses = expenses.filter(date__range=[start_date, end_date])

#         serializer = ExpenseSerializer(expenses, many=True)
#         return Response(serializer.data)
    
# class ExpenseSummaryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         expenses = Expense.objects.filter(user=request.user)

#         total = expenses.aggregate(total=Sum('amount'))['total'] or 0

#         category_data = expenses.values('category').annotate(total=Sum('amount'))

#         return Response({
#             "total_expense": total,
#             "category_wise": category_data
#         })

# ✅ FILTER SERIALIZER (for Swagger query params)
class ExpenseFilterSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user).order_by('-date')

        category = self.request.query_params.get('category')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if category:
            queryset = queryset.filter(category=category)

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        print(self.request.user) 
        serializer.save(user=self.request.user)

    # ✅ LIST API (NOW SHOWS PARAMETERS IN SWAGGER)
    @swagger_auto_schema(
        operation_description="Get all expenses with filters",
        query_serializer=ExpenseFilterSerializer,
        responses={200: ExpenseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ✅ SUMMARY API (NOW SHOWS PARAMETERS IN SWAGGER)
    @swagger_auto_schema(
        operation_description="Get expense summary",
        query_serializer=ExpenseFilterSerializer,
        responses={200: ExpenseSummarySerializer}
    )
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        expenses = self.get_queryset()

        total = expenses.aggregate(total=Sum('amount'))['total'] or 0
        category_data = expenses.values('category').annotate(total=Sum('amount'))

        return Response({
            "total_expense": total,
            "category_wise": category_data
        })