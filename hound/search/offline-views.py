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
from activemq.bus_query import BusQuery
from StringIO import StringIO
import json

class SearchForm(forms.Form):
    PROJECT_CHOICES = (('solid','Solid (KDE)'),
                      )
    project = forms.ChoiceField(choices = PROJECT_CHOICES)
    #project = forms.CharField()
    issue_id = forms.CharField(widget = forms.TextInput(attrs={'oninput':'OnInput (event);DisableRight (event)'}))
    I_OPTIONS = (('sug','Get suggested assignee'),
                 ('rel','Find related issues'),
                 ('ext','Display extended issue view'),
                )
    issue_option = forms.ChoiceField(widget=RadioSelect(attrs={'disabled':'disabled'}),
                                     choices = I_OPTIONS)
    keywords = forms.CharField(required = False,
                               widget = forms.TextInput(attrs={'oninput':'DisableLeft (event)'}))

def search_form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            #name = form.cleaned_data['name']
            #surname = form.cleaned_data['surname']
            
            # Also forward csrf context info
            #return render_to_response('characters/contact.html', 
                                      #{'name': name, 'surname': surname}, 
                                      #context_instance = c)
            #return render_to_response('characters/contact.html', 
                                      #{'name': name, 'surname': surname})
            
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = SearchForm() # An unbound form

    return render_to_response('search.html', {
        'form': form,
    })
                                            
    

def query_handler(request):
    """
    Entry method to handle incoming search queries for hound service.
    Query fields come embedded in request search arguments.
    """
    
    if request.method == 'GET':
        
        query = request.GET
        print "kk"
        
        html = "The query items: </br>"

        json_project = ""
        json_issue_id = ""
        json_issue_option = ""
        json_keywords = ""
        json_data = ""
        json_suggested = ""
        json_happening = ""

        print "kk2"
	if 'project' in request.GET:
            json_project = str(query.get('project'))
        
        if 'issue_id' in request.GET:
            json_issue_id = str(query.get('issue_id'))

	if 'issue_option' in request.GET:
            json_issue_option = str(query.get('issue_option'))
            
        if 'keywords' in request.GET:
            json_keywords = str(query.get('keywords'))

        if 'suggested' in request.GET:
            json_suggested = str(query.get('suggested'))

        if 'happening' in request.GET:
            json_happening = str(query.get('hapenning'))

        print "kk3"

        data = []

        print("issue_id = %s" % (query['issue_id'],))
        print "kk4"

        if query['suggested'] == 'sug':
            print "** SUGGESTED USE CASE**"   # to be deleted
            #ALERT.Search.APICallRequest (issue.getOpen) Search service -> Metadata service
            #ALERT.Metadata.APICallResponse (issue.getOpen) Metadata service ->	Search service
            #ALERT.Search.Recommender.RecommendationRequest Search service -> Recommender
            #ALERT.Recommender.IdentityRecommendation Recommender -> Search service

            ec = EventComposer()

            params_issue_get_open = {"apiCall": "issue.getOpen",
                                     "name": "productID",
                                     "value": query['project']}
            get_open_msg = ec.serial_metadata(None,
                                              params_issue_get_open,
                                              False, True,
                                              EventComposer.topic_req_metadata)
            #print get_open_msg

            #bquery = BusQuery('tcp://www.cimcollege.rs:61616',
            
            ## bquery = BusQuery('tcp://laus.perimeter.fzi.de:61616',            
            ##                   EventComposer.topic_req_metadata,
            ##                   get_open_msg,
            ##                   'ALERT.Metadata.APICallResponse')
            ## try:
            ##     result = bquery.run()
            ##     print "Received: ALERT.Metadata.APICallResponse"
            ## except:
            ##     print "ERROR: ALERT.Metadata.APICallResponse is MIA"

            print "hola"

            ## print result
            ## aux = ec.deserial_metadata('issue.getOpen', StringIO(result))
            ## print aux
            ## aux_issues = ()
            ## cont = 0
            ### {'issue_id': '271749', 'issue_uri': 'http://www.alert-project.eu/ontologies/alert_its.owl#Bug870', 'issue_url': 'https://bugs.kde.org/show_bug.cgi?id=271749', 'desc': 'Malformed URL error dragging and dropping a file to a usb drive'}]}
            ## for i in aux['issues']:
            ##     aux_issues = aux_issues + ((i['issue_id'], i['issue_uri']),)
            ##     cont = cont + 1
            ##     if (cont == 10):
            ##         break

            ## print("%s opened issues" % (str(cont),))

            ## ### params_devs_recommend = {"issues": aux_issues}
            ## params_devs_recommend = {"issues": ( (291250,"owl#1"), 
            ##                                      (290735, "owl#2"),) }
                        
            ## to_reco_msg = ec.serial_recommendation(ec.header_devs_recomm,
            ##                                        params_devs_recommend,
            ##                                        False, True,
            ##                                        ec.topic_req_devs_recomm)

            ## # comment out as soon as Fotis starts its component
            ## print to_reco_msg
                
            ## # bquery = BusQuery('tcp://www.cimcollege.rs:61616',"""
            ## bquery = BusQuery('tcp://laus.perimeter.fzi.de:61616',
            ##                   ec.topic_req_issues_recomm,
            ##                   to_reco_msg,
            ##                   'ALERT.Recommender.IdentityRecommendation')
            ## try:
            ##     result = bquery.run()
            ##     print "Received: ALERT.Recommender.IdentityRecommendation"
            ## except:
            ##     print "ERROR: ALERT.Recommender.IdentityRecommendation is MIA"
            

            #print result

            # comment out this as soon as the metadata and recommendation components are started
            suggested_devs = ec.deserial_recommendation('identity.Recommendation',
                                                        'socrates-identity-recomm-test.xml')

            suggested_devs['devs']['2050'].append("Notify user on hardware changes")
            suggested_devs['devs']['2050'].append("https://bugs.kde.org/show_bug.cgi?id=184671")

            suggested_devs['devs']['274'].append("Cant open window Power Management")
            suggested_devs['devs']['274'].append("https://bugs.kde.org/show_bug.cgi?id=177772")

            print suggested_devs
            
            data = suggested_devs

            #print suggested_devs

        elif query['issue_id']:
            print "** EXTENDED VIEW USE CASE**"   # to be deleted
            #ALERT.Search.APICallRequest (issue.getInfo) Search service -> Metadata service
            #ALERT.Metadata.APICallResponse (issue.getInfo) Metadata service ->	Search service

            ec = EventComposer()

            ## params_issue_get_info = {"apiCall": "issue.getInfo",
            ##                          "name": "issueID",
            ##                          "value": query['issue_id']}    
            ## get_info_msg = ec.serial_metadata(None,
            ##                                   params_issue_get_info,
            ##                                   False, True,
            ##                                   EventComposer.topic_req_metadata)
            ## print get_info_msg
            ## #bquery = BusQuery('tcp://laus.perimeter.fzi.de:61616',
            ## bquery = BusQuery('tcp://www.cimcollege.rs:61616',
            ##                   ec.topic_req_metadata,
            ##                   get_info_msg,
            ##                   'ALERT.Metadata.APICallResponse')            

            ## result = bquery.run()

            ## print("Received: ALERT.Metadata.APICallResponse")

            ## print result

            ## aux = ec.deserial_metadata('issue.getInfo', StringIO(result))

            print "hola"
            aux = ec.deserial_metadata('issue.getInfo','metadata-issue.getInfo.xml')
            print "adios"
            print aux

            data = aux

        elif query['happening'] == 'happening':
            print("METHOD NOT IMPLEMENTED")
            # TO BE DONE

        elif query['issue_option'] == 'rel':
            print "** RELATED ISSUES USE CASE**"   # to be deleted
            #Alert.Search.KEUIRequest 	Search service -> KEUI
            #ALERT.KEUI.Response 	KEUI ->	Search service
            # to be done
        else:
            print "** KEYWORDS USE CASE**"
            # TO BE DONE


        try:
            resjson = json.dumps(data)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        resjson = query.get('jsoncall') + "(" + resjson + ")"

        print("JSON to be sent back: %s" % (resjson,))


        return HttpResponse(resjson)
