# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from superset.superset_typing import CacheConfig
from superset.tasks.types import ExecutorType
from typing import  Callable
from dateutil import tz

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

from security import CustomSecurityManager
CUSTOM_SECURITY_MANAGER = CustomSecurityManager


logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

# Visual Customizations
APP_NAME = "Платформа аналитики ЦРЦЭ"
APP_ICON = "/static/assets/images/logo.png"
#APP_ICON_WIDTH = 100
# Path for routing when APP_ICON image is clicked
LOGO_TARGET_PATH = '/dashboard/list/' # Forwards to /superset/welcome/home
LOGO_TOOLTIP = "Центр развития цифровой экономики" # Text displayed when hovering.
LOGO_RIGHT_TEXT: Callable[[], str] | str = "Аналитическая Платформа"
FAVICONS = [{"href": "/static/assets/images/logo.png"}]


CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

MAPBOX_API_KEY = "pk.eyJ1IjoiaXRhcHBhcmF0IiwiYSI6ImNsMXVhOXJwMTA4YnczY21tczdmNG41c28ifQ.rNjd1zZfhPo0vpcon8kc9w"

class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        'superset.tasks.thumbnails',
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig


BABEL_DEFAULT_LOCALE = "ru"


HTML_SANITIZATION = False
CONTENT_SECURITY_POLICY_WARNING = False
TALISMAN_ENABLED = False

ENABLE_TEMPLATE_REMOVE_FILTERS = True

HTML_SANITIZATION_SCHEMA_EXTENSIONS = {
  "attributes": {
    "*": ["style","className"],
  },
  "tagNames": ["style"],
}



FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_RBAC": True,
    "GENERIC_CHART_AXES": True,
    #"LISTVIEWS_DEFAULT_CARD_VIEW": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_TEMPLATE_REMOVE_FILTERS": True,
    "DASHBOARD_CACHE": True,
    "UX_BETA": True,
    "TAGGING_SYSTEM": True,
    #"GLOBAL_ASYNC_QUERIES": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "DASHBOARD_FILTERS_EXPERIMENTAL": True,
    "RLS_IN_SQLLAB": True,
    "DRILL_TO_DETAIL": True,
    "ALLOW_ADHOC_SUBQUERY": True,
    "HORIZONTAL_FILTER_BAR": True,
    "RLS_FORM_QUERY_REL_FIELDS": True,
    "DASHBOARD_EDIT_CHART_IN_NEW_TAB": True,
    "DRILL_BY": True,
    "CACHE_QUERY_BY_USER": True,
}

THUMBNAIL_SELENIUM_USER = "admin"
THUMBNAIL_EXECUTE_AS = [ExecutorType.SELENIUM]

THUMBNAIL_CACHE_CONFIG: CacheConfig = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 24*60*60*7,
    'CACHE_KEY_PREFIX': 'thumbnail_',
    'CACHE_REDIS_URL': 'redis://redis:6379/1'
}


D3_FORMAT = {
    "decimal": ",",           # - decimal place string (e.g., ".").
    "thousands": "\u00a0",         # - group separator string (e.g., ",").
    "grouping": [3],          # - array of group sizes (e.g., [3]), cycled as needed.
    "currency": ["", "\u00a0\u20b8"]     # - currency prefix/suffix strings (e.g., ["$", ""])
}

D3_TIME_FORMAT = {
    'dateTime': '%A, %e %B %Y г. %X',
    'date': '%d.%m.%Y',
    'time': '%H:%M:%S',
    'periods': ['AM', 'PM'],
    'days': [
        'воскресенье',
        'понедельник',
        'вторник',
        'среда',
        'четверг',
        'пятница',
        'суббота',
    ],
    'shortDays': ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'],
    'months': [
        'январь',
        'февраль',
        'март',
        'апрель',
        'май',
        'июнь',
        'июль',
        'август',
        'сентябрь',
        'октябрь',
        'ноябрь',
        'декабрь',
    ],
    'shortMonths': [
        'янв',
        'фев',
        'мар',
        'апр',
        'май',
        'июн',
        'июл',
        'авг',
        'сен',
        'окт',
        'ноя',
        'дек',
    ]
}



CURRENCIES = ["USD", "EUR", "GBP", "INR", "MXN", "JPY", "CNY","KZT"]


SECRET_KEY = os.getenv("SECRET_KEY")

# Hide all users
def user_filter(query):
    from sqlalchemy.sql import false
    return query.filter(false())

EXTRA_RELATED_QUERY_FILTERS = {
    "user": user_filter,
}

ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"  # When using docker compose baseurl should be http://superset_app:8088/
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
