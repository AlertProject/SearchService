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
# 
# hound/search/rest/api.py

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from search.models  import Issue, Commit, Person

#class SimpleTest(TestCase):
    #def test_basic_addition(self):
        #"""
        #Tests that 1 + 1 always equals 2.
        #"""
        #self.assertEqual(1 + 1, 2)

# Some dummy values to populate DB

p1 = Person.objects.create(name = 'Luis Mendoza', email = 'lmendoza@foo.bar',
                           user_id = 1)
p2 = Person.objects.create(name = 'Pedro Roderas', email = 'proder@foo.bar', 
                           user_id = 2)
pR = Person.objects.create(name = 'Fausto Melas', email = 'fmelas@foo.bar',
                           user_id = 3)

c1 = Commit.objects.create(author = p1, committer = p1)
c2 = Commit.objects.create(author = p2, committer = p2)
c3 = Commit.objects.create(author = p1, committer = p1)

i1 = Issue.objects.create(issue_id = '001', reporter = pR)
i2 = Issue.objects.create(issue_id = '002', reporter = pR)
i3 = Issue.objects.create(issue_id = '003', reporter = pR)
i4 = Issue.objects.create(issue_id = '004', reporter = pR)

i1.assigned_to.add(p1)
i2.assigned_to.add(p1)
i3.assigned_to.add(p1)
i4.assigned_to.add(p1)
i1.rel_commits.add(c1)
i2.rel_commits.add(c2)
i3.rel_commits.add(c1)
i3.rel_commits.add(c3)
