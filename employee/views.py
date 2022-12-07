from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect,HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, logout, login
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.urls import reverse,reverse_lazy

class Signup(APIView): 
    """
    A viewset for signup and signin of an user
    """
    authentication_classes = [] 
    permission_classes = [] 

    def post(self, request, format=None):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(is_superuser=True,active=True,is_staff=True,password=make_password(request.data['password']))
            return redirect('employee:index')
            # return Response({"status":True,"message":"Success","data":serializer.data,"token":token.key})
        else:
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            return Response({"status":False,"message":error_list[0]})

    # @action(methods=['POST'], detail=False,url_path="login")
class Login(APIView):
    authentication_classes = [] 
    permission_classes = [] 

    def post(self, request, format=None):
        data=request.data
        email=data['email']
        password=data['password']
        try:
            user=User.objects.get(email=email)
            user_id=user.id
            if user:
                user=authenticate(email=email,password=password)
                if(user!=None):
                    token, created = Token.objects.get_or_create(user=user_id)
                    result={
                        'id':user_id,
                        'token':token.key
                    }
                    # return Response({"status":True,"message":"Login success","data":result})
                    # return re(request,"show.html")
                    return redirect('create/') 
                # return Response({"status":False,"message":"Invalid password"})/
                messages.error(request, 'Invalid password".')
                return redirect('employee:index')
                # return HttpResponseRedirect(reverse_lazy('employee:index'))

            messages.error(request, 'Not an user".')
            return redirect('employee:index')
            # return HttpResponseRedirect(reverse_lazy('employee:index'))
        except User.DoesNotExist:
            messages.error(request, 'User Does not exists".')
            return redirect('employee:index')
                # return Response({"status":False,"message":"User Does not exists"})

@permission_classes((IsAuthenticated, ))
class CreateEmployee(APIView):
    """
        View for create and list employee data
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'menu.html'
    # permission_classes = (AllowAny,)

    def get(self, request):
        obj = Employee.objects.all().order_by('-id')
        serilized = EmployeeSerializers(obj, many=True)
        data=serilized.data
        print(data)
        # return render('show.html',{'context':data})
        # return Response({"context": data}, template_name="show.html")
        return render(request, "show.html",{"context":data})
        # return Response(serilized.data)

    def post(self, request):
        data = request.data
        serializer = EmployeeSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            data={
                "id":serializer.data['id'],
                "name":serializer.data['name'],
                "code":serializer.data['employee_code']
            }
            print(data)
            return render(request,"salary.html",data)
            # return redirect('employee:create')
            # return HttpResponseRedirect(reverse('mployee:login/create/'))
            # return Response({"status": True,"Message": "Successfully added new employee"})
        else:
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            messages.error(request, error_list[0])
            return redirect("employee:creationform")
            # return Response({"status": False, "Message": serializer.errors})


@permission_classes((IsAuthenticated, ))
class ViewEmployee(APIView):
    """
        View for Edit Delete Retrieve Employee data
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, id, *args, **kwargs):
        obj = Employee.objects.filter(id=id)
        serializer = EmployeeSerializers(obj, many=True)
        data = serializer.data
        return render(request,"view.html",{"context":data})
        # return Response(data)

@permission_classes((IsAuthenticated, ))
class EditEmployee(APIView):

    def get(self, request, id, *args, **kwargs):
        obj = Employee.objects.filter(id=id)
        serializer = EmployeeSerializers(obj, many=True)
        data = serializer.data
        return render(request,"edit.html",{"context":data})

    def post(self, request, id):
        print(id)
        obj = Employee.objects.get(id=id)
        data = request.data
        serializer = EmployeeSerializers(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # return Response({"status": True,"Message": "Employee data successfully Updated"})
            return redirect('employee:create')
        else:
            return Response({"status": False,"Message": "Employee data Updation Failed"})

    def delete(self,request,id,*args,**kwargs,):
        obj = Employee.objects.get(pk=id)
        try:
            obj.delete()
            # return Response({"status": True,"Message": "Employee Deleted"})
            return redirect('employee:create')
        except:
            return Response({"status": False, "Message": "Employee Deletion Failed"})


@permission_classes((IsAuthenticated, ))
class DeleteEmployee(APIView):

    def get(self, request, id, *args, **kwargs):
        obj = Employee.objects.filter(id=id)
        serializer = EmployeeSerializers(obj, many=True)
        data = serializer.data
        return render(request,"delete.html",{"context":data})

    def post(self,request,id,*args,**kwargs,):
        obj = Employee.objects.get(pk=id)
        try:
            obj.delete()
            # return Response({"status": True,"Message": "Employee Deleted"})
            return redirect('employee:create')
        except:
            return Response({"status": False, "Message": "Employee Deletion Failed"})

def index(request):
    return redirect(request,"")

def creationform(request):
    return redirect(request,"creationform.html")

def createuser(request):
    return redirect(request,"createuser.html")