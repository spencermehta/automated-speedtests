from celery import shared_task


@shared_task
def sample_task():
    print("The sample task just ran.")


@shared_task
def custom_command():
    call_command("myCustomCommand", )