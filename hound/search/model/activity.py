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
#          Luis Cañas-Díaz <lcanas@libresoft.es>

from entity import Entity

class Activity(Entity):
    """
    
    """
    
    def __init__(self, who, when, what, old_value, new_value):
        self.who = who
        self.when = when
        self.what = what
        self.old_value = old_value
        self.new_value = new_value
        