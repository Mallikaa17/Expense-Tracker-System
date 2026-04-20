from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, LoginView, RegisterView, UpdateProfileView, add_expense_page
from django.http import HttpResponse
from .analytics_views import AnalyticsViewSet
from django.urls import path


def test(request):
    return HttpResponse("WORKING")

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', UpdateProfileView.as_view()),
    path('', include(router.urls)), 
    path('profile/', UpdateProfileView.as_view()),
    path('add-expense/', add_expense_page),
    path('test/', test),
    
]

urlpatterns += router.urls