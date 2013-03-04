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

class ComputerSystem(Action):
    def __init__(self, platform, os):
        self._platform = platform
        self._os = os
    
    @property
    def platform(self):
        """Return platform name"""
        return self._platform
        
    @platform.setter
    def platform(self, platform):
        self._platform = platform
        
    @property
    def os(self):
        """Return os name"""
        return self._os
        
    @os.setter
    def os(self, os):
        self._os = os