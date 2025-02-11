from celery import shared_task
from .models import Duty


@shared_task
def delete_done_duties():
    # select done duties (task) and delete them
    done_duties = Duty.objects.filter(done_status="don")
    done_duties.delete()
    print("Done duties deleted")
