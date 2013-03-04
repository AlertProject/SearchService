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

#from event_handler import EventHandler
from lxml import etree
from search.model import person

#from activemq.EventPublisher import EventPublisher

from activemq.bus_query import BusQuery
from event_composer import EventComposer

from StringIO import StringIO

if __name__ == "__main__":
    
    def send_receive(test):
        print "message ready to be sent"
        rv_message = test.run() 
        print "sent"
        print "*******"
        print "*******"
        print "received message is:"
        print ""
        #print rv_message
        print "*******"
        return rv_message
    
    ##########################################
    # SERIALIZATION TEST
    ##########################################
    
    # URL of target ActiveMQ bus
    # To monitor bus activity for cimcollege browse to the following URL
    # http://www.cimcollege.rs:8161/admin/topics.jsp
    url = 'tcp://www.cimcollege.rs:61616'
    #url = 'tcp://laus.perimeter.fzi.de:61616'
    # General purpose event composer
    event_composer = EventComposer()
    
    ## Socrates
    ## issue recommendation
    #tx_message = event_composer.serial_metadata(EventComposer.header_issues_recomm, 
                                #EventComposer.params_issues_recommend,
                                #False, True, EventComposer.topic_req_issues_recomm)
    #print tx_message
    #test_recomm = BusQuery(url, EventComposer.topic_req_issues_recomm, tx_message,
                             #EventComposer.topic_res_issues_recomm)
    #send_receive(test_recomm)
    
    ## developer recommendation
    #tx_message = event_composer.serial_metadata(EventComposer.header_devs_recomm, 
                                #EventComposer.params_devs_recommend,
                                #False, True, EventComposer.topic_req_devs_recomm)
    #print tx_message
    #test_recomm = BusQuery(url, EventComposer.topic_req_devs_recomm, tx_message,
                             #EventComposer.topic_res_devs_recomm)
    #send_receive(test_recomm)
    
    # Metadata
    # issue.getInfo
    #####
    #params_issue_get_info = {"apiCall": "issue.getInfo",
                                     #"in_params": (("issueID", '253729',),)} 
    #tx_message = event_composer.serial_metadata(None, 
                                ##EventComposer.params_issue_get_info,
                                #params_issue_get_info,
                                #False, True, EventComposer.topic_req_metadata)
    #for i in range(1,20):
            #print ""
    
    #print "Sending issue.getInfo to metadata service for issueID: 253729"
    #print "*****"
    #print "*****"
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #answer = send_receive(test_metadata)
    
    #f = open('topo.xml', 'w')
    #f.write(StringIO(answer))
    #f.close()
    
    ## issue.getOpen                                 
    #tx_message = event_composer.serial_metadata(None, 
                                #EventComposer.params_issue_get_open,
                                #False, True, EventComposer.topic_req_metadata)
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #send_receive(test_metadata)
    
    ## issue.getAllForProduct
    #tx_message = event_composer.serial_metadata(None, 
                                #EventComposer.params_issue_get_all_for_product,
                                #False, True, EventComposer.topic_req_metadata)
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #answer = send_receive(test_metadata)
    
    # issue.getAllForMethod
    #tx_message = event_composer.serial_metadata(None, 
                                #EventComposer.params_issue_get_all_for_method,
                                #False, True, EventComposer.topic_req_metadata)
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #answer = send_receive(test_metadata)
    
    ## commit.getAllForProduct
    #tx_message = event_composer.serial_metadata(None, 
                               #EventComposer.params_commit_get_all_for_product,
                               #False, True, EventComposer.topic_req_metadata)
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #answer = send_receive(test_metadata)
    
    # method.getAllForIdentity
    #tx_message = event_composer.serial_metadata(None, 
                                #EventComposer.params_method_get_all_for_identity,
                                #False, True, EventComposer.topic_req_metadata)
    #print tx_message
    #test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             #EventComposer.topic_res_metadata)
    #answer = send_receive(test_metadata)
    
    # commit.getInfo
    tx_message = event_composer.serial_metadata(None, 
                                EventComposer.params_commit_get_info,
                                False, True, EventComposer.topic_req_metadata)
    print tx_message
    test_metadata = BusQuery(url, EventComposer.topic_req_metadata, tx_message,
                             EventComposer.topic_res_metadata)
    answer = send_receive(test_metadata)
    
    ## KEUI
    
    ## Get similar threads
    #tx_message = event_composer.serial_keui(None, 
                                    #EventComposer.params_issues_for_keywords,
                                    #False, True, EventComposer.topic_req_keui)
    #print tx_message
    #test_keui = BusQuery(url, EventComposer.topic_req_keui, tx_message,
                         #EventComposer.topic_res_keui)
    #send_receive(test_keui)
    
    ## Get issues for keywords
    #tx_message = event_composer.serial_keui(None,
                                    #EventComposer.params_similar_threads,
                                    #False, True, EventComposer.topic_req_keui)
    #print tx_message
    #test_keui = BusQuery(url, EventComposer.topic_req_keui, tx_message,
                         #EventComposer.topic_res_keui)
    #send_receive(test_keui)

    ##########################################
    # DESERIALIZATION TEST
    ##########################################
    
    des_test = EventComposer()
    
    ## Socrates
    
    ## Socrates recommendation: socrates-identity-recomm-test.xml
    #res = des_test.deserial_recommendation('identity.Recommendation',
                                      #'socrates-identity-recomm-test.xml')
    #print res
    
    ## Socrates event_file = "socrates-issuesRecommended.xml"
    #res = des_test.deserial_recommendation('issue.Recommendation',
                                      #'socrates-issuesRecommended.xml')
    #print res
    
    # Metadata
    
    # Metadata issue.getInfo
    #res = des_test.deserial_metadata('issue.getInfo',
                                      ##'metadata-issue.getInfo.xml')
                                      #StringIO(answer))
    #print "Response event: " + res['event'] 
    #print answer
    
    #issues = res['issues']
    #print issues['references']
    #print issues['issue_activities']
    #comments = issues['issue_comments']
    #print comments
    #print issues['issue_description']
    #print issues
    
    ## Metadata issue.getOpen
    #res = des_test.deserial_metadata('issue.getOpen',
                                      #'metadata-issue.getOpen.xml')
    
    #print res
    
    ## Metadata issue.getAllForProduct
    ## Metadata event_file = "metadata-issue.getAllForProduct.xml"
    #res = des_test.deserial_metadata('issue.getAllForProduct',
                                        #StringIO(answer))
                                      #'APIResponse - issue.getAllForProduct.xml')
    #print res
    
    ## Metadata commit.getInfo
    res = des_test.deserial_metadata('commit.getInfo',
                                        StringIO(answer))
                                      #'APIResponse - issue.getAllForProduct.xml')
    print res
    
    ## Metadata commit.getAllForProduct
    #res = des_test.deserial_metadata('commit.getAllForProduct',
                                        #StringIO(answer))
                                      #'APIResponse - commit.getAllForProduct.xml')
    #print res
    
    ## Metadata issue.getAllForMethod
    #res = des_test.deserial_metadata('issue.getAllForMethod',
                                        #StringIO(answer))
                                      #'APIResponse - issue.getAllForMethod.xml')
    #print res
    
    ## Metadata method.getAllForIdentity
    #res = des_test.deserial_metadata('method.getAllForIdentity',
                                        #StringIO(answer))
                                      #'APIResponse - method.getAllForIdentity.xml')
    #print res
    
    ## KEUI
    
    ## Get similar threads
    #res = des_test.deserial_keui('similarThreads', 
                            #'ALERT.KEUI.Response#similarThreads.xml')
    #print res
    
    ## Get issues for keywords
    #res = des_test.deserial_keui('issuesForKeywords', 
                            #'ALERT.KEUI.Response#keywords.xml')
    #print res