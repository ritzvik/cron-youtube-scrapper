from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from code_service.utils.datetime_utils import get_present_datetime_in_utc


class _BaseQueryset(QuerySet):

    def update(self, **kwargs):
        if kwargs and isinstance(kwargs, dict):
            kwargs.update({"modified_at": get_present_datetime_in_utc()})
        return super().update(**kwargs)


class BaseModelManager(BaseManager.from_queryset(_BaseQueryset)):
    pass


class BaseModel(models.Model):
    created_on = models.DateTimeField(db_index=False, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True


class BigIDAbstract(BaseModel):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True
