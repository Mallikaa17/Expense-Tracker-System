# from django.contrib import admin
# from django.urls import path,include 
# from apps.accounts import views
# from .views import LoginView
# from .views import *
# from rest_framework.routers import DefaultRouter
# from .views import ExpenseViewSet

# router = DefaultRouter()
# router.register(r'expenses', ExpenseViewSet, basename='expenses')



# urlpatterns =router.urls, [
#     path('admin/', admin.site.urls),
#     path('login/', LoginView.as_view(), name='login'),
#     path('update-profile/', UpdateProfileView.as_view()),





    # path('add-expense/', AddExpenseView.as_view()),
    # path('expenses/', ListExpenseView.as_view()),
    # path('update-expense/<int:pk>/', UpdateExpenseView.as_view()),
    # path('delete-expense/<int:pk>/', DeleteExpenseView.as_view()),
    # path('filter-expense/', FilterExpenseView.as_view()),
    # path('summary/', ExpenseSummaryView.as_view()),

# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, LoginView, RegisterView, UpdateProfileView, add_expense_page
from django.http import HttpResponse
from django.urls import path

def test(request):
    return HttpResponse("WORKING")

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', UpdateProfileView.as_view()),
    path('', include(router.urls)), 
    path('profile/', UpdateProfileView.as_view()),
    path('add-expense/', add_expense_page),
    path('test/', test),
]