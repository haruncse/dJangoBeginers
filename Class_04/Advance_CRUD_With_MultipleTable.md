Here's an example Django model using various field types:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # Short text
    description = models.TextField()  # Long text
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed-precision decimal
    stock = models.IntegerField()  # Numeric value
    available = models.BooleanField(default=True)  # Boolean
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp with updates
    image = models.ImageField(upload_to='products/')  # Image upload
    data = models.JSONField(null=True, blank=True)  # JSON storage
    
    category = models.ForeignKey("Category", on_delete=models.CASCADE)  # Many-to-One
    tags = models.ManyToManyField("Tag")  # Many-to-Many
    
    def __str__(self):
        return self.name  # String representation

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

### Explanation:
- **Product Model**: Defines a product with multiple attributes, such as name, price, availability, and category.
- **Category Model**: Represents product categories linked via `ForeignKey`.
- **Tag Model**: Allows multiple tags to be assigned to products through `ManyToManyField`.


Here's a complete **CRUD (Create, Read, Update, Delete)** implementation for your Django models using **views, forms, and templates**.

---

### **1. Create Forms for Product**
Define a Django form to handle product creation and editing.

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"  # Include all fields
```

---

### **2. Define CRUD Views**
Create views for handling product operations.

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

# Create a new product
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    
    return render(request, "product_form.html", {"form": form})


# Read (list) products
def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


# Update an existing product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    
    return render(request, "product_form.html", {"form": form})


# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    
    return render(request, "product_confirm_delete.html", {"product": product})
```

---

### **3. Configure URLs**
Set up URL patterns for CRUD operations.

```python
from django.urls import path
from .views import product_create, product_list, product_update, product_delete

urlpatterns = [
    path("", product_list, name="product_list"),
    path("create/", product_create, name="product_create"),
    path("update/<int:pk>/", product_update, name="product_update"),
    path("delete/<int:pk>/", product_delete, name="product_delete"),
]
```

---

### **4. Create Templates**
#### `product_list.html` (Displays All Products)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Products</title>
</head>
<body>
    <h1>Product List</h1>
    <a href="{% url 'product_create' %}">Create New Product</a>
    <ul>
        {% for product in products %}
        <li>
            {{ product.name }} - ${{ product.price }}
            <a href="{% url 'product_update' product.pk %}">Edit</a>
            <a href="{% url 'product_delete' product.pk %}">Delete</a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

#### `product_form.html` (Create & Update Form)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Product Form</title>
</head>
<body>
    <h1>{% if form.instance.pk %}Edit{% else %}Create{% endif %} Product</h1>
    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'product_list' %}">Back to List</a>
</body>
</html>
```

#### `product_confirm_delete.html` (Confirm Deletion)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Delete Product</title>
</head>
<body>
    <h1>Delete {{ product.name }}?</h1>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Confirm</button>
    </form>
    <a href="{% url 'product_list' %}">Cancel</a>
</body>
</html>
```

---

### **5. Add Django Admin Support**
```python
from django.contrib import admin
from .models import Product, Category, Tag

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
```

---

### **6. Run Migrations and Start the Server**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

This will set up a **fully functional CRUD system** for managing products in Django. 

### For using Differnet App | Like  | Category and Tags

Since `Category` and `Tag` will be handled in a separate Django app, let’s break this down step by step.

---

### **1. Create a New Django App for Categories and Tags**
Run the following command to create a new app (`categories`):

```bash
python manage.py startapp categories
```

This will create the necessary structure for the `categories` app.

---

### **2. Define Models for Category and Tag in `categories/models.py`**
```python
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
```

---

### **3. Create Forms in `categories/forms.py`**
```python
from django import forms
from .models import Category, Tag

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
```

---

### **4. Define Views for CRUD Operations in `categories/views.py`**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Tag
from .forms import CategoryForm, TagForm

# Category Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "category_form.html", {"form": form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "category_form.html", {"form": form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "category_confirm_delete.html", {"category": category})

# Tag Views
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "tag_list.html", {"tags": tags})

def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = TagForm()
    return render(request, "tag_form.html", {"form": form})

def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = TagForm(instance=tag)
    return render(request, "tag_form.html", {"form": form})

def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        return redirect("tag_list")
    return render(request, "tag_confirm_delete.html", {"tag": tag})
```

---

### **5. Configure URLs in `categories/urls.py`**
```python
from django.urls import path
from .views import (
    category_list, category_create, category_update, category_delete,
    tag_list, tag_create, tag_update, tag_delete
)

urlpatterns = [
    # Category URLs
    path("categories/", category_list, name="category_list"),
    path("categories/create/", category_create, name="category_create"),
    path("categories/update/<int:pk>/", category_update, name="category_update"),
    path("categories/delete/<int:pk>/", category_delete, name="category_delete"),

    # Tag URLs
    path("tags/", tag_list, name="tag_list"),
    path("tags/create/", tag_create, name="tag_create"),
    path("tags/update/<int:pk>/", tag_update, name="tag_update"),
    path("tags/delete/<int:pk>/", tag_delete, name="tag_delete"),
]
```

---

### **6. Register the New App in Django's `settings.py`**
Make sure `categories` is added to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "categories",  # Newly added app
]
```

---

### **7. Create Templates for Categories and Tags**
#### `category_list.html` (Displays All Categories)
```html
<h1>Categories</h1>
<a href="{% url 'category_create' %}">Add New Category</a>
<ul>
    {% for category in categories %}
        <li>
            {{ category.title }}
            <a href="{% url 'category_update' category.pk %}">Edit</a>
            <a href="{% url 'category_delete' category.pk %}">Delete</a>
        </li>
    {% endfor %}
</ul>
```

#### `category_form.html` (Create & Update Category)
```html
<h1>{% if form.instance.pk %}Edit{% else %}Create{% endif %} Category</h1>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
<a href="{% url 'category_list' %}">Back to List</a>
```

#### `category_confirm_delete.html` (Confirm Category Deletion)
```html
<h1>Delete {{ category.title }}?</h1>
<form method="POST">
    {% csrf_token %}
    <button type="submit">Confirm</button>
</form>
<a href="{% url 'category_list' %}">Cancel</a>
```

Similarly, create `tag_list.html`, `tag_form.html`, and `tag_confirm_delete.html` for the `Tag` model.

---

### **8. Run Migrations and Start the Server**
```bash
python manage.py makemigrations categories
python manage.py migrate
python manage.py runserver
```

---

### **9. Using These Models in the Product App**
To connect these models to the `Product` app (which already references `Category` and `Tag` as ForeignKey and ManyToMany relationships), **make sure to import them** in `products/models.py`:

```python
from categories.models import Category, Tag
```

---

### **Final Thoughts**
Now, `Category` and `Tag` live in a **separate app** and can be used independently while remaining integrated with `Product`. 🚀


