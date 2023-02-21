from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .logger import CH_LOGGER
import datetime, time
from functools import wraps

TRIGGERS = ['date', 'interval', 'cron']

class _Undefined(object):
    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '<undefined>'


undefined = _Undefined()  #: a unique object that only signifies that no value is defined

class Scheduler():
    def __init__(self, block=False, trigger='date', id=None, name=None, **trigger_args):
        self.block = block
        self.trigger = trigger
        self.id = id
        self.name = name
        self.trigger_args = trigger_args

    def __call__(self, func):
        CH_LOGGER.debug("ready to decorate")
        if self.trigger not in TRIGGERS:
            CH_LOGGER.error(f"triggers only support: {TRIGGERS}")
        @wraps(func)
        def wrap(*args, **kwargs):
            if self.block:
                CH_LOGGER.debug("initializing blocking scheduler")
                sche = BlockingScheduler()
                sche.add_job(func, self.trigger, args, kwargs, self.id, self.name,
                                **self.trigger_args)
                sche.start()
                CH_LOGGER.debug("blocking scheduler started")
            else:
                CH_LOGGER.debug("initializing background scheduler")
                sche = BackgroundScheduler()
                sche.add_job(func, self.trigger, args, kwargs, self.id, self.name,
                                **self.trigger_args)
                sche.start()
                CH_LOGGER.debug("blocking scheduler started")
        return wrap


class TimeUtils():
    @classmethod
    def getToday(cls) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def getTomorrow(cls) -> str:
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")

    @classmethod
    def now(cls) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def nowDelta(cls,seconds=0) -> str:
        now = datetime.datetime.now()
        then = now + datetime.timedelta(seconds=seconds)
        return then.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def isLater(cls, time, other) -> bool:
        if time < other:
            return False
        else:
            return True