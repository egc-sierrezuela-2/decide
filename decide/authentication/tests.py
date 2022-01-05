from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from http import HTTPStatus
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

from base import mods


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )

class AuthPageTextCase(TestCase):
    def setUp(self):
        self.user = User(username='voter1')
        self.user.set_password('123')
        self.user.save()

    def test_form(self):
        form = RegisterForm(data={'username':'Prueba','email':'prueba@decide.es','password':'password123','sexo':'mujer','edad':'20'})
        
        self.assertTrue(form.is_valid())

    def test_form_no_username(self):
        form = RegisterForm(data={'email':'prueba@decide.es','password':'password123','sexo':'mujer','edad':'20'})

        self.assertEquals(form.errors['username'], ["This field is required."])

    def test_form_no_email(self):
        form = RegisterForm(data={'username':'prueba','password':'password123','sexo':'mujer','edad':'20'})

        self.assertEquals(form.errors['email'], ["This field is required."])

    def test_form_no_password(self):
        form = RegisterForm(data={'email':'prueba@decide.es','username':'prueba','sexo':'mujer','edad':'20'})

        self.assertEquals(form.errors['password'], ["This field is required."])

    def test_form_no_sex(self):
        form = RegisterForm(data={'email':'prueba@decide.es','password':'password123','username':'prueba','edad':'20'})

        self.assertEquals(form.errors['sexo'], ["This field is required."])

    def test_register_get(self):
        response = self.client.get("/authentication/register-alt/")

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertIsInstance(response.context['form'],RegisterForm)

    def test_register_logged(self):
        self.client.login(username='voter1', password='123')
        response = self.client.get("/authentication/register-alt/")

        self.assertEquals(response.status_code,403)

    def test_register_valid(self):
        response = self.client.post("/authentication/register-alt/",data={'username':'Prueba','email':'prueba@decide.es','password':'password123','sexo':'mujer','edad':'20'})
        user = User.objects.get(username="Prueba")

        self.assertRedirects(response,"/authentication/login-success", target_status_code=301)
        self.assertTrue(user.is_authenticated)

    def test_register_user_exists(self):
        response = self.client.post("/authentication/register-alt/",data={'username':'voter1','email':'prueba@decide.es','password':'password123','sexo':'mujer','edad':'20'})

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertEqual(response.context['message'],'Usuario ya existente.')

    def test_login_get(self):
        response = self.client.get("/authentication/login-alt/")

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertIsInstance(response.context['form'],AuthenticationForm)

    def test_login_logged(self):
        self.client.login(username='voter1', password='123')
        response = self.client.get("/authentication/login-alt/")

        self.assertEquals(response.status_code,403)
        self.assertEqual(int(self.client.session['_auth_user_id']),self.user.pk)

    def test_login_valid(self):
        #Comprueba que el usuario no esta logeado todavia
        self.assertTrue('_auth_user_id' not in self.client.session)
        
        response = self.client.post("/authentication/login-alt/",data={'username':'voter1','password':'123'})

        self.assertRedirects(response,"/authentication/login-success", target_status_code=301)
        self.assertEqual(int(self.client.session['_auth_user_id']),self.user.pk)
    
    def test_login_incorrect_password(self):
        response = self.client.post("/authentication/login-alt/",data={'username':'voter1','password':'novalida'})

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertEqual(response.context['message'],'Usuario o contraseña incorrectas.')

    def test_login_inexistent_user(self):
        response = self.client.post("/authentication/login-alt/",data={'username':'voter2','password':'123'})

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertEqual(response.context['message'],'Usuario o contraseña incorrectas.')

    def test_logout(self):
        #Logea y comprueba que esta logeado correctamente
        self.client.login(username='voter1', password='123')
        self.assertEqual(int(self.client.session['_auth_user_id']),self.user.pk)

        response = self.client.get("/authentication/logout-alt/")

        self.assertRedirects(response,"/authentication/login-alt/")
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_login_success_view(self):
        self.client.login(username='voter1', password='123')

        response = self.client.get("/authentication/login-success/")

        self.assertEquals(response.status_code,HTTPStatus.OK)
        self.assertTemplateUsed(response=response, template_name='successful_login.html')

        
    def test_login_success_view_unauthorized(self):
        response = self.client.get("/authentication/login-success/")

        self.assertEquals(response.status_code,401)

        
