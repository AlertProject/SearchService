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

class Product(Entity):
    def __init__(self, product_id, component_id, version):
        self._product_id = product_id
        self._component_id = component_id
        self._version = version
        
    @property
    def product_id(self):
        """Return ID of this Product."""
        return self._product_id
        
    @product_id.setter
    def product_id(self, product_id):
        """Set new ID for this Product."""
        self._product_id = product_id
        
    @property
    def component_id(self):
        """Return component ID for this Product."""
        return self._component_id
        
    @component_id.setter
    def component_id(self, component_id):
        """Change component_id for this Product."""
        self._component_id = component_id
        
    @property
    def version(self):
        """Return version of this Product."""
        return self._version
        
    @version.setter
    def version(self, version):
        """Set new version of this Product."""
        self._version = version