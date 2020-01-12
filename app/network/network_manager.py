import requests
from logger_library import Logger
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = Logger.app_logger().get_logger()


class AppNetworkManager:

    def __init__(self, total=10, read=10, connect=7, backoff_factor=0.5):
        retry = Retry(
            total=total,
            read=read,
            connect=connect,
            backoff_factor=backoff_factor
        )
        self.__session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry)
        self.__session.mount('http://', adapter)
        self.__session.mount('https://', adapter)

    def get_session(self):
        return self.__session
