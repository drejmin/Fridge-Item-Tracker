from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from fridge_app.models import Reminder
from datetime import datetime
from .tasks import schedule_email
from apscheduler.schedulers.background import BackgroundScheduler
from django.template.loader import render_to_string
import pytz, os

scheduler = BackgroundScheduler()
scheduler.start()

@receiver(post_save, sender=Reminder)
def my_handler(sender, instance, **kwargs):
    job = None
    reminder = Reminder.objects.get(id=instance.id)

    # building date time in PST
    cst_tz = pytz.timezone('America/Los_Angeles')
    event_datetime = datetime.combine(instance.date, instance.time)
    specific_date_time = cst_tz.localize( event_datetime ) # Example date: August 22, 2023, 6:00 PM

    # building message with perishables
    message = instance.description
    html_message = render_to_string('reminder_email_template.html', {'reminder': reminder, 'BASE_URL': os.environ['BASE_URL']})

    if instance.task_id is None or not instance.task_id:
        job = scheduler.add_job(schedule_email, 'date', args=[instance.name, message, html_message, instance.send_to_email], run_date=specific_date_time)
    else:
        if scheduler.get_job(instance.task_id):
            scheduler.remove_job(instance.task_id)
        job = scheduler.add_job(schedule_email, 'date', args=[instance.name, message, html_message, instance.send_to_email], run_date=specific_date_time)

    instance.task_id = job.id

@receiver(post_delete, sender=Reminder)
def my_handler(sender, instance, **kwargs):
    if scheduler.get_job(instance.task_id):
        scheduler.remove_job(instance.task_id)