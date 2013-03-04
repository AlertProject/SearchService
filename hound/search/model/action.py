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
from file import File

class Action(Entity):
    """
    This abstract class represents the different actions performed in
    every commit.
    
    In systems like CVS, where the commit is limited to a single
    file, there will be only one action per commit. However, most of
    the version control systems support atomic commits, where several
    actions are carried out on several files.
    
    Keep in mind that the type of the actions are specific for each
    SCM solution. Though some of them are common such as 'add',
    'delete' or 'modify', others are just available on a
    type of repository, like 'replace' for the SVN solution.
    """
    
    def __init__(self, theFile):
        self._theFile = theFile
        
    
    def _get_file(self):
        return self._theFile