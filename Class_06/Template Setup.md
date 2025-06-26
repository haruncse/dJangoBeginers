Setting up a layout-based header and footer in Django templates is a great way to maintain consistency across your web pages. Here's a **step-by-step** guide to implementing it:

### 1️⃣ **Create a Base Template**
In your **templates/** folder, create a file called `base.html` that will hold the common structure.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>

    <!-- Header -->
    {% include "header.html" %}

    <!-- Main Content -->
    <div>
        {% block content %}
        {% endblock %}
    </div>

    <!-- Footer -->
    {% include "footer.html" %}

</body>
</html>
```

---

### 2️⃣ **Create the Header Template**
Inside the **templates/** folder, create `header.html` and add the header markup.

```html
<header>
    <h1>Welcome to My Site</h1>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
        </ul>
    </nav>
</header>
```

---

### 3️⃣ **Create the Footer Template**
Similarly, create `footer.html` inside the **templates/** folder and add footer content.

```html
<footer>
    <p>&copy; 2025 My Website. All rights reserved.</p>
</footer>
```

---

### 4️⃣ **Extending the Base Template**
For individual pages, such as `home.html`, extend `base.html`.

```html
{% extends "base.html" %}

{% block title %} Home Page {% endblock %}

{% block content %}
    <h2>This is the home page content.</h2>
{% endblock %}
```

---

### 5️⃣ **Configuring Django to Use Templates**
Make sure your Django settings are configured to recognize templates. In **settings.py**, add:

```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "templates"],  # Ensure the templates folder is listed
    },
]
```

Now, your Django project will consistently use the **header** and **footer** across all pages!

Great! Let's go **step by step** on how to use the header-footer layout in your Django project. I'll walk you through **setting up the templates, rendering views, and linking the header/footer dynamically.**  

---

### **1️⃣ Create a Django App (If Not Already Done)**
First, make sure you have a Django project. If not, create one:  

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

**Register your app** in `settings.py` under `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",  # Add your app here
]
```

---

### **2️⃣ Set Up Your Templates Folder**
Inside your `myapp/` directory, create a folder called **templates/**.  
Then, inside `templates/`, add subfolders for better organization:

```bash
mkdir templates/myapp
```

Ensure Django recognizes the templates directory in `settings.py`:

```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "templates"],  # Ensure the templates folder is included
    },
]
```

---

### **3️⃣ Create the Base Template (base.html)**
Your base template should contain the common layout, like **header and footer**.

#### 📄 `templates/myapp/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Default Page Title{% endblock %}</title>
</head>
<body>

    <!-- Include Header -->
    {% include "myapp/header.html" %}

    <!-- Main Content -->
    <div>
        {% block content %}
        {% endblock %}
    </div>

    <!-- Include Footer -->
    {% include "myapp/footer.html" %}

</body>
</html>
```

---

### **4️⃣ Create Header & Footer Templates**
These templates will be reusable across pages.

#### 📄 `templates/myapp/header.html`
```html
<header>
    <h1>Welcome to My Website</h1>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about/">About</a></li>
        </ul>
    </nav>
</header>
```

#### 📄 `templates/myapp/footer.html`
```html
<footer>
    <p>&copy; 2025 My Website - All rights reserved.</p>
</footer>
```

---

### **5️⃣ Create a Page that Uses the Layout**
Now, let's create a page that extends the base template.

#### 📄 `templates/myapp/home.html`
```html
{% extends "myapp/base.html" %}

{% block title %}Home - My Website{% endblock %}

{% block content %}
    <h2>Welcome to the home page!</h2>
    <p>This content is wrapped in the base layout.</p>
{% endblock %}
```

---

### **6️⃣ Render Views and Link the Template**
Now, you need to create a Django view that loads the template.

#### 📄 `myapp/views.py`
```python
from django.shortcuts import render

def home(request):
    return render(request, "myapp/home.html")
```

---

### **7️⃣ Set Up URLs**
Finally, define the route to serve the home page.

#### 📄 `myapp/urls.py`
```python
from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),
]
```

Include the app's URLs in the main project:

#### 📄 `myproject/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
]
```

---

### **8️⃣ Run the Server & View Your Page**
Now, start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser, and you'll see your home page with a **header and footer**!

---

### **🚀 Bonus: Passing Dynamic Data to Header/Footer**
If you want the header or footer to display **dynamic content**, like the logged-in user's name, modify your view:

#### 📄 `views.py`
```python
def home(request):
    user_name = "Harun"  # Example dynamic data
    return render(request, "myapp/home.html", {"user_name": user_name})
```

Then, update `header.html` to display the user’s name:

```html
<header>
    <h1>Welcome, {{ user_name }}!</h1>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about/">About</a></li>
        </ul>
    </nav>
</header>
```
Using a base template **across multiple apps** in Django is straightforward. The key is ensuring your templates are accessible globally within your project. Here's **how to use a base template in another app** step by step:

---

### **1️⃣ Store the Base Template in a Global Location**
Instead of keeping the **base.html** template inside an app-specific folder, place it inside a **global templates folder**.  
Create a `templates/` directory inside your project root:

```bash
mkdir templates
```

Move the `base.html` template into the **global** templates folder:

```
myproject/
│── myapp/
│── anotherapp/
│── templates/    <---- Global folder for shared templates
│    ├── base.html
│    ├── header.html
│    ├── footer.html
```

---

### **2️⃣ Configure Django to Use Global Templates**
Tell Django to look for templates **inside the global folder** by modifying `settings.py`:

```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "templates"],  # Ensure this points to the global folder
    },
]
```

Now, Django can use `base.html` across all apps!

---

### **3️⃣ Extend the Base Template in Another App**
Inside `anotherapp/templates/anotherapp/home.html`, extend the base template:

```html
{% extends "base.html" %}

{% block title %} Home - Another App {% endblock %}

{% block content %}
    <h2>This is the home page from another app!</h2>
    <p>Since we placed `base.html` globally, this template can use it!</p>
{% endblock %}
```

---

### **4️⃣ Create a View for Another App**
In `anotherapp/views.py`, render the `home.html` template:

```python
from django.shortcuts import render

def another_home(request):
    return render(request, "anotherapp/home.html")
```

---

### **5️⃣ Define URLs for Another App**
In `anotherapp/urls.py`, set up the route:

```python
from django.urls import path
from .views import another_home

urlpatterns = [
    path("", another_home, name="another_home"),
]
```

Include `anotherapp` URLs inside `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),  # Main app
    path("anotherapp/", include("anotherapp.urls")),  # Another app
]
```

---

### **6️⃣ Run the Server & Check**
Start Django:

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/anotherapp/** and you'll see your page **using the global base.html** 🎉  

---

### **✨ Bonus: Using Global Header/Footer in Another App**
Since `header.html` and `footer.html` are also **global**, your other app can use them without duplication.

Update `base.html` to include them:

```html
{% include "header.html" %}
{% include "footer.html" %}
```

Now, `anotherapp` templates **automatically** get the same layout!   

