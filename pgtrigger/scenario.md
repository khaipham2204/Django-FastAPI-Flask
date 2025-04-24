Scenario: Insert into Model A → Update Model B → If Condition Fails, Send Notification
1.Use a Django trigger (django-pgtrigger) to automatically update Model B when Model A is inserted.
2.Use a Django signal (post_save) to check Model B's condition and send a notification if it fails.

# Define Models (A & B)
import django_pgtrigger as pgtrigger
from django.db import models

class ModelA(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    class Meta:
        app_label = 'myapp'

class ModelB(models.Model):
    model_a = models.OneToOneField(ModelA, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('good', 'Good'), ('bad', 'Bad')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'myapp'
        
# Use a Trigger to Auto-Update Model B
We create a trigger that inserts/updates Model B automatically when a new record is added to Model A.
pgtrigger.register(
    pgtrigger.Trigger(
        name="update_model_b_on_insert_a",
        operation=pgtrigger.Insert,
        when=pgtrigger.After,
        func=pgtrigger.F(
            """
            INSERT INTO myapp_modelb (model_a_id, status, created_at)
            VALUES (NEW.id, 'good', now())
            ON CONFLICT (model_a_id) 
            DO UPDATE SET status = 'good';
            """
        ),
    )
)(locals())  # Attach trigger to ModelA

# Use a Django Signal to Check Model B and Send a Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=ModelB)
def check_model_b_status(sender, instance, **kwargs):
    if instance.status == 'bad':  # Condition check
        send_mail(
            subject="Alert: Model B Status is Bad!",
            message=f"Warning: ModelB linked to ModelA ID {instance.model_a_id} has a bad status.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['admin@example.com'],
        )
