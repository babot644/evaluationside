from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='register-home'),
    path('login/', views.login , name='login-page'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('availableseminars/', views.availableSeminars, name='availableseminars'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('evaluateSeminar/', views.evaluateSeminar, name='evaluateSeminar'),
    
    path('firstEvaluation/', views.evaluationInfo, name='firstEvaluation'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('forgotPasswordConfirm/', views.forgotPasswordConfirm, name='forgotPasswordConfirm'),
]