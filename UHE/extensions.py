from celery import Celery
from flask_admin import Admin
from flask_allows import Allows
from flask_babelex import Babel
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis

from UHE.captcha.solver import Solver
from UHE.plugin_manager import PluginManager

# from UHE.schedule import clock

login_manager = LoginManager()

mail = Mail()

allows = Allows()

admin = Admin(name='SHUhelper pikachu', template_mode='bootstrap3')

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'UHE_',
                      'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/2'})

redis_store = FlaskRedis(decode_responses=True)

db = MongoEngine()

celery = Celery()

plugin_manager = PluginManager()

captcha_solver = Solver()

babel = Babel()




# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(5.0, clock.dalay('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
