from django.urls import path
from .views import *
from django.views.generic.base import TemplateView
app_name = 'employee'
urlpatterns = [
    path('login/',Login.as_view()),
    path('login/create/',CreateEmployee.as_view(),name='create'),
    path('view/<int:id>/',ViewEmployee.as_view(),name='view'),
    path('edit/<int:id>/',EditEmployee.as_view(),name='edit'),
    path('delete/<int:id>/',DeleteEmployee.as_view(),name='delete'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('creationform', TemplateView.as_view(template_name='creationform.html'), name='creationform'),
    path('signup',Signup.as_view(),name='signup'),
    path('createuserform', TemplateView.as_view(template_name='createuser.html'), name='createuser'),
]