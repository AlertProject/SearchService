#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Hound: Search service
# Copyright (C) 2012 GSyC/LibreSoft, Universidad Rey Juan Carlos
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

from event_handler import EventHandler
from lxml import etree
from search.model import person
from activemq.EventPublisher import EventPublisher
from activemq.bus_query import BusQuery

class EventComposer(object):
    
    # Metadata
    # Test issue.getInfo
    params_issue_get_info = {"apiCall": "issue.getInfo",
                "in_params": (("issueID",'184671',),)
                }
                
    # Test issue.getOpen
    params_issue_get_open = {"apiCall": "issue.getOpen",
                "in_params": (("productID", "solid",),)
                }
                
    # Test issue.getAllForProduct
    params_issue_get_all_for_product = {"apiCall": "issue.getAllForProduct",
                "in_params": (("productID", "solid",),
                                ("fromDate", "2012-03-16 12:00",),)
                }
                
    # Test issue.getAllForMethod
    params_issue_get_all_for_method = {"apiCall": "issue.getAllForMethod",
        "in_params": (("methodUri",
        "http://www.alert-project.eu/ontologies/alert.owl#Method1",
        "http://www.alert-project.eu/ontologies/alert.owl#Method10",),)
        }
        
    # Test commit.getAllForProduct
    params_commit_get_all_for_product = {"apiCall": "commit.getAllForProduct",
                "in_params": (("productID", "solid",),
                                ("fromDate","2012-01-13 12:00",),)
                }
    
    # Test commit.getInfo
    params_commit_get_info = {"apiCall": "commit.getInfo",
                "in_params": (("commitUri", 
                "http://www.alert-project.eu/ontologies/alert_scm.owl#Commit5",),)
                }
    
    
    # Test method.getAllForIdentity
    params_method_get_all_for_identity = {"apiCall": "method.getAllForIdentity",
                "in_params": (("uuid","ivano",),)
                }
    
    # Test developers recommendation
    header_devs_recomm = {'name': "ALERT.Search.Recommender."+\
                "IdentitiesRecommendationRequest",
                'id': 5478, 'type': "request", 'api': None
                }
    
    params_devs_recommend = {"issues": ( (291250,"owl#1"), 
                                        (290735, "owl#2"),) 
                                        }
    
    # Test issues recommendation
    header_issues_recomm = {'name': "ALERT.Search.Recommender."+\
                "IssueRecommendationRequest",
                'id': 5478, 'type': "request", 'api': None
                }
    
    params_issues_recommend = {"identities": ("ff9dc34d-774e-47ad-"+\
                "9eab-07c46ab3e765",
                "ff0df1c4-4c8d-4703-97ea-267d83b4ac08",)
                }
              
    # Test KEUI similar threads
    params_similar_threads = {"type": "similarThreads",
                              "threadId": -1,
                              "bugId": 55,
                              "count": 50,
                              "itemDataSnipLen" : 200,
                              "includeItemIds": "True",
                              "includeItemData": "True",
                              "includeOnlyFirstInThread": "True",
                              "maxCount": 50,
                              "offset": 0,
                              "includePeopleData" : "True"
                              }

    params_issues_for_keywords = {'keywords': ('solid',),
                "offset": 0, "maxCount": 100, 'resultData': 'itemData',
                "includeAttachments": 1, 'sortBy': 'dateDesc',
                'itemDataSnipLen': 200, 'snipMatchKeywords': 1,
                'keywordMatchOffset': 25, 'includePeopleData':0
                }
    
    topic_req_metadata = 'ALERT.Search.APICallRequest'
    
    topic_req_issues_recomm = 'ALERT.Search.Recommender.'+\
                                'IssueRecommendationRequest'
    
    topic_req_devs_recomm = "ALERT.Search.Recommender."+\
                            "IdentitiesRecommendationRequest"
    
    topic_req_keui = "ALERT.Search.KEUIRequest"
    
    topic_res_keui = "ALERT.KEUI.Response"
    
    topic_res_metadata = "ALERT.Metadata.APICallResponse"
    
    topic_res_issues_recomm = "ALERT.Recommender.IssueRecommendation"
    
    topic_res_devs_recomm = "ALERT.Recommender.IdentityRecommendation"
    
    def __init__(self):
        self.event_handler = EventHandler()
        
    # SERIALIZATION TESTS        
    def serial_recommendation(self, header, params, printed, 
                              message, topic_name):
        if printed:
            self._print_event(header,params)
        
        if message and topic_name is not None:
            #for index in range(1,11):
            #self._publish_event(header, params, topic_name)
            return self._get_event(header, params)
    
    def serial_metadata(self, header, params, printed, message, topic_name):
        if header is None:
            header = {'name': "ALERT.Search.APICallRequest",
                      'id': 5476, 'type': "request", 'api': 'apiRequest'}
        
        if printed:  
            self._print_event(header,params)
        if message and topic_name is not None:
            #for index in range(1,11):
            #self._publish_event(header, params, topic_name)
            return self._get_event(header, params)
    
    def serial_keui(self, header, params, printed, message, topic_name):
        if header is None:
            if 'type' in params:
                header = {'name': "ALERT.Search.KEUIRequest",
                          'id': 5478, 'type': "request", 
                          'api': "customQuery"}
            
            elif 'keywords' in params:
                header = {'name': "ALERT.Search.KEUIRequest",
                          'id': 5478, 'type': "request", 
                          'api': "generalQuery"}
        
        if printed:  
            self._print_event(header,params)
                            
        if message and topic_name is not None:
            #for index in range(1,11):
            #    self._publish_event(header, params, topic_name)
            return self._get_event(header, params)
    
    
    # DESERIALIZATION TESTS
    def deserial_recommendation(self, event_name, event):
        #res = []
        self.event_handler.load_event(event)
        #if event_name == 'identity.Recommendation':
            #print "Deserializing socrates event: "
            #print "["
            #for person in self.event_handler.entity:
                #print "(" + person.get_name() + ","
                #print person.get_user_id() + "), "
                #res.append((person.get_name(), person.get_user_id()))
            #print "]"
            
        #elif event_name == 'issue.Recommendation':
            #print self.event_handler.entity

        return self.event_handler.entity
    
    def deserial_metadata(self, event_name, event):
        print "line 0: deserial_metadata"  # DELETEME
        self.event_handler.load_event(event)
        return self.event_handler.entity
        # Depending on the event type, response list will contain the
        # event name (first item in list) plus a tuple of dicts, with all
        # parameters from the response message payload
        
        # Uncomment the following lines for tracing
        #if event_name == 'issue.getInfo':
            #print "Issue ID is: " + self.event_handler.entity.get_issue_id()
            #print "Issue description: " +\
                  #self.event_handler.entity.get_description()
            #print "Reporter name is: " +\
                  #self.event_handler.entity.get_reporter().get_name()
            #print "Reporter email is: " +\
                  #self.event_handler.entity.get_reporter().get_email()
            #print "Reporter id is: " +\
                  #self.event_handler.entity.get_reporter().get_user_id()
            #print "Assignee name is: " +\
                  #self.event_handler.entity.get_assigned_to().get_name()
            #print "Assignee email is: " +\
                  #self.event_handler.entity.get_assigned_to().get_email()
            #print "Assignee id is: " +\
                  #self.event_handler.entity.get_assigned_to().get_user_id()
            #print "Issue URL: " + self.event_handler.entity.get_issue_url()

        #elif event_name == 'issue.getOpen':
            #for item in self.event_handler.entity:
                #print "Issue Id: " + item.get_issue_id()
                #print "Issue desc: " + item.get_description()
                #print "Issue URL: " + item.get_issue_url()
                
        #elif event_name == 'issue.getAllForProduct':
            #for item in self.event_handler.entity:
                #print "Issue Id: " + item.get_issue_id()
                #print "Issue desc: " + item.get_description()
                #print "Issue URL: " + item.get_issue_url()
            
        #elif event_name == 'commit.getAllForProduct':
            #for commit in self.event_handler.entity:
                #print "Commit message: " + commit.get_commitMessage() +\
                      #" with date: " + commit.get_commitDate()

    
    #def deserial_metadata(self, event_name, message):
        #pass
    
    def deserial_keui(self, event_name, event):
        self.event_handler.load_event(event)
        # For similarThreads return list of tuples 
        # (threads, similarity coef. and item ids)
        # For issuesForKeywords list of dicts
        # each dict carry issue info
        return self.event_handler.entity
            
    
    # UTILITY METHODS
    
    def send_recv_metadata(self, bus_url, params):
        """
        Routine to interact with Metadata service via ActiveMQ bus
        """
        get_info_msg = self.serial_metadata(None,
                                        params,
                                        False, True,
                                        self.topic_req_metadata)
        #Uncomment to trace
        #print get_info_msg

        bquery = BusQuery(bus_url,
                        self.topic_req_metadata,
                        get_info_msg,
                        self.topic_res_metadata)            

        result = bquery.run()
        
        return result
    
    def send_recv_recommender(self, bus_url, params, option):
        """
        Routine to interact with Recommendation service via ActiveMQ bus
        option == 'devs' : recommend developers to solve an issue
        option == 'issues' : recommend issues to a developer
        """
        if option == 'devs':
            header = self.header_devs_recomm
            topic_req = self.topic_req_devs_recomm
            topic_res = self.topic_res_devs_recomm
            
        elif option == 'issues':
            header = self.header_issues_recomm
            topic_req = self.topic_res_issues_recomm
            topic_res = self.topic_req_issues_recomm
        
        get_info_msg = self.serial_recommendation(header, params,
                                        False, True,
                                        topic_req)
                                        
        #Uncomment to trace
        #print get_info_msg
        
        bquery = BusQuery(bus_url, topic_req, get_info_msg, topic_res)

        result = bquery.run()
        
        return result
    
    def send_recv_keui(self, bus_url, params):
        """
        Routine to interact with KEUI via ActiveMQ
        """
        
        get_info_msg = self.serial_keui(None, params,
                                        False, True,
                                        self.topic_req_keui)
                                        
        #Uncomment to trace
        #print get_info_msg
        
        bquery = BusQuery(bus_url, 
                        self.topic_req_keui, 
                        get_info_msg, 
                        self.topic_res_keui)            

        result = bquery.run()
        
        return result
    
    def _publish_event(self, header, params, topic_name):
        # pub = EventPublisher(topic_name)
        # pub.publishMessage(etree.tostring(
        #    self.event_handler.serialize_event(
        #        header['name'], header['id'],
        #        header['type'], header['api'],
        #        params), 
        #    pretty_print = True))
        #pub.finish()
        pass
                
    def _print_event(self, header, params):
        print etree.tostring(self.event_handler.serialize_event(
                                    header['name'], header['id'], 
                                    header['type'], header['api'],
                                    params), 
                            pretty_print = True)
        
    def _get_event(self, header, params):
        return etree.tostring(self.event_handler.serialize_event(
            header['name'], header['id'], 
            header['type'], header['api'],
            params), 
                              pretty_print = True)
    
