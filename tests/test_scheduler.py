import pytest
import time
from crawler_helper.scheduler import Scheduler, TimeUtils

global cnt

@Scheduler(block=True, trigger='interval', seconds=1, end_date=TimeUtils.nowDelta(10))
def block_job():
    global cnt
    cnt = cnt + 1

@Scheduler(block=False, trigger='interval', seconds=1, end_date=TimeUtils.nowDelta(10))
def nonblock_job():
    global cnt
    cnt = cnt + 1

class Test_scheduler():
    # def test_block_scheduler(self):
    #     self.cnt = 1
    #     block_job(self.cnt)
    #     assert(self.cnt == 10)
    
    def test_nonblock_scheduler(self):
        global cnt
        cnt = 1
        nonblock_job()
        time.sleep(10)
        assert(cnt == 10)