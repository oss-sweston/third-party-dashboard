# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright 2013 Thierry Carrez <thierry@openstack.org>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
SQLAlchemy Models for storing storyboard
"""

from oslo.config import cfg
from oslo.db.sqlalchemy import models
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import Enum
from sqlalchemy.ext import declarative
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy import schema
from sqlalchemy import select
import sqlalchemy.sql.expression as expr
import sqlalchemy.sql.functions as func
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy_fulltext import FullText

import six.moves.urllib.parse as urlparse


CONF = cfg.CONF

def table_args():
    engine_name = urlparse.urlparse(cfg.CONF.database_connection).scheme
    if engine_name == 'mysql':
        return {'mysql_engine': cfg.CONF.mysql_engine,
                'mysql_charset': "utf8"}
    return None

## CUSTOM TYPES

# A mysql medium text type.
MYSQL_MEDIUM_TEXT = UnicodeText().with_variant(MEDIUMTEXT(), 'mysql')


class IdMixin(object):
    id = Column(Integer, primary_key=True)


class ThirdPartyDashboardBase(models.TimestampMixin,
                    IdMixin,
                    models.ModelBase):
    metadata = None

    @declarative.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

Base = declarative.declarative_base(cls=ThirdPartyDashboardBase)

class ModelBuilder(object):
    def __init__(self, **kwargs):
        super(ModelBuilder, self).__init__()

        if kwargs:
            for key in kwargs:
                if key in self:
                    self[key] = kwargs[key]

class System(FullText, ModelBuilder, Base):
    __tablename__ = "systems"

    __fulltext_columns__ = ['name']

    name = Column(Unicode(50))
    operator_id = Column(Integer, ForeignKey('operators.id'))
    events = relationship('SystemEvent', backref='system')

class SystemEvent(ModelBuilder, Base):
    __tablename__ = 'system_events'

    system_id = Column(Integer, ForeignKey('systems.id'))
    event_type = Column(Unicode(100), nullable=False)
    event_info = Column(UnicodeText(), nullable=True)

class Operator(ModelBuilder, Base):
    __tablename__ = "operators"

    operator_name = Column(Unicode(50))
    operator_email = Column(Unicode(50))
    systems = relationship('System', backref='operator')
