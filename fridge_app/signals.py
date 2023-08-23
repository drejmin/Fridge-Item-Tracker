from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from fridge_app.models import Reminder
from datetime import datetime
from .tasks import schedule_email
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

scheduler = BackgroundScheduler()
scheduler.start()

@receiver(pre_save, sender=Reminder)
def my_handler(sender, instance, **kwargs):
    job = ''

    # building date time in PST
    cst_tz = pytz.timezone('America/Los_Angeles')
    event_datetime = datetime.combine(instance.date, instance.time)
    specific_date_time = cst_tz.localize( event_datetime ) # Example date: August 22, 2023, 6:00 PM

    # building message with perishables

    if instance.task_id is None or not instance.task_id:
        job = scheduler.add_job(schedule_email, 'date', args=[instance.name, instance.description, instance.send_to_email], run_date=specific_date_time)
    else:
        if scheduler.get_job(instance.task_id):
            scheduler.remove_job(instance.task_id)
        job = scheduler.add_job(schedule_email, 'date', args=[instance.name, instance.description, instance.send_to_email], run_date=specific_date_time)
    job2 = scheduler.get_job(job_id=job.id)
    instance.task_id = job.id

@receiver(post_delete, sender=Reminder)
def my_handler(sender, instance, **kwargs):
    if scheduler.get_job(instance.task_id):
        scheduler.remove_job(instance.task_id)