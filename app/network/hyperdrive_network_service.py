import json
from typing import Optional, List

from logger_library import Logger

from .model import StarShipsList, Ship

logger = Logger.app_logger().get_logger()


class HyperDriveNetworkService:

    def __init__(self, network_manager, url):
        self.url = url
        self.network_manager = network_manager

    def get_starship_list(self):
        return self.__get_starships__(self.url)

    def __get_starships__(self, next_page) -> Optional[List[Ship]]:
        try:
            if next_page is None:
                return []
            page = self.get_starship_page(next_page)
            return page.results + self.__get_starships__(page.next)
        except Exception as e:
            logger.error("Error while fetching ships", e)
            raise Exception("Could not download all ships pages")

    def get_starship_page(self, page_url) -> Optional[StarShipsList]:
        try:
            payload = {}
            headers = {}
            response = self.network_manager.get_session().get(page_url, headers=headers, data=payload)
            result = json.loads(response.text.encode('utf8'))
            starship_list = StarShipsList.from_dict(result)
            return starship_list
        except Exception as e:
            logger.error("Error while downloading starship list", e)
        return None

