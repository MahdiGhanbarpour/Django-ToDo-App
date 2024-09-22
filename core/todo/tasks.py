from celery import shared_task


@shared_task
def delete_completed_tasks():
    from .models import Task

    Task.objects.filter(is_done=True).delete()
