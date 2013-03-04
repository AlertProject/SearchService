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
#          Luis Cañas <lcanas@libresoft.es>

from entity import Entity
from datetime import datetime

class Milestone(Entity):
    
    def __init__(self, id):
        self._id = id
        self._deadline = None
        
    @property
    def id(self):
        """Return ID of this Milestone."""
        return self._id
        
    @id.setter
    def id(self, id):
        """Set new ID for this Milestone."""
        self._id = id
        
    @property
    def deadline(self):
        """Return deadline of this Milestone."""
        return self._deadline
        
    @deadline.setter
    def deadline(self, deadline):
        """Set new deadline for this Milestone."""
        self._deadline = deadline