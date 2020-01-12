from dependency_injector import providers, containers

from app.network.network_manager import AppNetworkManager
from .hyperdrive_network_service import HyperDriveNetworkService


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class NetworkManager(containers.DeclarativeContainer):
    manager = providers.Singleton(AppNetworkManager, total=10, read=10, connect=7, backoff_factor=0.5)


class HyperDrive(containers.DeclarativeContainer):
    hyperdrive_network_service = providers.Singleton(HyperDriveNetworkService, network_manager=NetworkManager.manager(),
                                                     url="https://swapi.co/api/starships/")
