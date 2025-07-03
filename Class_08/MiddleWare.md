To protect multiple URLs across different Django apps using **custom middleware**, you can create a centralized middleware that checks authentication and restricts access based on URL patterns. Here's a full step-by-step guide:

---

## 🛡️ Step-by-Step: Protect Multiple URLs with Middleware in Django

### 📁 1. Create Middleware File

In your project or a common app (e.g., `accounts/middleware.py`):

```python
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            '/dashboard/',
            '/admin-panel/',
            '/profile/',
            '/orders/',
        ]

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.protected_paths):
            if not request.user.is_authenticated:
                return redirect(reverse('login'))
        return self.get_response(request)
```

> 🔍 You can customize `self.protected_paths` to include any URL prefixes from **any app**.

---

### ⚙️ 2. Register Middleware in `settings.py`

Add your middleware **after** `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.LoginRequiredMiddleware',  # 👈 Add this
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

### 🧪 3. Test with Multiple Apps

Let’s say you have:

- `dashboard/` in `dashboard/urls.py`
- `admin-panel/` in `adminpanel/urls.py`
- `orders/` in `orders/urls.py`

As long as those paths are listed in `self.protected_paths`, the middleware will **block unauthenticated access** and redirect to the login page.

---

### 🧠 Optional Enhancements

- **Use regex or `re.match()`** for more flexible pattern matching.
- **Whitelist paths** like `/accounts/login/`, `/accounts/register/` to avoid redirect loops.
- **Use `request.resolver_match.view_name`** to protect by view name instead of URL.

---

### ✅ Example with Whitelist

```python
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = ['/dashboard/', '/admin-panel/', '/orders/']
        self.exempt_paths = ['/accounts/login/', '/accounts/register/']

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.protected_paths):
            if not request.user.is_authenticated and request.path not in self.exempt_paths:
                return redirect(reverse('login'))
        return self.get_response(request)
```
---