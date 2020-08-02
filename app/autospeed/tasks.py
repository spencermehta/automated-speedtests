from celery import shared_task, signals
from django.core.management import call_command # NEW

@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass

@shared_task
def sample_task():
    print("The sample task just ran.")


@shared_task
def custom_command():
    call_command("myCustomCommand", )

@shared_task
def run_speed_test():
    call_command("run_speed_test", )