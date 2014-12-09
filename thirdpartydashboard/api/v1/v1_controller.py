import pecan
from pecan import rest

from thirdpartydashboard.api.v1.system import SystemController


class V1Controller(rest.RestController):
    @pecan.expose('json')
    def get(self):
        return {"version": "1.0.0"}

    systems = SystemController()
