import os
from celery import Celery
from celery.schedules import crontab
from todo.tasks import delete_completed_tasks

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/10"),
        delete_completed_tasks.s(),
        name="Delete completed tasks every 10 minutes",
    )
