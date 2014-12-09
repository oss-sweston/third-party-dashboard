from api.v1.v1_controller import V1Controller
from thirdpartydashboard.api.v1.system import SystemsController

class RootController(object):
    v1 = V1Controller()
    systems = SystemsController()
