import celery
from celery import shared_task
from code_service.decorators import task_deduplicator
from code_service.logger.logging import setup_logger

from scrapper.entity_member_functions import YoutubeScrapperService

_module_name = __name__
log = setup_logger(_module_name)


class GeneralTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        log.critical(
            f"Error in task_id {exc} {task_id} {args} {kwargs} {einfo}", exc_info=True
        )


# celery commands
# $ celery -A code_service beat -l INFO
# $ celery -A code_service worker -B


@shared_task(default_retry_delay=30, base=GeneralTask)
def populate_youtube_data():
    log.info("cron ran")
    YoutubeScrapperService.store_youtube_results()


@shared_task(default_retry_delay=30, base=GeneralTask)
@task_deduplicator
def populate_youtube_data_helper():
    for i in range(0, 60, 10):
        populate_youtube_data.apply_async(countdown=i)
