To integrate **JWT authentication** into your existing Django project with custom login and session handling, here’s a **step-by-step guide** using Django REST Framework and `djangorestframework-simplejwt`:

---

## 🔐 Step-by-Step: Add JWT Auth to Your Django Project

### 📦 1. Install Required Packages

```bash
pip install djangorestframework djangorestframework-simplejwt
```

---

### ⚙️ 2. Update `settings.py`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

Optional: Customize token lifetime
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

### 🧰 3. Create Token Views

In `accounts/api_views.py`:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=401)
```

---

### 🌐 4. Add JWT URLs

In `accounts/urls.py`:

```python
from django.urls import path
from .api_views import CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns += [
    path('api/token/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

### 🔒 5. Protect API Views

In any API view:

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Hello {request.user.username}, you are authenticated!'})
```

---

### 🧪 6. Test with Postman or cURL

- **POST** to `/accounts/api/token/` with:
```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

- Use the returned `access` token in headers:
```
Authorization: Bearer <access_token>
```

- Access protected endpoints like `/api/protected/`.

---

### ✅ Done!

You now have:
- Custom login using JWT
- Stateless authentication for APIs
- Session-based login for web views (optional)

---
