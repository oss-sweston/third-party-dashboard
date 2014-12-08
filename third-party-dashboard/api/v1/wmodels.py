from datetime import datetime
from wsme import types as wtypes
from api.v1 import base

class Systems(base.APIBase):
    """Represents the ci systems for the dashboard
    """

    name = wtypes.text
    """The system name"""

    operator_id = int
    """ID of the operator associated with the system"""

    @classmethod
    def sample(cls):
        return cls(
            version="338c2d6")

class SystemEvent(base.APIBase):
    event_type = wtypes.text
    event_info = wtypes.text
    system_id = int
