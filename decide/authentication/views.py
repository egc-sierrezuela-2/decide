from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView, View
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404,render,redirect
from django.core.exceptions import ObjectDoesNotExist
from authentication.forms import RegisterForm
from django.http import HttpResponse
from .models import Persona

from .serializers import UserSerializer


class GetUserViewAPI(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutViewAPI(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterViewAPI(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


class RegisterView(View):
    def get(get, request):
        if(request.user.is_authenticated):
            return HttpResponse('Debe ingresar como usuario anonimo',status=403)
        form = RegisterForm()
        params = {'form':form}
        return render(request,'register.html',params)

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            params = {'form':form}
            return render(request,'register.html',params)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        pwd = form.cleaned_data['password']
        sex= form.cleaned_data['sexo']
        edad= form.cleaned_data['edad']
        
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0"   
        try:
            response = DbIpCity.get(ip,api_key='free')
            region = response.country #response.city
        except:
            region = "Desconocida"
        try:
            user = User(username=username)
            user.email = email
            user.set_password(pwd)
            user.save()
            persona = Persona(usuario = user, sexo=sex, ip=ip, edad=edad, region=region)
            persona.save()
            login(request,user, backend='authentication.backends.EmailOrUsernameModelBackend')
        except IntegrityError:
            params = {'form':form, 'message':'Usuario ya existente.'}
            return render(request,'register.html',params)
        return redirect('/authentication/login-success')

class LoginView(View):
    def get(get, request):
        if(request.user.is_authenticated):
            return HttpResponse('Debe ingresar como usuario anonimo',status=403)
        form = AuthenticationForm()
        params = {'form':form}
        return render(request,'login.html',params)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        usuario = request.POST['username']
        pwd = request.POST['password']
        acceso = authenticate(username=usuario,password=pwd)
        if acceso is None:
            params = {'form':form, 'message':'Usuario o contraseña incorrectas.'}
            return render(request,'login.html',params)
        if not acceso.is_active:
            params = {'form':form, 'message':'Usuario no activo.'}
            return render(request,'login.html',params)
        login(request,acceso)
        return redirect('/authentication/login-success')


class SuccessView(View):
    def get(get, request):
        if(not request.user.is_authenticated):
            return HttpResponse('Debe iniciar sesion',status=401)
        return render(request,'successful_login.html')