---  
  
## 🧱 1. Install Required Packages  
  
If not already installed:  
  
```bash  
pip install djangorestframework djangorestframework-simplejwt```  
  
---  
  
## ⚙️ 2. Update `settings.py`  
  
Add to `INSTALLED_APPS`:  
  
```python  
INSTALLED_APPS = [  
 ... 'rest_framework',]  
```  
  
Configure DRF to use JWT:  
  
```python  
REST_FRAMEWORK = {  
 'DEFAULT_AUTHENTICATION_CLASSES': ( 'rest_framework_simplejwt.authentication.JWTAuthentication', ),}  
```  
  
(Optional) Add custom auth backend if needed:  
  
```python  
AUTHENTICATION_BACKENDS = ['yourapp.auth_backend.CustomAuthBackend']  
```  
  
---  
  
## 🔐 3. Create Custom Authentication Logic  
  
If your login uses something like `username + employee_id`, define a custom backend:  
  
```python  
# yourapp/auth_backend.py  
from django.contrib.auth.backends import BaseBackend  
from django.contrib.auth import get_user_model  
  
User = get_user_model()  
  
class CustomAuthBackend(BaseBackend):  
 def authenticate(self, request, username=None, employee_id=None, password=None): try: user = User.objects.get(username=username, profile__employee_id=employee_id) if user.check_password(password): return user except User.DoesNotExist: return None  
```  
  
---  
  
## 🧾 4. Create a Custom Token View  
  
```python  
# yourapp/views.py  
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework_simplejwt.tokens import RefreshToken  
from django.contrib.auth import authenticate  
  
class CustomTokenView(APIView):  
 def post(self, request): username = request.data.get('username') employee_id = request.data.get('employee_id') password = request.data.get('password')  
 user = authenticate(request, username=username, employee_id=employee_id, password=password) if user: refresh = RefreshToken.for_user(user) return Response({ 'refresh': str(refresh), 'access': str(refresh.access_token), }) return Response({'error': 'Invalid credentials'}, status=401)  
```  
  
---  
  
## 🌐 5. Add URL Route  
  
```python  
# yourapp/urls.py  
from django.urls import path  
from .views import CustomTokenView  
  
urlpatterns = [  
 path('api/token/', CustomTokenView.as_view(), name='custom_token'),]  
```  
  
Include it in your main `urls.py`:  
  
```python  
# project/urls.py  
from django.urls import path, include  
  
urlpatterns = [  
 ... path('', include('yourapp.urls')),]  
```  
  
---  
  
## 🔒 6. Protect API Views  
  
```python  
# yourapp/views.py  
from rest_framework.permissions import IsAuthenticated  
from rest_framework.views import APIView  
  
class ProtectedDataView(APIView):  
 permission_classes = [IsAuthenticated]  
 def get(self, request): return Response({'message': f'Welcome, {request.user.username}!'})  
```  
  
---  
  
## 🧪 7. Test the Flow  
  
1. POST to `/api/token/` with:  
   ```json  
  {  
 "username": "john", "employee_id": "EMP123", "password": "secret" }  
 ```  
2. Use the access token in headers:  
   ```  
  Authorization: Bearer <access_token>  
 ```  
3. Access protected views like `/api/protected-data/`.  
  
--- 