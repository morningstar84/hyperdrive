from flask import Blueprint

hyperdrive = Blueprint('hyperdrive', __name__)

from . import views