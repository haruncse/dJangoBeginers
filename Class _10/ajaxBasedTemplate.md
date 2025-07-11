
### 🧩 Step-by-Step Guide: jQuery AJAX in Django Template with Bootstrap 5

#### 1. **Set Up Bootstrap 5 and jQuery in Your Template**
Include these in your base template:

```html
{% load static %}
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

You can also serve them from your static files if preferred.

📺 [How to use Bootstrap with Django](https://www.youtube.com/watch?v=SPGrc6byv_Y) shows how to properly include Bootstrap 5 in Django templates.

---

#### 2. **Create a Form in Your Template**
Use Bootstrap classes for styling:

```html
<form id="contactForm" method="POST">
  {% csrf_token %}
  <input type="text" name="name" class="form-control" placeholder="Your Name">
  <button type="submit" class="btn btn-primary mt-2">Submit</button>
</form>
<div id="responseMessage"></div>
```

---

#### 3. **Write the jQuery AJAX Script**
Place this at the bottom of your template:

```html
<script>
$(document).ready(function() {
  $('#contactForm').on('submit', function(e) {
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: "{% url 'contact_form' %}",
      data: $(this).serialize(),
      success: function(response) {
        $('#responseMessage').html('<div class="alert alert-success">Thanks, ' + response.name + '!</div>');
      },
      error: function(response) {
        $('#responseMessage').html('<div class="alert alert-danger">Something went wrong.</div>');
      }
    });
  });
});
</script>
```

📺 [Django AJAX Tutorial : Basic AJAX in Django app | Django ...](https://www.youtube.com/watch?v=QDdLvImfq_g) explains how to handle AJAX POST requests and CSRF tokens in Django.

---

#### 4. **Create the Django View**
In `views.py`:

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return JsonResponse({'name': name})
```

---

#### 5. **Use Bootstrap Modals with AJAX**
You can load content dynamically into modals:

```html
<!-- Trigger -->
<button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#infoModal">Open Modal</button>

<!-- Modal -->
<div class="modal fade" id="infoModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-body" id="modalContent">Loading...</div>
    </div>
  </div>
</div>

<script>
$('#infoModal').on('show.bs.modal', function () {
  $.get("{% url 'modal_content' %}", function(data) {
    $('#modalContent').html(data);
  });
});
</script>
```


To securely add a **CSRF token** in an AJAX request—especially in Django or Laravel—you’ll need to include the token in your request headers or form data. Here's a step-by-step guide tailored for both frameworks, plus video tutorials to reinforce each method.

---

### 🔐 Django: CSRF Token in AJAX

#### 1. **Include CSRF Token in Your Template**
Add this in your HTML `<head>`:

```html
<meta name="csrf-token" content="{{ csrf_token }}">
```

#### 2. **Set Up jQuery to Include the Token**
Use `$.ajaxSetup()` to automatically attach the token:

```javascript
$.ajaxSetup({
  headers: {
    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
  }
});
```

#### 3. **Make Your AJAX Request**
```javascript
$.ajax({
  type: 'POST',
  url: '/your-url/',
  data: { name: 'Harun' },
  success: function(response) {
    console.log('Success:', response);
  },
  error: function(error) {
    console.log('Error:', error);
  }
});
```

📺 [How To Use CSRF Token In AJAX Form Submission](https://www.youtube.com/watch?v=vLOe61zD620) clearly demonstrates how to include CSRF tokens in Django AJAX requests.

📺 [Django - AJAX Requests, HTMX & CSRF Tokens](https://www.youtube.com/watch?v=lc1sOvRaFpg) explains how CSRF tokens work with HTMX and jQuery in Django.

---

### 🛡️ Laravel: CSRF Token in AJAX

#### 1. **Add CSRF Token to Your HTML**
In your Blade template:

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

#### 2. **Configure jQuery to Use the Token**
```javascript
$.ajaxSetup({
  headers: {
    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
  }
});
```

#### 3. **Send AJAX POST Request**
```javascript
$.ajax({
  type: 'POST',
  url: '/your-laravel-route',
  data: { name: 'Harun' },
  success: function(response) {
    console.log('Success:', response);
  },
  error: function(error) {
    console.log('Error:', error);
  }
});
```
