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

from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.serializers import Serializer

#from search.model.issue import Issue
#from search.model.commit import Commit
#from search.model.person import Person

from search.models import Issue, Commit, Person, SearchResult

sr_1 = SearchResult(1, "first result")
sr_2 = SearchResult(2, "second result")
sr_3 = SearchResult(3, "third result")

data = { 1: sr_1, 2: sr_2, 3: sr_3 }

class PersonResource(ModelResource):
    class Meta:
        # List of all objects to be displayed in base URL
        queryset = Person.objects.all()
        # Resource name mapped to URL
        resource_name = 'person'
        # Fields to be excluded from data returned to client

class CommitResource(ModelResource):
    class Meta:
        # List of all objects to be displayed in base URL
        queryset = Commit.objects.all()
        # Resource name mapped to URL
        resource_name = 'commit'
        # Fields to be excluded from data returned to client
    
    author = fields.ToOneField(PersonResource, 'author', full = False)
    committer = fields.ToOneField(PersonResource, 'committer', full = False)
        
class IssueResource(ModelResource):
    class Meta:
        # List of all objects to be displayed in base URL
        queryset = Issue.objects.all()
        # Resource name mapped to URL
        resource_name = 'issue'
        # Fields to be excluded from data returned to client
        
    assigned_to = fields.ManyToManyField(PersonResource, 'assigned_to', 
                                         full = False)
    reporter = fields.ToOneField(PersonResource, 'reporter', full = False)
    rel_commits = fields.ManyToManyField(CommitResource, 'rel_commits',
                                         full = False)

# Still a dummy implementation to test API behavior on plain Resource class
class SearchResource(Resource):
    # Fields that we are going to handle via the API
    # These fields must mimic attributes in target model class (Topo in this
    # case)
    uuid = fields.IntegerField(attribute = 'uuid')
    desc = fields.CharField(attribute = 'desc')
    
    # Meta info for Resource
    class Meta:
        resource_name = 'search'
        object_class = SearchResult
        #authorization = Authorization()
    
    # The following methods will need overriding regardless of your
    # data source.
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
        
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid # pk is referenced in ModelResource
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)
    
    def get_object_list(self, request):
        # Here we must retrieve results from other data source
        return data.values()
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)
        
    def obj_get(self, request=None, **kwargs):
        pk = int(kwargs['pk'])
        try:
            return data[pk]
        except KeyError:
            raise NotFound("Object not found")
        