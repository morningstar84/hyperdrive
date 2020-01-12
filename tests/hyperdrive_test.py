import os
import unittest
from random import randint
from unittest.mock import patch

from faker import Faker
from nose.tools import assert_is_not_none

from app import create_app
from app.hyperdrive.views import index
from app.network import Ship


class HyperDriveTest(unittest.TestCase):

    def setUp(self):
        os.environ["FLASK_ENV"] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.network.HyperDriveNetworkService')
    def test_hyperdrive(self, hyperdrive_mock):
        hyperdrive_mock.get_starship_list.return_value = HyperDriveTest.__generate_fake_ship_list__(2, 2)
        response = index(hyperdrive_mock)
        assert_is_not_none(response)
        assert response.status_code == 200

    @patch('app.network.HyperDriveNetworkService')
    def test_hyperdrive_network_error(self, hyperdrive_mock):
        hyperdrive_mock.get_starship_list.side_effect = Exception("Network error simulation")
        response = index(hyperdrive_mock)
        assert_is_not_none(response)
        assert response.status_code == 503

    @patch('app.network.HyperDriveNetworkService')
    def test_hyperdrive_ship_count(self, hyperdrive_mock):
        hyper_count = randint(0, 50)
        no_hyper_count = randint(0, 50)
        hyperdrive_mock.get_starship_list.return_value = HyperDriveTest.__generate_fake_ship_list__(hyper_count,
                                                                                                    no_hyper_count)
        response = index(hyperdrive_mock)
        assert_is_not_none(response)
        assert response.status_code == 200
        assert len(response.json['starships']) == hyper_count
        assert len(response.json['starships_unknown_hyperdrive']) == no_hyper_count

    @staticmethod
    def __generate_fake_ship_list__(hyper_number: int, no_hyper_number: int) -> [Ship]:
        result = []
        for i in range(0, hyper_number):
            ship = HyperDriveTest.__create_fake_ship__()
            result.append(ship)

        for i in range(0, no_hyper_number):
            ship = HyperDriveTest.__create_fake_ship__(False)
            result.append(ship)
        return result

    @staticmethod
    def __create_fake_ship__(has_hyperdrive=True):
        fake = Faker()
        result = {
            "name": fake.name(),
            "model": fake.name(),
            "manufacturer": fake.name(),
            "cost_in_credits": fake.name(),
            "length": fake.name(),
            "max_atmosphering_speed": fake.name(),
            "crew": fake.name(),
            "passengers": fake.name(),
            "cargo_capacity": fake.name(),
            "consumables": fake.name(),
            "hyperdrive_rating": fake.pyfloat() if has_hyperdrive else None,
            "MGLT": fake.name(),
            "pilots": [],
            "films": [],
            "starship_class": fake.name(),
            "created": fake.iso8601(),
            "edited": fake.iso8601()
        }
        return Ship.from_dict(result)
