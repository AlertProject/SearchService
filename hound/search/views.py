#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Hound: Search service
# Copyright (C) 2012  GSyC/LibreSoft, Universidad Rey Juan Carlos
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
# 


# Create your views here.
from django.forms.widgets import RadioSelect
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django import forms
from event_composer import EventComposer
from settings import BUS_URL

from StringIO import StringIO
import json


class JSONPCallback(object):
    """This decorator function wraps a normal view function
    so that it can be read through a jsonp callback.

    Usage:

    @JSONPCallback                                                                                                                          
    def my_view_function(request):
        return HttpResponse('this should be viewable through jsonp')

    It looks for a GET parameter called "callback", and if one exists,
    wraps the payload in a javascript function named per the value of callback.
    If the input does not appear to be json, wrap the input in quotes
    so as not to throw a javascript error upon receipt of the response.

    Based on cominatchu's code (http://djangosnippets.org/snippets/2208/)
    """
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        request = args[0]
        response = self.f(*args, **kwargs)

        # if callback parameter is present,
        # this is going to be a jsonp callback.
        callback = request.GET.get('callback')       
        if callback:
            if response.content[0] not in ['"', '[', '{'] \
                    or response.content[-1] not in ['"', ']', '}']:
                response.content = '"%s"' % response.content
            response.content = "%s(%s)" % (callback, response.content)
            response['Content-Type'] = 'application/javascript'

        return response

class SearchForm(forms.Form):
    PROJECT_CHOICES = (('solid','Solid (KDE)'),
                      )
    project = forms.ChoiceField(choices = PROJECT_CHOICES)
    #project = forms.CharField()
    issue_id = forms.CharField(widget = forms.TextInput(attrs={'oninput':'OnInput (event);DisableRight (event)'}))
    
    I_OPTIONS = (('sug','Get suggested assignee'),
                 ('sim','Find similar issues'),
                 ('ext','Display extended issue view'),
                )
    issue_option = forms.ChoiceField(widget=RadioSelect(attrs={'enabled':'enabled'}),
                                     choices = I_OPTIONS)
    
    commit_uri = forms.CharField(widget = forms.TextInput(attrs={'oninput':'OnInput (event);DisableRight (event)'}))
    
    C_OPTIONS = (('info','Get info for a commit'),
                 ('prod','Find all commits related to a product'),
                )
    commit_option = forms.ChoiceField(widget=RadioSelect(attrs={'enabled':'enabled'}),
                            choices = C_OPTIONS)
    
    product = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'oninput':'DisableLeft (event)'}))
                               
    method_uri = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'oninput':'DisableLeft (event)'}))
                               
    from_date = forms.DateField(required = False,
                            widget = forms.DateInput(attrs={'oninput':'DisableLeft (event)'}))
    
    to_date = forms.DateField(required = False,
                            widget = forms.DateInput(attrs={'oninput':'DisableLeft (event)'}))
    
    keywords = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'oninput':'DisableLeft (event)'}))

    developer = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'oninput':'DisableLeft (event)'}))
    
def search_form(request):
    #if request.method == 'POST': # If the form has been submitted...
        #form = SearchForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            ## Process the data in form.cleaned_data
            ##name = form.cleaned_data['name']
            ##surname = form.cleaned_data['surname']
            
            ## Also forward csrf context info
            ##return render_to_response('characters/contact.html', 
                                      ##{'name': name, 'surname': surname}, 
                                      ##context_instance = c)
            ##return render_to_response('characters/contact.html', 
                                      ##{'name': name, 'surname': surname})
            
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
    #else:
    form = SearchForm() # An unbound form

    return render_to_response('search_form.html', {
        'form': form,
    })
    
def test_form(request):
    """
    Form for testing search API
    """

    form = SearchForm()
    
    return render_to_response('search_test.html', {
        'form': form,
    })

@JSONPCallback
def query_test(request):
    """
    Test method for REST API
    http://127.0.0.1:8000/hound/search/query/?issue_id=1&project=kde
    &keywords=hola,adios,tururu&commit_id=123&component=solid
    &start_date=20100901&end_date=20110901
    """
    
    deserial_test = EventComposer()
    
    if request.method == 'GET':
        
        query = request.GET
        
        if 'commit_option' in query:
            
            if (query['commit_option'] == 'info'):
                if 'commit_uri' in query and query['commit_uri'] != '':
                    print "Case commit.getInfo"
                    data = deserial_test.deserial_metadata('commit.getInfo',
                                'templates/events/metadata-commit.getInfo.xml')
                                
                else:
                    return HttpResponse("You must provide the commit URI")
                
            elif (query['commit_option'] == 'prod'):
                if 'product' in query and query['product'] != '':
                    # Case of retrieving all commits related to a method
                    # To: Metadata service
                    print "Case commit.getAllForProduct"
                    data = deserial_test.deserial_metadata('commit.getAllForProduct',
                        'templates/events/metadata-commit.getAllForProduct.xml')
                else:
                    return HttpResponse("You must provide a product name.")
                        
        elif ('issue_id' in query and query['issue_id'] != ''):
            
            if ('issue_option' in query and query['issue_option'] != ''):
                if (query['issue_option'] == 'sug'):
                    # Case of suggesting developers for an issue
                    # To: Recommendation service
                    print "Case Recommender.identity.Recommendation"
                    data = deserial_test.deserial_recommendation('identity.Recommendation',
                            'templates/events/recommender-IdentityRecommendation.xml')
                
                elif (query['issue_option'] == 'sim'):
                    # Case of finding related issues
                    # To: KEUI
                    print "Case KEUI-similarThreads"
                    data = deserial_test.deserial_keui('similarThreads',
                                    'templates/events/KEUI-similarThreads.xml')
                
                elif (query['issue_option'] == 'ext'):
                    # Case of presented extended info about issue
                    # To: Metadata service
                    print "Case issue.getInfo"
                    data = deserial_test.deserial_metadata('issue.getInfo',
                                    'templates/events/metadata-issue.getInfo.xml')
                                   
            else:
                return HttpResponse("You must select an issue option for this particular ID.")
                                        
        elif 'product' in query and query['product'] != '':
            # Case of getting all issues for a product
            # To: Metadata service
            print "Case issue.getAllForProduct"
            data = deserial_test.deserial_metadata('issue.getAllForProduct',
                    'templates/events/metadata-issue.getAllForProduct.xml')
            
        elif 'method_uri' in query and query['method_uri'] != '':
            # Case of getting all issues for a method
            # To: Metadata service
            print "Case issue.getAllForMethod"
            data = deserial_test.deserial_metadata('issue.getAllForMethod',
                    'templates/events/metadata-issue.getAllForMethod.xml')
       
        elif 'keywords' in query and query['keywords'] != '':
            # Case of issues related to keywords
            # To: KEUI
            print "Case KEUI-keywords"
            data = deserial_test.deserial_keui('issuesForKeywords',
                                    'templates/events/KEUI-keywords.xml')
            
        elif 'developer' in query and query['developer'] != '':
            # Case of suggest issues for a developer
            # To: Recommendation service
            print "Case Recommender.issuesRecommended"
            data = deserial_test.deserial_recommendation('issue.Recommendation',
                                    'templates/events/recommender-issuesRecommended.xml')
        
        else:
            # Error: there must be one option selected
            return HttpResponse("Unsupported query petition.</br>"+\
                "You must provide at least a commit_id, issue_id, "+\
                "list of keywords (separated by blank spaces) "+\
                "or developer name for searching.")
                
        return HttpResponse(json.dumps(data), mimetype="application/json")
            
        
        #return HttpResponse(
            ##query.get('project') + '</br>' +\
            ##query.get('issue_id') + '</br>' +\
            ##query.get('keywords') + '</br>' +\
            ##query.get('commit_id') + '</br>' +\
            ##query.get('component') + '</br>' +\
            ##query.get('start_date') + '</br>' +\
            ##query.get('end_date') + '</br>' +\
            #json.dumps(data), mimetype="application/json"
            #)

@JSONPCallback
def query_handler(request):
    """
    Entry method to handle incoming search queries for hound service.
    Query fields come embedded in request search arguments.
    """
    
    ec = EventComposer()
    
    if request.method == 'GET':
        
        query = request.GET
        
        if 'commit_option' in query:
            
            if (query['commit_option'] == 'info'):
                if 'commit_uri' in query and query['commit_uri'] != '':
                    # Case of retrieving information from a commit
                    print "Case commit.getInfo"

                    params_commit_get_info = {"apiCall": "commit.getInfo",
                        "in_params": (("commitUri", 
                        query['commit_uri'],),)
                        }
                    
                    response = ec.send_recv_metadata(BUS_URL, params_commit_get_info)

                    print("Received: ALERT.Metadata.APICallResponse")
                    
                    data = ec.deserial_metadata('commit.getInfo',
                                StringIO(response))
                else:
                    return HttpResponse("You must provide the commit URI")
                
            elif (query['commit_option'] == 'prod'):
                if 'product' in query and query['product'] != '':
                    # Case of retrieving all commits related to a method
                    # To: Metadata service
                    print "Case commit.getAllForProduct"
                    
                    if 'from_date' in query and query['from_date'] != '':
                        params_commit_get_all_for_product = {"apiCall": "commit.getAllForProduct",
                        "in_params": (("productID", query['product'],),
                                    ("fromDate",query['from_date'],),)
                        }
                        
                    else:
                        params_commit_get_all_for_product = {"apiCall": "commit.getAllForProduct",
                        "in_params": (("productID", query['product'],),)
                        }
                    
                    response = ec.send_recv_metadata(BUS_URL, params_commit_get_all_for_product)

                    print("Received: ALERT.Metadata.APICallResponse")
                    
                    data = ec.deserial_metadata('commit.getAllForProduct',
                            StringIO(response))
                else:
                    return HttpResponse("You must provide a product name.")
                        
        elif ('issue_id' in query and query['issue_id'] != ''):
            
            if ('issue_option' in query and query['issue_option'] != ''):
                if (query['issue_option'] == 'sug'):
                    # Case of suggesting developers for an issue
                    # To: Recommendation service
                    print "Case Recommender.identity.Recommendation"
                    
                    params_devs_recommend = {"issues": ((query['issue_id'],"owl#1"),) 
                                        }
                    
                    response = ec.send_recv_recommender(BUS_URL, params_devs_recommend, 'devs')
                    
                    print("Received: Response from Recommendation service")
                    response = response.replace('encoding="UTF-8"', 'encoding="iso-8859-1"')
                    
                    data = ec.deserial_recommendation('identity.Recommendation',
                            StringIO(response))
                
                elif (query['issue_option'] == 'sim'):
                    # Case of finding related issues
                    # To: KEUI
                    print "Case KEUI-similarThreads"
                    
                    params_similar_threads = {"type": "similarThreads",
                                              "threadId": "-1",
                                              "bugId": query['issue_id'],
                                              "count": 10,
                                              "itemDataSnipLen" : 200,
                                              "includeItemIds": "True",
                                              "includeItemData": "True",
                                              "includeOnlyFirstInThread": "True",                          
                                              "maxCount": 10,
                                              "offset": 0,
                                              "includePeopleData" : "False"
                                              }

                    response = ec.send_recv_keui(BUS_URL, params_similar_threads)
                    response = response.replace('encoding="UTF-8"', 'encoding="iso-8859-1"')
                    data = ec.deserial_keui('similarThreads',
                                    StringIO(response))
                
                elif (query['issue_option'] == 'ext'):
                    # Case of presented extended info about issue
                    # To: Metadata service
                    print "Case issue.getInfo"
                                  
                    params_issue_get_info = {"apiCall": "issue.getInfo",
                                "in_params": (("issueID",query['issue_id'],),)
                                }

                    response = ec.send_recv_metadata(BUS_URL, params_issue_get_info)

                    print("Received: ALERT.Metadata.APICallResponse")
                    response = response.replace('encoding="UTF-8"', 'encoding="iso-8859-1"')
                    data = ec.deserial_metadata('issue.getInfo',
                                    StringIO(response))
     
            else:
                return HttpResponse("You must select an issue option for this particular ID.")
                                        
        elif 'product' in query and query['product'] != '':
            # Case of getting all issues for a product
            # To: Metadata service
            print "Case issue.getAllForProduct"
            
            if 'from_date' in query and query['from_date'] != '':
                params_issue_get_all_for_product = {"apiCall": "issue.getAllForProduct",
                    "in_params": (("productID", query['product'],),
                                    ("fromDate", query['from_date'],),)
                    }
                    
            else:
                params_issue_get_all_for_product = {"apiCall": "issue.getAllForProduct",
                    "in_params": (("productID", query['product'],),)
                    }
            
            response = ec.send_recv_metadata(BUS_URL, params_issue_get_all_for_product)

            print("Received: ALERT.Metadata.APICallResponse")
            
            data = ec.deserial_metadata('issue.getAllForProduct',
                    StringIO(response))
            
        elif 'method_uri' in query and query['method_uri'] != '':
            # Case of getting all issues for a method
            # To: Metadata service
            print "Case issue.getAllForMethod"
            
            #TODO: Handle input for more than one method
            params_issue_get_all_for_method = {"apiCall": "issue.getAllForMethod",
                "in_params": (("methodUri", query['method'],),)
                }
            
            response = ec.send_recv_metadata(BUS_URL, params_issue_get_all_for_method)

            print("Received: ALERT.Metadata.APICallResponse")
            
            data = ec.deserial_metadata('issue.getAllForMethod',
                    StringIO(response))
       
        elif 'keywords' in query and query['keywords'] != '':
            # Case of issues related to keywords
            # To: KEUI
            print "Case KEUI-keywords"
            
            params_issues_for_keywords = {'keywords': (query['keywords'],),
                        "offset": 0, "maxCount": 100, 'resultData': 'itemData',
                        "includeAttachments": 1, 'sortBy': 'dateDesc',
                        'itemDataSnipLen': 200, 'snipMatchKeywords': 1,
                        'keywordMatchOffset': 25, 'includePeopleData':0
                        }
            
            response = ec.send_recv_keui(BUS_URL, params_issues_for_keywords)
            
            data = ec.deserial_keui('issuesForKeywords',
                                    StringIO(response))
            
        elif 'developer' in query and query['developer'] != '':
            # Case of suggest issues for a developer
            # To: Recommendation service
            print "Case Recommender.issuesRecommended"
            
            # Example developer UUID:
            # "ff9dc34d-774e-47ad-9eab-07c46ab3e765ff0df1c4-4c8d-4703-97ea-267d83b4ac08"
            params_issues_recommend = {"identities": (query['developer'],)
                }
            
            response = send_recv_recommender(BUS_URL, params_issues_recommend, 'issues')
            
            data = ec.deserial_recommendation('issue.Recommendation',
                                    StringIO(response))
        
        else:
            # Error: there must be one option selected
            return HttpResponse("Unsupported query petition.</br>"+\
                "You must provide at least a commit_id, issue_id, "+\
                "list of keywords (separated by blank spaces) "+\
                "or developer name for searching.")
                
        return HttpResponse(json.dumps(data), mimetype="application/json")
    