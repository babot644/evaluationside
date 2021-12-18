from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='register-home'),
    path('login/', views.login , name='login-page'),
    path('logout/', views.logout, name="logout"),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('availableseminars/', views.availableSeminars, name='availableseminars'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('evaluateSeminar/', views.evaluateSeminar, name='evaluateSeminar'),
    path('firstEvaluation/', views.firstEvaluation, name='firstEvaluation'),
    path('secondEvaluation/', views.secondEvaluation, name='secondEvaluation'),
    path('thirdEvaluation/', views.thirdEvaluation, name='thirdEvaluation'),
    path('fourthEvaluation/', views.fourthEvaluation, name='fourthEvaluation'),
    path('fifthEvaluation/', views.fifthEvaluation, name='fifthEvaluation'),
    path('sixthEvaluation/', views.sixthEvaluation, name='sixthEvaluation'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('forgotPasswordConfirm/', views.forgotPasswordConfirm, name='forgotPasswordConfirm'),
]