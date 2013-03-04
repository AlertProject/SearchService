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

from django.conf.urls.defaults import patterns, include, url

#from search.rest.api import IssueResource, CommitResource
#from search.rest.api import PersonResource, SearchResource

## Create resource to expose search results through API
#search_resource = SearchResource()
#issue_resource = IssueResource()
#commit_resource = CommitResource()
#person_resource = PersonResource()

# Specific URLs for search service

urlpatterns = patterns('',
    url(r'^query/', 'search.views.query_handler'),
    url(r'^test/query/$', 'search.views.query_test'),
    url(r'^test/$', 'search.views.test_form'),
    #url(r'^api/', include(person_resource.urls)),
    #url(r'^api/', include(commit_resource.urls)),
    #url(r'^api/', include(issue_resource.urls)),
    #url(r'^api/', include(search_resource.urls)),
    url(r'^$', 'search.views.search_form'),
)