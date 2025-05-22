Here's a step-by-step guide to perform basic CRUD (Create, Read, Update, Delete) operations using Django:

---

### Step 1: Set Up a Django Project
1. Install Django:  
   ```bash
   pip install django
   ```
2. Create a new Django project:  
   ```bash
   django-admin startproject myproject
   ```
3. Navigate into the project directory:
   ```bash
   cd myproject
   ```

---

### Step 2: Create a Django App
1. Create a new app within the project:  
   ```bash
   python manage.py startapp myapp
   ```
2. Register your app in `settings.py`:
   ```python
   INSTALLED_APPS = [
       'myapp',
       # other apps...
   ]
   ```

---

### Step 3: Define the Model
1. Open `models.py` in your app directory and define a model:
   ```python
   from django.db import models

   class Item(models.Model):
       name = models.CharField(max_length=255)
       description = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
   ```
2. Run migrations to create the database table:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

### Step 4: Create the Views
1. Define views in `views.py` for each CRUD operation:
   - **Create**: Add a new item.
   - **Read**: List all items or view details of a single item.
   - **Update**: Edit an existing item.
   - **Delete**: Remove an item.

Example:
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item

# Create
def create_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Item.objects.create(name=name, description=description)
        return redirect('item_list')
    return render(request, 'create_item.html')

# Read
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html', {'item': item})

# Update
def update_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.save()
        return redirect('item_list')
    return render(request, 'update_item.html', {'item': item})

# Delete
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    return redirect('item_list')
```

---

### Step 5: Create Templates
1. Add HTML templates for each view (e.g., `create_item.html`, `item_list.html`, etc.) in a `templates` directory:
   ```html
   <!-- Example: item_list.html -->
   <h1>Items</h1>
   <ul>
       {% for item in items %}
           <li>{{ item.name }} - <a href="{% url 'item_detail' item.id %}">Details</a></li>
       {% endfor %}
   </ul>
   ```

---

### Step 6: Configure URLs
1. In `urls.py` of your app, define URL patterns:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.item_list, name='item_list'),
       path('item/<int:id>/', views.item_detail, name='item_detail'),
       path('create/', views.create_item, name='create_item'),
       path('update/<int:id>/', views.update_item, name='update_item'),
       path('delete/<int:id>/', views.delete_item, name='delete_item'),
   ]
   ```

2. Include the app URLs in your project's `urls.py`:
   ```python
   from django.urls import include, path

   urlpatterns = [
       path('myapp/', include('myapp.urls')),
   ]
   ```

---

### Step 7: Run the Server
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application in your browser at `http://127.0.0.1:8000/myapp`.

---

Here’s a detailed breakdown of the HTML templates required for your CRUD operations. You'll place these templates in the `templates` directory within your Django app.

---

### 1. **`create_item.html`**
This template will contain a form for creating a new item. Use the Django template syntax to handle the POST method.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create Item</title>
</head>
<body>
    <h1>Create a New Item</h1>
    <form method="POST">
        {% csrf_token %}
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br>
        <label for="description">Description:</label>
        <textarea id="description" name="description" required></textarea>
        <br>
        <button type="submit">Create</button>
    </form>
    <a href="{% url 'item_list' %}">Back to Items</a>
</body>
</html>
```

---

### 2. **`item_list.html`**
This template will display all items in a list format. It includes links to view, update, and delete items.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <ul>
        {% for item in items %}
            <li>
                <strong>{{ item.name }}</strong>
                <a href="{% url 'item_detail' item.id %}">View</a>
                <a href="{% url 'update_item' item.id %}">Edit</a>
                <a href="{% url 'delete_item' item.id %}">Delete</a>
            </li>
        {% endfor %}
    </ul>
    <a href="{% url 'create_item' %}">Create New Item</a>
</body>
</html>
```

---

### 3. **`item_detail.html`**
This template will show detailed information about a single item.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Item Detail</title>
</head>
<body>
    <h1>Item Details</h1>
    <p><strong>Name:</strong> {{ item.name }}</p>
    <p><strong>Description:</strong> {{ item.description }}</p>
    <p><strong>Created At:</strong> {{ item.created_at }}</p>
    <a href="{% url 'item_list' %}">Back to Items</a>
</body>
</html>
```

---

### 4. **`update_item.html`**
This template will allow you to edit an existing item using a form populated with the current values.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Item</title>
</head>
<body>
    <h1>Edit Item</h1>
    <form method="POST">
        {% csrf_token %}
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" value="{{ item.name }}" required>
        <br>
        <label for="description">Description:</label>
        <textarea id="description" name="description" required>{{ item.description }}</textarea>
        <br>
        <button type="submit">Update</button>
    </form>
    <a href="{% url 'item_list' %}">Back to Items</a>
</body>
</html>
```

---

### 5. **`delete_item.html`** (Optional)
You could include a confirmation screen for deleting an item, but it's optional. Django can handle deletion directly if you prefer.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Item</title>
</head>
<body>
    <h1>Confirm Deletion</h1>
    <p>Are you sure you want to delete "<strong>{{ item.name }}</strong>"?</p>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
    </form>
    <a href="{% url 'item_list' %}">Cancel</a>
</body>
</html>
```

---

### Directory Structure
Make sure your `templates` folder is structured as follows:
```
myapp/
└── templates/
    ├── create_item.html
    ├── item_list.html
    ├── item_detail.html
    ├── update_item.html
    └── delete_item.html
```
