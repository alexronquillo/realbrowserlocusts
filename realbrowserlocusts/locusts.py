# pylint:disable=too-few-public-methods
""" Combine User with Selenium Web Driver """
import logging
from os import getenv as os_getenv
from locust import User
from locust.exception import LocustError
from selenium import webdriver
from realbrowserlocusts.core import RealBrowserClient

_LOGGER = logging.getLogger(__name__)


class RealBrowserLocust(User):
    """
    This is the abstract User class which should be subclassed.
    """
    abstract = True

    client = None
    timeout = 30
    screen_width = None
    screen_height = None

    def __init__(self, environment):
        super(RealBrowserLocust, self).__init__(environment)
        self.proxy_server = os_getenv("LOCUST_BROWSER_PROXY", None)


class ChromeLocust(RealBrowserLocust):
    """
    Provides a Chrome webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(ChromeLocust, self).__init__()
        options = webdriver.ChromeOptions()
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
        self.client = RealBrowserClient(
            webdriver.Chrome(chrome_options=options),
            self.timeout,
            (self.screen_width, self.screen_height),
        )


class HeadlessChromeLocust(RealBrowserLocust):
    """
    Provides a headless Chrome webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(HeadlessChromeLocust, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size={}x{}'.format(
            self.screen_width, self.screen_height
        ))
        options.add_argument('disable-gpu')
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
        driver = webdriver.Chrome(chrome_options=options)
        _LOGGER.info('Actually trying to run headless Chrome')
        self.client = RealBrowserClient(webdriver.Chrome(options=options), self.timeout)


class FirefoxLocust(RealBrowserLocust):
    """
    Provides a Firefox webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(FirefoxLocust, self).__init__()
        self.client = RealBrowserClient(
            webdriver.Firefox(),
            self.timeout,
            (self.screen_width, self.screen_height),
        )


class PhantomJSLocust(RealBrowserLocust):
    """
    Provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    def __init__(self):
        super(PhantomJSLocust, self).__init__()
        self.client = RealBrowserClient(
            webdriver.PhantomJS(),
            self.timeout,
            (self.screen_width, self.screen_height),
        )
