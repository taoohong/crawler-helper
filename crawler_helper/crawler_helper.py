from enum import Enum
from selenium import webdriver
from retrying import retry
import os
import requests
from .logger import CH_LOGGER
from excel_writer import ExcelWriter


class CrawlerType(Enum):
    """
    CrawlerHelper work type
    DIRECT: Use http requests to get the results directly
    SIMULATE: Use Chrome driver and Selenium to simulate human
    operations to get the results.
    """
    DIRECT = 1

    SIMULATE = 2


class CrawlerHelper():
    DEFAULT_RESULT_PATH = "result.xslx"
    DEFAULT_ROOT_DIR = os.path.join(os.getcwd(), "result")

    def __init__(self, type=CrawlerType.DIRECT,  root_dir=DEFAULT_ROOT_DIR):
        self.excel_writer_dic = {}
        if type == CrawlerType.SIMULATE:
            self.driver = self.__init_chrome_driver()
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        self.root_dir = root_dir

    def __init_chrome_driver(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            'useAutomationExtension', False)
        chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        chrome_options.add_argument(
            "disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=chrome_options)
        return driver


    def __result(self, result):
        CH_LOGGER.debug(result)
        return result is None

    @retry(stop_max_attempt_number=5, wait_random_min=500, wait_random_max=1000, retry_on_result=__result)
    def send_get_request(self, url, cookies=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        try:
            ret = requests.get(url, cookies=cookies, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as errh:
            CH_LOGGER.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            CH_LOGGER.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            CH_LOGGER.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            CH_LOGGER.error("OOps: Something Else", err)
        else:
            return ret

    def add_excel_writer(self, excel_writer_name, columns_list) -> ExcelWriter:
        if excel_writer_name in self.excel_writer_dic.keys:
            CH_LOGGER.error("this excel write name has existed")
        excel_writer = ExcelWriter(self.root_dir, excel_writer_name)
        excel_writer.init_sheet(columns_list)
        self.excel_writer_dic[excel_writer_name] = excel_writer
        return excel_writer

    def remove_excel_writer(self, excel_writer_name):
        if excel_writer_name not in self.excel_writer_dic.keys:
            CH_LOGGER.error("this excel write does not existed")
        self.excel_writer_dic[excel_writer_name].close()
        self.excel_writer_dic.pop(excel_writer_name)
