Some key features:
Declarative trigger definition using Python classes.
Supports common trigger operations like INSERT, UPDATE, and DELETE.
Allows conditional triggers using Django's ORM-like expressions.
Integrates well with Django's migration system.

Step 1: Install django-pgtrigger
pip install django-pgtrigger

Step 2: Define a Model with a Trigger
import django_pgtrigger as pgtrigger
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    class Meta:
        app_label = 'myapp'  # Change this to match your app name

    # Attach a trigger to prevent updates on soft-deleted records
    pgtrigger.register(
        pgtrigger.Protect(
            name="prevent_update_if_deleted",
            operation=pgtrigger.Update,
            condition=pgtrigger.Q(old__is_deleted=True),
        )
    )(locals())  # Register the trigger with the model

Step 3: Run Migrations
python manage.py makemigrations
python manage.py migrate

How It Works
If is_deleted=True, any attempt to update the record will be blocked.
If is_deleted=False, updates are allowed as usual.
