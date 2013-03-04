# -*- coding: utf8 -*-
#
# Hound: Search service
# Copyright (C) 2012  GSyC/LibreSoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Felipe Ortega <jfelipe@libresoft.es>
#          Santiago Dueñas <sduenas@libresoft.es>

from entity import Entity

class SearchQuery(Entity):
    """
    Encapsulates search queries from the search UI
    """
    
    def __init__(self, query_id, query_fields):
        self._query_id = query_id
        # Dictionary to store fields provided with this query
        self._query_fields = query_fields
        
    @property
    def query_id(self):
        #print "Hello from the getter"
        return self._query_id
        
    @query_id.setter
    def query_id(self, value):
        #print "Hello from the setter"
        self._query_id = value
        
    @property
    def query_fields(self):
        return self._query_fields
        