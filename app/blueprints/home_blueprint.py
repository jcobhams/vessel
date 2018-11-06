from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.home_controller import HomeController

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
home_blueprint = Blueprint('home', __name__, url_prefix=url_prefix)

home_controller = HomeController(request)

@home_blueprint.route('/', methods=['GET'])
def homepage():
	return home_controller.home_page()

	