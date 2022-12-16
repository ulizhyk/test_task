"""Usage related tasks"""
import datetime
import uuid

from celery.utils.log import get_task_logger
from flask import current_app

from src.celery_app import celery
from src.models.base import db
from src.models.service_codes import ServiceCode, ServiceCodeVersions, Plan
from src.models.subscriptions import Subscription, SubscriptionStatus
from src.models.usages import DataUsage

log = get_task_logger(__name__)


@celery.task()
def monitor_usage_for_data_blocks():
    """Add google style doc string here

    (https://www.sphinx-doc.org/en/1.7/ext/example_google.html)

    """
    subscription_version_date = ''

    data_usages = DataUsage.query.all()
    blocking_service_code = ServiceCode.get_data_blocking_code()
    subscriptions = Subscription.query.join(Plan).filter(
        Subscription.service_codes,
        Subscription.status == SubscriptionStatus.active,
        Plan.is_unlimited == False
    ).all()

    for s in subscriptions:
        for service_code in s.service_codes:
            if service_code.name == blocking_service_code.name:

                subscription_version_date = ServiceCodeVersions.query.filter(
                    ServiceCodeVersions.status == 'added',
                    ServiceCodeVersions.service_code_id == service_code.id,
                    ServiceCodeVersions.subscription_id == s.id
                ).first().from_date

    if subscription_version_date:
        list_ids = [data.subscription_id for data in data_usages if data.from_date <= subscription_version_date <= data.to_date]

        return list_ids

    return []
