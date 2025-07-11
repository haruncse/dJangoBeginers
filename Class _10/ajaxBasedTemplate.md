
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