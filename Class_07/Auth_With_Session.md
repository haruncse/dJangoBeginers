To implement a **custom authentication login and session system** in a Django project, here’s a step-by-step guideline
---

### 🛠️ Step-by-Step: Custom Auth Login & Session in Django

#### 1. **Start Your Project and App**
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp accounts
```

#### 2. **Create a Custom User Model**
In `accounts/models.py`:
```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```

Create `accounts/managers.py`:
```python
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
```

#### 3. **Update `settings.py`**
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

#### 4. **Create Authentication Backend (Optional)**
In `accounts/backends.py`:
```python
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
```

Then in `settings.py`:
```python
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']
```

#### 5. **Create Login and Registration Forms**
In `accounts/forms.py`:
```python
from django import forms
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")
```

#### 6. **Create Views for Login, Logout, and Register**
In `accounts/views.py`:
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from .models import CustomUser

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
```

#### 7. **Configure URLs**
In `accounts/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
```

Include it in your project’s `urls.py`:
```python
path('accounts/', include('accounts.urls')),
```

#### 8. **Session Management**
Django handles sessions automatically when you use `login()` and `logout()`. You can customize session expiry:
```python
# settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

---


To bind or restrict access to certain URLs based on session authentication in Django, you can use **login-required decorators**, **middleware**, or **custom logic in views**. Here's a breakdown of how to do it effectively:

---

### 🔐 1. **Restrict URLs Using `@login_required`**

This is the most common and cleanest way to protect views.

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')
```

This ensures that only authenticated users can access the `dashboard_view`. If not logged in, they’ll be redirected to the login page.

---

### 🧭 2. **Protect URL Patterns in `urls.py`**

You can wrap views directly in `urls.py`:

```python
from django.contrib.auth.decorators import login_required
from .views import dashboard_view

urlpatterns = [
    path('dashboard/', login_required(dashboard_view), name='dashboard'),
]
```

---

### 🧱 3. **Use Middleware for Global Protection**

If you want to restrict access to a whole section of your site (e.g., `/admin/`, `/dashboard/`), you can write custom middleware:

```python
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/dashboard/'):
            return redirect('/accounts/login/')
        return self.get_response(request)
```

Then add it to `MIDDLEWARE` in `settings.py`.

---

### 🧠 4. **Session-Based Logic in Views**

You can also use session data to control access:

```python
def some_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    # Proceed with view logic
```

But since Django already handles sessions when using `login()`, this is rarely needed unless you're managing sessions manually.

---

### 🧪 5. **Template-Level Access Control (Optional)**

In templates, you can check if a user is authenticated:

```html
{% if user.is_authenticated %}
  <a href="{% url 'dashboard' %}">Dashboard</a>
{% else %}
  <a href="{% url 'login' %}">Login</a>
{% endif %}
```

---

Template Setup
---

### 🗂️ 1. Project Structure Overview

```
myproject/
├── accounts/
│   ├── templates/
│   │   └── accounts/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── dashboard.html
```

Make sure `DIRS` in `settings.py` points to the templates folder:

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'accounts' / 'templates'],
        ...
    },
]
```

---

### 🧱 2. `base.html` – Shared Layout

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light px-4">
        <a class="navbar-brand" href="#">MyApp</a>
        <div class="ms-auto">
            {% if user.is_authenticated %}
                <a href="{% url 'dashboard' %}" class="btn btn-outline-primary me-2">Dashboard</a>
                <a href="{% url 'logout' %}" class="btn btn-outline-danger">Logout</a>
            {% else %}
                <a href="{% url 'login' %}" class="btn btn-outline-primary me-2">Login</a>
                <a href="{% url 'register' %}" class="btn btn-outline-success">Register</a>
            {% endif %}
        </div>
    </nav>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

---

### 🔐 3. `login.html`

```html
{% extends 'accounts/base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<h2>Login</h2>
<form method="post" class="card p-4 shadow-sm">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Login</button>
</form>
{% endblock %}
```

---

### 📝 4. `register.html`

```html
{% extends 'accounts/base.html' %}
{% block title %}Register{% endblock %}
{% block content %}
<h2>Register</h2>
<form method="post" class="card p-4 shadow-sm">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success">Register</button>
</form>
{% endblock %}
```

---

### 🧭 5. `dashboard.html` (Protected View)

```html
{% extends 'accounts/base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<h2>Welcome, {{ user.username }}!</h2>
<p>This is your dashboard. Only logged-in users can see this.</p>
{% endblock %}
```

---

### 🧪 6. Test It All Together

- Make sure your views return the correct templates.
- Use `@login_required` on views like `dashboard_view`.
- Run `python manage.py runserver` and test `/accounts/login/`, `/accounts/register/`, and `/dashboard/`.
---

Step by Step
---

## 🧱 1. Project Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install django
django-admin startproject myproject
cd myproject
python manage.py startapp accounts
```

---

## 🧩 2. Custom User Model

### `accounts/models.py`
```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```

### `accounts/managers.py`
```python
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
```

---

## ⚙️ 3. Settings Configuration

### `settings.py`
```python
INSTALLED_APPS = [
    ...
    'accounts',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'accounts' / 'templates'],
        ...
    },
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

---

## 🧠 4. Forms

### `accounts/forms.py`
```python
from django import forms
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")
```

---

## 🧭 5. Views

### `accounts/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')
```

---

## 🌐 6. URLs

### `accounts/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
```

### `myproject/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
```

---

## 🖼️ 7. Templates

### `accounts/templates/accounts/base.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
</head>
<body>
    {% if user.is_authenticated %}
        <a href="{% url 'dashboard' %}">Dashboard</a>
        <a href="{% url 'logout' %}">Logout</a>
    {% else %}
        <a href="{% url 'login' %}">Login</a>
        <a href="{% url 'register' %}">Register</a>
    {% endif %}
    <hr>
    {% block content %}{% endblock %}
</body>
</html>
```

### `login.html`, `register.html`, `dashboard.html`
Extend `base.html` and include forms or messages as needed (you already saw examples earlier).

---

## 🧪 8. Final Steps

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---