# Copyright (c) 2014 Triniplex.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo.config import cfg
from pecan import expose
from pecan import request
from pecan import response
from pecan import rest
from pecan.secure import secure
from wsme.exc import ClientSideError
import wsmeext.pecan as wsme_pecan

#from thirdpartydashboard.api.auth import authorization_checks as checks
from thirdpartydashboard.api.v1.search import search_engine
#from thirdpartydashboard.api.v1.system_event import SystemEventsController
from thirdpartydashboard.api.v1 import wmodels
from thirdpartydashboard.db.api import systems as systems_api
#from thirdpartydashboard.db.api import timeline_events as events_api


CONF = cfg.CONF

SEARCH_ENGINE = search_engine.get_engine()


class SystemsController(rest.RestController):
    """Manages operations on systems."""

    _custom_actions = {"search": ["GET"]}

    #@secure(checks.guest)
    @wsme_pecan.wsexpose(wmodels.System, int)
    def get_one(self, system_id):
        """Retrieve details about one system.

        :param system_id: An ID of the system.
        """
        system = systems_api.system_get_simple(system_id)

        if system:
            return wmodels.System.from_db_model(system)
        else:
            raise ClientSideError("System %s not found" % system_id,
                                  status_code=404)

    #@secure(checks.guest)
    @wsme_pecan.wsexpose([wmodels.System], unicode, unicode, [unicode], int,
                         int, int, int, int, unicode, unicode)
    def get_all(self, name=None, marker=None, limit=None, sort_field='id', sort_dir='asc'):
        """Retrieve definitions of all of the systems.

        :param name: A string to filter the name by.
        """

        # Boundary check on limit.
        if limit is None:
            limit = CONF.page_size_default
        limit = min(CONF.page_size_maximum, max(1, limit))

        # Resolve the marker record.
        marker_system = systems_api.system_get_simple(marker)

        systems = systems_api \
            .system_get_all(name=name,
                           marker=marker_system,
                           limit=limit, sort_field=sort_field,
                           sort_dir=sort_dir)
        system_count = systems_api \
            .system_get_count(name=name)

        # Apply the query response headers.
        response.headers['X-Limit'] = str(limit)
        response.headers['X-Total'] = str(system_count)
        if marker_system:
            response.headers['X-Marker'] = str(marker_system.id)

        return [wmodels.System.from_db_model(s) for s in systems]

    #@secure(checks.guest)
    @wsme_pecan.wsexpose([wmodels.System], unicode, unicode, int, int)
    def search(self, q="", marker=None, limit=None):
        """The search endpoint for systems.

        :param q: The query string.
        :return: List of Systems matching the query.
        """

        systems = SEARCH_ENGINE.systems_query(q=q,
                                              marker=marker,
                                              limit=limit)

        return [wmodels.System.from_db_model(system) for system in systems]

    @expose()
    def _route(self, args, request):
        if request.method == 'GET' and len(args) > 0:
            # It's a request by a name or id
            something = args[0]

            if something == "search":
                # Request to a search endpoint
                return self.search, args

        return super(SystemsController, self)._route(args, request)
