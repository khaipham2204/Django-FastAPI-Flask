---

# Automatic Audit Logging with django-pgtrigger

This walkthrough demonstrates how to use `django-pgtrigger` to automatically audit changes to a model in Django.

---

### Step 1: Create the Main Model

Define the `Product` model and attach a trigger to log changes.

```python
import django_pgtrigger as pgtrigger
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        app_label = 'myapp'  # Change this to match your app name

    # Attach a trigger to log changes
    pgtrigger.register(
        pgtrigger.Trigger(
            name="audit_changes",
            operation=pgtrigger.Insert | pgtrigger.Update | pgtrigger.Delete,
            when=pgtrigger.After,
            func=pgtrigger.F(
                """
                INSERT INTO product_audit (product_id, action, old_data, new_data, changed_at)
                VALUES (
                    OLD.id, 
                    TG_OP, 
                    row_to_json(OLD), 
                    row_to_json(NEW), 
                    now()
                );
                """
            ),
        )
    )(locals())  # Register the trigger with the model
```

---

### Step 2: Create the Audit Table

Define the `ProductAudit` model to store audit logs.

```python
class ProductAudit(models.Model):
    product_id = models.IntegerField()
    action = models.CharField(max_length=10)  # INSERT, UPDATE, DELETE
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'myapp'
```

---

This setup ensures that any changes to the `Product` model (inserts, updates, or deletions) are automatically logged in the `ProductAudit` table. This is particularly useful for maintaining an audit trail in applications that require tracking historical changes.
