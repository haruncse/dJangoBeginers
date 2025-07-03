Here’s a complete guide on how to **create, retrieve, and destroy session data** in Django using the built-in session framework.

---

## 🧠 1. What Are Django Sessions?

Django sessions allow you to store and retrieve arbitrary data on a per-user basis. The data is stored server-side (in the database, cache, or file), and the client only holds a session ID in a cookie.

To enable sessions, make sure your `settings.py` includes:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

Then run:
```bash
python manage.py migrate
```

---

## 🛠️ 2. Create (Set) Session Data

In your view:
```python
def set_session(request):
    request.session['username'] = 'harun_dev'
    request.session['role'] = 'admin'
    request.session['login_count'] = request.session.get('login_count', 0) + 1
    return HttpResponse("Session data set.")
```

You can also set expiry:
```python
request.session.set_expiry(1800)  # 30 minutes
```

---

## 🔍 3. Retrieve (Get) Session Data

```python
def get_session(request):
    username = request.session.get('username', 'Guest')
    role = request.session.get('role', 'none')
    login_count = request.session.get('login_count', 0)
    return HttpResponse(f"User: {username}, Role: {role}, Logins: {login_count}")
```

In templates:
```html
<p>Welcome {{ request.session.username }}</p>
```

---

## ❌ 4. Delete Session Data

### Delete a specific key:
```python
def delete_key(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse("Username session key deleted.")
```

### Use `pop()` safely:
```python
request.session.pop('role', None)
```

### Clear all session data (but keep session ID):
```python
request.session.clear()
```

### Flush session (delete all data and session ID):
```python
request.session.flush()
```
> This is what Django’s `logout()` function uses internally.

---

## 🧪 5. Example Use Case: Visit Counter

```python
def visit_counter(request):
    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1
    return HttpResponse(f"You have visited this page {request.session['visits']} times.")
```

---

## 🧼 6. Clean Up Expired Sessions

Run this periodically (e.g., via cron):
```bash
python manage.py clearsessions
```
This removes expired sessions from the database without logging out active users.

---