from thirdpartydashboard.api.v1.system import SystemController
import pecan
from pecan import rest

class V1Controller(rest.RestController):
    @pecan.expose('json')
    def get(self):
        return {"version": "1.0.0"}

    systems = SystemController()
