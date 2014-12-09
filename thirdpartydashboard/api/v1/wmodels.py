from datetime import datetime
from wsme import types as wtypes
from api.v1 import base

class System(base.APIBase):
    """Represents the ci systems for the dashboard
    """

    name = wtypes.text
    """The system name"""

    @classmethod
    def sample(cls):
        return cls(
            version="338c2d6")

class SystemEvent(base.APIBase):
    event_type = wtypes.text
    event_info = wtypes.text

class Operator(base.APIBase):
    operator_name = wtypes.text
    operator_email = wtypes.text
