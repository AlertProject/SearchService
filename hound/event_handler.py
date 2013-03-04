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

# import xml.etree.cElementTree as ET
from lxml import etree
from search.model.issue import Issue
from search.model.commit import Commit
from search.model.person import Person
from search.model.entity import Entity

from datetime import datetime

class EventHandler(object):
    # Namespace codes xmlns:code
    PRE_SOAP = "soap"
    PRE_WSNT = "wsnt"
    PRE_WSA = "wsa"
    PRE_NS1 = "ns1"
    PRE_O = "o"
    PRE_R = "r"
    PRE_R1 = "r1"
    PRE_R2 = "r2"
    PRE_S = "s"
    PRE_S1 = "s1"
    PRE_S2 = "s2"
    PRE_S3 = "s3"
    PRE_SE = "se"
    PRE_SM = "sm"
    PRE_SC = "sc"
    PRE_XSI = "xsi"
    
    # Namespace prefixes and values
    NS_SOAP = "http://www.w3.org/2003/05/soap-envelope"
    NS_WSNT = "http://docs.oasis-open.org/wsn/b-2"
    NS_WSA = "http://www.w3.org/2005/08/addressing"
    
    NS_NS1 = "http://www.alert-project.eu/"
    NS_O = "http://www.alert-project.eu/ontoevents-mdservice"
    NS_R = "http://www.alert-project.eu/rawevents-forum"
    NS_R1 = "http://www.alert-project.eu/rawevents-mailinglist"
    NS_R2 = "http://www.alert-project.eu/rawevents-wiki"
    NS_S0 = "http://www.alert-project.eu/strevents-kesi"
    NS_S1 = "http://www.alert-project.eu/strevents-keui"
    NS_S2 = "http://www.alert-project.eu/APIcall-request"
    NS_S3 = "http://www.alert-project.eu/APIcall-response"
    NS_SE = "http://www.alert-project.eu/search"
    NS_SM = "http://www.alert-project.eu/stardom"
    NS_SC = "http://www.alert-project.eu/socrates"
    NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    
    SOAP = "{%s}" % NS_SOAP
    WSNT = "{%s}" % NS_WSNT
    WSA = "{%s}" % NS_WSA
    
    NS1 = "{%s}" % NS_NS1
    O = "{%s}" % NS_O
    R = "{%s}" % NS_R
    R1 = "{%s}" % NS_R1
    R2 = "{%s}" % NS_R2
    S0 = "{%s}" % NS_S0
    S1 = "{%s}" % NS_S1
    S2 = "{%s}" % NS_S2
    S3 = "{%s}" % NS_S3
    SE = "{%s}" % NS_SE
    SM = "{%s}" % NS_SM
    SC = "{%s}" % NS_SC
    XSI = "{%s}" % NS_XSI
    
    # Top-level namespaces for serialization
    NS_MAP_TOP = {PRE_SOAP: NS_SOAP, PRE_WSNT: NS_WSNT, PRE_WSA: NS_WSA}

    # Event tag namespaces
    NS_MAP_EVENT = {PRE_NS1: NS_NS1, PRE_O: NS_O, PRE_R: NS_R, PRE_R1: NS_R1,
                    PRE_R2: NS_R2, PRE_S: NS_S0, PRE_S1: NS_S1, PRE_S2: NS_S2,
                    PRE_S3: NS_S3, PRE_SE: NS_SE, PRE_SM: NS_SM, PRE_SC: NS_SC,
                    PRE_XSI: NS_XSI}

    def __init__(self):
        # Parse tree of elements from XML event file
        self.sender = ''
        self.ts = ''
        self.seq_num = ''
        self.event_name = ''
        self.event_id = ''
        self.event_type = ''
        self.entity = None # Stores entities parsed from new event
        self.tree = None # Memory tree from parsed event
        self.root = None # Root element in tree
    
    
    ## SERIALIZATION
    
    def serialize_event(self, event_name, event_id, event_type, 
                        event_api, params):
        """
        XML serialization of events that will be send to ESB
        """
        # Possible args: , req_fields, event_id, event_name, event_type
        # event_api values:
        # ALERT.Search.KEUIRequest (to KEUI)
        # ALERT.Search.APICallRequest (to Metadata)
        # ALERT.Search.Recommender.IssueRecommendationRequest (to Socrates)
        
        # params: Encapsulates additional params depending on type of
        # request/response
        # example: params = ("apiCall", "issue.getInfo", "issueUri", "URI")
        
        # Build common header
        envelope, event_data = self.__build_header(event_name, event_id, 
                                                   event_type)
        
        if event_name == "ALERT.Search.APICallRequest" and\
           event_type == "request" and event_api == "apiRequest":
               return self.__build_metadata_req(envelope, event_data, params)
        
        elif (event_name == "ALERT.Search.Recommender."+\
                            "IssueRecommendationRequest" and\
            event_type == "request") or\
            (event_name == "ALERT.Search.Recommender."+\
                            "IdentitiesRecommendationRequest" and\
            event_type == "request"):
               
               return self.__build_recommendation_req(event_name, envelope, 
                                                      event_data, params)
                                                      
        elif event_name == "ALERT.Search.KEUIRequest":
                  return self.__build_keui_req(event_name, envelope, 
                                               event_data, event_api, params)
        
        # Yield root element by default
        return envelope
        
    def __build_metadata_req(self, envelope, event_data, params):
        """
        Build event requests, target Metadata service
        Cases: params = {"apiCall": (issue.getInfo, issue.getOpen, 
        issue.getAllForProduct)}
        """
        # Event data
        api_req = etree.SubElement(event_data, EventHandler.NS1 + "apiRequest")
        api_call = etree.SubElement(api_req, EventHandler.S2 + "apiCall")
        # Assign call type
        api_call.text = params.get("apiCall")
        
        ##TODO: Double-check that all apiCall cases are indeed equivalent
        
        # Request data
        req_data = etree.SubElement(api_req, 
                                    EventHandler.S2 + "requestData")
        # Check number of input parameters and set values for request
        # Input parameters consist of ((name1, value1,),(name2, value2,),)
        # Sometimes ((name1, value1, value2, value3,),)
        parameters = params.get("in_params")
        for parameter in parameters:
            in_param = etree.SubElement(req_data, 
                                        EventHandler.S2 + "inputParameter")
            name = etree.SubElement(in_param, 
                                    EventHandler.S2 + "name")
            name.text = parameter[0] # Set name
            value = etree.SubElement(in_param,
                                    EventHandler.S2 + "value")
            value.text = parameter[1] # Set value
            # Set additional values if present
            if len(parameter) > 2:
                for k in range(2, len(parameter)):
                    value = etree.SubElement(in_param,
                                    EventHandler.S2 + "value")
                    value.text = parameter[k] # Set value
        
        # Yield root element
        return envelope
    
    def __build_recommendation_req(self, event_name, envelope, event_data, 
                                   params):
        """
        build requests for Socrates recommendation services
        """
        # Event data
        if event_name == "ALERT.Search.Recommender."+\
                         "IssueRecommendationRequest":
            identities = etree.SubElement(event_data,
                                          EventHandler.SC + "identities")
            identity_ids = params.get("identities")
            for identity in identity_ids:
                identity_tag = etree.SubElement(identities,
                                                EventHandler.SC + "identity")
                uuid = etree.SubElement(identity_tag,
                                        EventHandler.SC + "uuid")
                uuid.text = identity
                
        elif event_name == "ALERT.Search.Recommender."+\
                           "IdentitiesRecommendationRequest":
            issues = etree.SubElement(event_data,
                                          EventHandler.SC + "issues")
            issues_ids = params.get("issues")
            
            for issue_id, bug_url in issues_ids:
                issue_tag = etree.SubElement(issues,
                                                EventHandler.SC + "issue")
                id = etree.SubElement(issue_tag,
                                        EventHandler.SC + "id")
                id.text = str(issue_id)
                bug = etree.SubElement(issue_tag,
                                        EventHandler.O + "bug")
                bug.text = bug_url
        
        # Yield root element
        return envelope
        
    def __build_keui_req(self, event_name, envelope, event_data, event_api,
                                   params):
        """
        build requests for KEUI service
        """
        # Event data
        keui_req = etree.SubElement(event_data,
                                        EventHandler.S1 + "keuiRequest")
        req_type = etree.SubElement(keui_req,
                                    EventHandler.S1 + "requestType")
        req_type.text = "Query"
        req_data = etree.SubElement(keui_req,
                                    EventHandler.S1 + "requestData")
        query = etree.SubElement(req_data,"query")
        query.attrib['type'] = event_api

        if event_api == "customQuery":
            parameters = etree.SubElement(query,"params")
            for key in params.iterkeys():
                parameters.attrib[key] = str(params[key])

            query_args = etree.SubElement(query,"queryArgs")
            conds = etree.SubElement(query_args,"conditions")
            posts = etree.SubElement(conds,"postTypes")
            posts.text = "issues";

        elif event_api == "generalQuery":
            query_args = etree.SubElement(query,"queryArgs")
            conds = etree.SubElement(query_args,"conditions")
            keywords = etree.SubElement(conds,"keywords")
            
            for word in params['keywords']:
                kw = etree.SubElement(keywords, 'kw')
                kw.text = word
            
            parameters = etree.SubElement(query,"params")
            for key in params.iterkeys():
                if key != 'keywords':
                    parameters.attrib[key] = str(params[key])
            
        # Yield root element
        return envelope
    
    def __build_header(self, value_event_name, value_event_id, 
                       value_event_type):
        """
        Create common header for all messages
        value_event_id: Unique identifier for this event
        value_event_type: {request, response}
        """
        envelope = etree.Element(EventHandler.SOAP + "Envelope", 
                                 nsmap = EventHandler.NS_MAP_TOP)
        header = etree.SubElement(envelope, EventHandler.SOAP + "Header")
        header.text = ""
        body = etree.SubElement(envelope, EventHandler.SOAP + "Body")
        notify = etree.SubElement(body, EventHandler.WSNT + "Notify")
        notification_msg = etree.SubElement(notify, 
                                 EventHandler.WSNT + "NotificationMessage")
        topic = etree.SubElement(notification_msg, EventHandler.WSNT + "Topic")
        topic.text = ""
        producer_ref = etree.SubElement(notification_msg,
                                   EventHandler.WSNT + "ProducerReference")
        address = etree.SubElement(producer_ref, EventHandler.WSA + "Address")
        address.text = "http://www.alert-project.eu/search"
        message = etree.SubElement(notification_msg,
                                   EventHandler.WSNT + "Message")
        
        # Event definition
        event = etree.SubElement(message, EventHandler.NS1 + "event",
                                 nsmap = EventHandler.NS_MAP_EVENT)
        ## SPECIAL ATTRIBUTE in tag event USING xsi: namespace
        event.set(EventHandler.XSI + "schemaLocation", 
                  "http://www.alert-project.eu/alert-root.xsd")
        
        # Event head
        head = etree.SubElement(event, EventHandler.NS1 + "head")
        sender = etree.SubElement(head, EventHandler.NS1 + "sender")
        sender.text = "Search"
        timestamp = etree.SubElement(head, EventHandler.NS1 + "timestamp")
        timestamp.text = "10000"
        seq_num = etree.SubElement(head, EventHandler.NS1 + "sequencenumber")
        seq_num.text = "1"
        
        # Event payload
        payload = etree.SubElement(event, EventHandler.NS1 + "payload")
        
        # Event metadata
        meta = etree.SubElement(payload, EventHandler.NS1 + "meta")
        start_time = etree.SubElement(meta, EventHandler.NS1 + "startTime")
        start_time.text = "10010"
        end_time = etree.SubElement(meta, EventHandler.NS1 + "endTime")
        end_time.text = "10010"
        event_name = etree.SubElement(meta, EventHandler.NS1 + "eventName")
        event_name.text = value_event_name
        event_id = etree.SubElement(meta, EventHandler.NS1 + "eventId")
        event_id.text = str(value_event_id)
        event_type = etree.SubElement(meta, EventHandler.NS1 + "eventType")
        event_type.text = value_event_type
        
        # Event data header
        data = etree.SubElement(payload, EventHandler.NS1 + "eventData")
        
        # Return root element and event_payload to continue tree structure
        # after callback
        return envelope, data
        
    def __get_tag(self, elem):
        prefix, tag = elem.tag.split("}")
        prefix = prefix.lstrip("{")
        return prefix, tag
        
    ## DESERIALIZATION ##
    
    def load_event(self, event):
        """
        Load event info from new XML message received from ESB
        """
        # Load namespaces and return ET
        #self.tree, self.root = self.__parse_nsmap(event_file)
        self.tree = etree.parse(event)
        self.root = self.tree.getroot()
        
        # Iterate only over etree.Element
        for elem in self.tree.iter(tag=etree.Element):
            #nspace = elem.get(EventHandler.NS_MAP)
            nspace = elem.nsmap
            try:
                prefix, tag = self.__get_tag(elem)
            except(ValueError):
                pass
                # print "Warning, some tags not including namespace prefix"
            
            if nspace.has_key(EventHandler.PRE_NS1) and\
                                prefix == nspace[EventHandler.PRE_NS1]:
                # Load event info
                if tag == "sender":
                    # print tag + ":" + elem.text
                    self.sender = elem.text
                    #print self.sender
                
                if tag == "timestamp":
                    # print tag + ":" + elem.text
                    self.ts = elem.text
                    #print self.ts
                    
                if tag == "sequencenumber":
                    # print tag + ":" + elem.text
                    self.seq_num = elem.text
                    #print self.seq_num
                    
                if tag == "eventName":
                    # print tag + ":" + elem.text
                    self.event_name = elem.text
                    #print "eventName: " + self.event_name
                
                if tag == "eventId":
                    # print tag + ":" + elem.text
                    self.event_id = elem.text
                    #print self.event_id
                    
                if tag == "eventType":
                    # print tag + ":" + elem.text
                    self.event_type = elem.text
                    #print self.event_type
        
        # Case IssueNew
        if self.event_name == "ALERT.KESI.IssueNew" and\
        self.event_type == "request": 
                self.entity = {"event": self.event_name, "issue": self.__load_new_issue()}
            
        # Case IssueRecommendation
        elif self.event_name == "ALERT.Recommender.IssueRecommendation":
                self.entity = {"event": self.event_name, "issues": self.__load_recomm_issues()}
        
        # Case IdentityRecommendation
        elif self.event_name == "ALERT.Recommender.IdentityRecommendation":
                #self.entity = [(self.event_name,), self.__load_recomm_persons()]
                self.entity = {"event":self.event_name, "devs":self.__load_recomm_persons()}
            
        elif self.event_name == "ALERT.Metadata.APICallResponse":
                res_type, entity = self.__load_metadata_response() 
                #self.entity = [(self.event_name, res_type,), entity]
                # Parsing event name we can guess type of entity in response
                # Such as method.getAllForIdentity --> 'method' or
                # issue.getAllForProduct --> 'issue'
                self.entity = {"event": res_type, "entity":entity}
            
        #elif self.event_name == "ALERT.KEUIResponse" or\
             #self.event_name == 'ALERT.Search.KEUIRequest':
        elif self.event_name == "ALERT.KEUI.Response":
                print "Loading KEUI response"
                res_type, entity = self.__load_keui_response()
                self.entity = {"event": self.event_name, "type": res_type, 
                                "response": entity}
        
    def __load_recomm_issues(self):
        # TODO: fill in complete information about issues
        # from metadata
        issue_id = ''
        bug = ''
        
        # key is issue_id, each one with list of suggested issues
        # only one project for now
        issues = {}
        
        # Iterate only over etree.Element
        for elem in self.tree.iter(tag=etree.Element):
            nspace = elem.nsmap
            prefix, tag = self.__get_tag(elem)
            
            if tag == "id":
                issue_id = elem.text
                
            elif tag == "bug":
                bug = elem.text
                
                if not (issue_id in issues):
                    issues[issue_id] = bug
                
        return issues
    
    def __load_recomm_persons(self):
        
        identities_recomm = []
        # Iterate only over etree.Element
        for elem in self.tree.iter(tag=etree.Element):
            nspace = elem.nsmap
            prefix, tag = self.__get_tag(elem)
            
            # For each issue, get idientity (uuid, name)
            if tag == "identities":
                identities = []
                issue_id = ''
                bug = ''
                
                for subelem in elem.iter():
                    subprefix, subtag = self.__get_tag(subelem)
                    if subtag == 'issue':
                       for issueelem in subelem.iter():
                            issueprefix, issuetag = self.__get_tag(issueelem)
                            if issuetag == 'id':
                                issue_id = issueelem.text
                            elif issuetag == 'bug':
                                bug = issueelem.text
                                
                    elif subtag == 'identity':
                        identity = {}
                        for idenelem in subelem.iter():
                            idenprefix, identag = self.__get_tag(idenelem)
                            if identag == 'uuid':
                                identity['uuid'] = idenelem.text
                            elif identag == 'name':
                                identity['name'] = idenelem.text
                        identities.append(identity)
                
                print "issueid: " + issue_id
                print "bug: " + bug
                identities_recomm = identities
            
        return identities_recomm
        
    def __load_metadata_response(self):
        api_call = ''
        
        # Fields for case of issues
        issue_id = ''
        issue_state = ''
        issue_resolution = ''
        issue_description = ''
        issue_severity = ''
        issue_url = ''
        issue_date_opened = ''
        issue_last_modified = ''
        issue_comments = []
        issue_activities = []
        issue_cc_persons = []
        
        author = None
        
        # TODO: Add support for other types of entities (commit or method)
        
        for elem in self.tree.iter(tag=etree.Element):
            prefix, tag = self.__get_tag(elem)
            
            if tag == "apiCall":
                api_call = elem.text
        
        if api_call == "issue.getInfo":
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                #nspace = elem.get(EventHandler.NS_MAP)
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                                
                    if tag == "issueId":
                        issue_id = elem.text
                    
                    elif tag == "issueAuthor":
                        # Expected subelements name, id, email, in this order
                        author_name = elem[0].text
                        author_id = elem[1].text
                        author_email = elem[2].text
                        
                        author = Person(author_name, author_email, author_id)
                    
                    elif tag == "issueStatus":
                        issue_state = elem.text
                                
                    elif tag == "issueResolution":
                        issue_resolution = elem.text
                    
                    elif tag == "issueDescription":
                        parent_prefix, parent_tag = self.__get_tag(elem.getparent())
                        if parent_tag == "responseData":
                            issue_description = elem.text
                    
                    #TODO: keyword
                    #Product
                    elif tag == 'issueProduct':
                        issue_product = {}
                        for subelem in elem.iter(): 
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'productComponentUri':
                                issue_product['component_uri'] = subelem.text
                            elif subtag == 'productComponentid':
                                issue_product['component_id'] = subelem.text
                            elif subtag == 'productUri':
                                issue_product['uri'] = subelem.text
                            elif subtag == 'productid':
                                issue_product['id'] = subelem.text
                            elif subtag == 'productVersion':
                                issue_product['version'] = subelem.text
                    
                    #Computer system
                    elif tag == 'issueComputerSystem':
                        issue_comp_sys = {}
                        for subelem in elem.iter(): 
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'computerSystemUri':
                                issue_comp_sys['uri'] = subelem.text
                            elif subtag == 'computerSystemPlatform':
                                issue_comp_sys['platform'] = subelem.text
                            elif subtag == 'computerSystemOS':
                                issue_comp_sys['os'] = subelem.text
                            
                    #TODO: priority
                    
                    elif tag == "issueSeverity":
                        issue_severity = elem.text
                    
                    elif tag == "issueAssignedTo":
                        assignee_name = elem[0].text
                        assignee_id = elem[1].text
                        assignee_email = elem[2].text
                        
                        assignee = Person(assignee_name, assignee_email, 
                                          assignee_id)
                    
                    #issueCCPerson
                    elif tag == "issueCCPerson":
                        issue_cc_person = {}
                        for subelem in elem.iter(): 
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'uri':
                                issue_cc_person['uri'] = subelem.text
                            elif subtag == 'email':
                                issue_cc_person['email'] = subelem.text
                            elif subtag == 'id':
                                issue_cc_person['id'] = subelem.text
                            elif subtag == 'name':
                                issue_cc_person['name'] = subelem.text
                        issue_cc_persons.append(issue_cc_person)
                        
                    elif tag == "issueUrl":
                        issue_url = elem.text
                    
                    #TODO: dependsOnId
                    #TODO: blocksId
                    #TODO: duplicateOfId
                    #TODO: mergedIntoId
                    
                    elif tag == "issueDateOpened":
                        issue_date_opened = elem.text
                    
                    elif tag == "issueLastModified":
                        issue_last_modified = elem.text
                    
                    #Milestone
                    elif tag == 'issueMilestone':
                        issue_milestone = {}
                        for subelem in elem.iter(): 
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'milestoneUri':
                                issue_milestone['uri'] = subelem.text
                            elif subtag == 'milestoneId':
                                issue_milestone['id'] = subelem.text
                                
                    #Retrieve multiple comments
                    
                    elif tag == "issueComment":
                        issue_comment = {}
                        for subelem in elem.iter():
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'commentUri':
                                issue_comment['comment_uri'] = subelem.text
                            elif subtag == 'commentText':
                                issue_comment['comment_text'] = subelem.text
                            elif subtag == 'commentPerson':
                                issue_comment['commentor'] = {
                                    'uri': subelem[0].text,
                                    'name': subelem[3].text,
                                    'id': subelem[1].text,
                                    'email': subelem[2].text
                                    }
                            elif subtag == 'commentDate':
                                issue_comment['comment_date'] = datetime.strptime(subelem.text[:-6],
                                    "%a, %d %b %Y %H:%M:%S")
                                    #Wed, 1 Mar 2008 18:11:19 +0100
                            elif subtag == 'commentNumber':
                                issue_comment['comment_number'] = subelem.text
                                #print subelem.text
                        
                        if len(issue_comment) > 0:
                            issue_comments.append(issue_comment)
                                
                    #TODO: List of attachments
                    
                    #List of activities
                    elif tag == "issueActivity":
                        issue_activity = {}
                        for subelem in elem.iter():
                            subprefix, subtag = self.__get_tag(subelem)
                            if subtag == 'activityUri':
                                issue_activity['uri'] = subelem.text
                            elif subtag == 'activityWho':
                                issue_activity['who'] = subelem.text
                            elif subtag == 'activityWhen':
                                issue_activity['when'] = subelem.text
                            elif subtag == 'activityAdded':
                                issue_activity['added'] = subelem.text
                            elif subtag == 'activityRemoved':
                                issue_activity['removed'] = subelem.text
                            elif subtag == 'activityWhat':
                                issue_activity['what'] = subelem.text
                        
                        issue_activities.append(issue_activity)
                                
                    #TODO: Tracker
                    
                    # References to other items (locally stored)
                    elif tag == "references":
                        references = self.__load_references(elem)
                        
                
            # Build issue object, pack with info and return
            # Short_desc missing from event fields
            issue = Issue(issue_id, "", issue_description, issue_date_opened,
                        author)
            issue.set_assigned_to(assignee)
            issue.set_state(issue_state)
            issue.set_resolution(issue_resolution)
            issue.set_issue_url(issue_url)
            issue.set_last_modified(issue_last_modified)
            issue.milestone = issue_milestone
            issue.product = issue_product
            issue.computer_system = issue_comp_sys
            
            for person in issue_cc_persons:
                issue.add_cc_person(person)
            
            #print issue_comments
            
            # Order comments list before return
            if len(issue_comments) > 0:
                order_issue_comments = sorted(issue_comments, 
                                            key=lambda k: k['comment_date'])
            
            for item in order_issue_comments:
                item['comment_date']=item['comment_date'].strftime("%a, %d %b %Y %H:%M:%S")
                                            
            #print order_issue_comments
            
            #print order_issue_comments
            
            #for comment in order_issue_comments:
            for comment in order_issue_comments:
                issue.add_comment(comment)
                
                
            for activity in issue_activities:
                issue.add_activity(activity)
            
            issue_dict = {
                'issue_id': issue.get_issue_id(),
                'issue_author': {
                    'author_name': author.get_name(),
                    'author_email': author.get_email(),
                    'author_id': author.get_user_id()
                    },
                'issue_status': issue.get_state(),
                'issue_resolution': issue.get_resolution(),
                'issue_description': issue.get_description(),
                'issue_severity': issue.get_severity(),
                'issue_assigned_to': {
                    'assignee_name': assignee.get_name(),
                    'assignee_email': assignee.get_email(),
                    'assignee_id': assignee.get_user_id()
                    },
                'issue_url': issue.get_issue_url(),
                'issue_date_opened': issue.get_date_opened(),
                'issue_last_modified': issue.get_last_modified(),
                'issue_comments': issue.get_comments(),
                'issue_activities': issue.activities,
                'issue_milestone': issue.milestone,
                'issue_cc_people': issue.cc_people,
                'issue_product': issue.product,
                'issue_computer_system': issue.computer_system,
                }
            
            # Only include references in issue dict if we have identified items
            if len(references) > 0:
                issue_dict['references'] = references
            
            # Return the type of call and dict with issue attributes & values
            return api_call, issue_dict
        
        if api_call == "commit.getInfo":
            commit = {}
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                #nspace = elem.get(EventHandler.NS_MAP)
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                                
                    if tag == "commitRepositoryUri":
                        commit['uri'] = elem.text
                    
                    elif tag == "commitRevisionTag":
                        commit['rev_tag'] = elem.text
                    
                    elif tag == "commitAuthor":
                        author = {
                            'uri': elem[0].text,
                            'name': elem[1].text,
                            'id': elem[2].text,
                            'email': elem[3].text
                            }
                        commit['author'] = author
                    
                    elif tag == "commitCommiter":
                        commiter = {
                            'uri': elem[0].text,
                            'name': elem[1].text,
                            'id': elem[2].text,
                            'email': elem[3].text
                            }
                        commit['commiter'] = commiter
                        
                    elif tag == "commitDate":
                        commit['date'] = elem.text
                        
                    elif tag == "commitMessageLog":
                        commit['message_log'] = elem.text
                    
                    #TODO: Commit files
                    
                    elif tag == "commitProduct":
                        product = {
                            'uri': elem[0].text,
                            'id': elem[1].text,
                            'comp_uri': elem[2].text,
                            'comp_id': elem[3].text,
                            'version': elem[4].text
                            }
                        
                        commit['product'] = product
                    
                    elif tag == "references":
                        references = self.__load_references(elem)
                        commit['references'] = references
                    
            return api_call, commit
        
        elif api_call == "issue.getOpen":
            list_issues = []
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                    if tag == "issue":
                        #list_issues.append(Issue(elem[2].text, 
                                                 #"", elem[3].text, 
                                                 #"", None) )
                        #list_issues[len(list_issues)-1].set_issue_url(
                                                        #elem[0].text)
                        #uri = elem[0]; ur1 = elem[1] 
                        #id_issue = elme[2]; desc = elem[3]
                        issue = {
                            'issue_id': elem[2].text,
                            'issue_uri': elem[0].text,
                            'issue_url': elem[1].text,
                            'desc': elem[3].text}
                        list_issues.append(issue)
                        
            return api_call, list_issues
        
        elif api_call == "issue.getAllForProduct":
            list_issues = []
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                    if tag == "issue":
                        # url = elem[0] id = elem[1]; desc = elem[2]
                        #list_issues.append(Issue(elem[1].text, 
                                                 #"", elem[2].text, 
                                                 #"", None) )
                        #list_issues[len(list_issues)-1].set_issue_url(
                                                        #elem[0].text)
                        issue = {
                            'issue_id': elem[1].text,
                            'issue_url': elem[0].text,
                            'desc': elem[2].text
                            }
                        list_issues.append(issue)
                        
            return api_call, list_issues
        
        #######
        #######
        elif api_call == "issue.getAllForMethod":
            list_methods = []
             # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                    if tag == "method":
                        method = {
                            'uri': elem[0].text
                            }
                        if len(elem) > 1:
                            issues = []
                            for method_issue in elem.iterchildren():
                                issue = {}
                                for child in method_issue.iterchildren(tag=etree.Element):
                                    child_prefix, child_tag = self.__get_tag(child)
                                    if child_tag == 'issueUri':
                                        issue['uri'] = child.text
                                    elif child_tag == 'relationLevel':
                                        issue['relation_level'] = child.text
                                issues.append(issue)
                            # Add list of related issues to method
                            method['issues'] = issues
                        # Insert new method in result list
                        list_methods.append(method)
                        
            return api_call, list_methods
        
        elif api_call == "commit.getAllForProduct":
            list_commits = []
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                    if tag == "commit":
                        # uri = elem[0] message = elem[1]; date = elem[2]
                        #list_commits.append(Commit(elem[1].text, 
                                                 #elem[2].text, "",
                                                 #None, None) )  
                        commit = {
                            'uri': elem[0].text,
                            'message': elem[1].text, 
                            'date': elem[2].text,
                            'file_num': elem[4].text
                            }
                        # Retrieve commit author info
                        author = elem[3]
                        author = {
                            'uri': author[0].text,
                            'name': author[1].text,
                            'id': author[2].text,
                            'email': author[3].text
                            }
                        # Add author info to commit
                        commit['author'] = author    
                        list_commits.append(commit)
                        
            return api_call, list_commits
        
        #####
        #####
        elif api_call == "method.getAllForIdentity":
            list_files = []
            # Iterate only over etree.Element
            for elem in self.tree.iter(tag=etree.Element):
                nspace = elem.nsmap
                prefix, tag = self.__get_tag(elem)
                
                # If namespace matched, retrieve all relevant fields
                # and build new Issue object
                if nspace.has_key(EventHandler.PRE_S3) and\
                                    prefix == nspace[EventHandler.PRE_S3]:
                    if tag == "file":
                        f = {
                            'uri': elem[0].text,
                            'name': elem[1].text,
                            'branch': elem[2].text
                            }
                        list_modules = []
                        for k in range(3, len(elem)):
                            file_module = elem[k]
                            list_methods = []
                            module = {
                                'uri': file_module[0].text,
                                'name': file_module[1].text
                                }
                            for i in range(2, len(file_module)):
                                module_method = file_module[i]
                                method = {
                                    'uri': module_method[0].text,
                                    'name': module_method[1].text
                                    }
                                list_methods.append(method)
                            # Add list of all methods for this module
                            module['methods'] = list_methods
                            # Append new complete module to file modules
                            list_modules.append(module)
                        # Assign the list of modules for this file    
                        f['modules'] = list_modules
                        list_files.append(f)
                        
            return api_call, list_files
    
    def __load_references(self, elem):
        references = {}
        issue_refs = []
        commit_refs = []
        email_refs = []
        forum_refs = []
        
        for subelem in elem.iter():
            subprefix, subtag = self.__get_tag(subelem)
            if subtag == 'issue':
                issue_item_uri = ''
                for issueelem in subelem.iter():
                    issueprefix, issuetag = self.__get_tag(issueelem)
                    if issuetag == 'issueUri':
                        issue_item_uri = issueelem.text
                    elif issuetag == 'issueDescription':
                        issue_refs.append((issue_item_uri, issueelem.text))
                
            elif subtag == 'commit':
                commit_uri = ''
                for commit in subelem.iter():
                    commitprefix, committag = self.__get_tag(commit)
                    if committag == 'commitUri':
                        commit_uri = commit.text
                    elif committag == 'commitMessageLog':
                        commit_refs.append((commit_uri, commit.text))
            
            elif subtag == 'email':
                email_uri = ''
                for email in subelem.iter():
                    emailprefix, emailtag = self.__get_tag(email)
                    if emailtag == 'emailUri':
                        email_uri = email.text
                    elif emailtag == 'subject':
                        email_refs.append((email_uri, email.text))
            
            elif subtag == 'forumPost':
                post_uri = ''
                for post in subelem.iter():
                    postprefix, posttag = self.__get_tag(post)
                    if posttag == 'postUri':
                        post_uri = post.text
                    elif posttag == 'subject':
                        forum_refs.append((post_uri, post.text))
            
        if len(issue_refs) > 0:
            references['issues'] = issue_refs
        if len(commit_refs) > 0:
            references['commits'] = commit_refs
        if len(email_refs) > 0:
            references['emails'] = email_refs
        if len(forum_refs) > 0:
            references['posts'] = forum_refs
            
        return references
        
    def __load_keui_response(self):
        """
        Load response events from KEUI
        """
        # List of tuples 
        # (threads, similarity coef. and item ids)
        thread_list = []
        # List of dicts with all issue parameters
        issue_list = []
        max_count = 0
        
        for elem in self.tree.iter(tag=etree.Element):
            print elem.tag
            #print elem.attrib
            if elem.tag == "info":
                max_count = int(elem.get('maxCount'))
                print "Num items in KEUI response = " + str(max_count)
            
            if elem.tag == "thread":
                print elem.attrib
                thread_list.append({'id': elem.attrib.get("id"),
                                    'sim': elem.attrib.get("sim"),
                                    'item_ids': elem.attrib.get("itemIds")})
            
            if elem.tag == "items":
                for i in range(0, max_count):
                    # Explicit cast to dict needed to avoid JSON serialization
                    # error in search API
                    new_issue = dict(elem[i].attrib)
                    # Get metadata and short content
                    for subelem in elem[i].iter():
                        if subelem.tag == "metaData":
                            if subelem.text is not None:
                                new_issue['metaData'] = subelem.text
                            else:
                                new_issue['metaData'] = ""
                        elif subelem.tag == "shortContent":
                            new_issue['shortContent'] = subelem.text
                        elif subelem.tag == "subject":
                            new_issue['subject'] = subelem.text
                        elif subelem.tag == "similarity":
                            new_issue['similarity'] = subelem.text
                        elif subelem.tag == "issueId":
                            new_issue['issueId'] = subelem.text
                    issue_list.append(new_issue)
        
        if len(thread_list) > 0 and len(issue_list) > 0:
            return 'similar_issues', issue_list
        elif len(issue_list) > 0:
            return 'keywords_issues', issue_list
    
    def __load_new_issue(self):
        issue_id = ''
        issue_state = ''
        issue_resolution = ''
        issue_description = ''
        issue_severity = ''
        issue_url = ''
        issue_date_opened = ''
        issue_last_modified = ''
        issue_comment = ''
        
        # Iterate only over etree.Element
        for elem in self.tree.iter(tag=etree.Element):
            #nspace = elem.get(EventHandler.NS_MAP)
            nspace = elem.nsmap
            prefix, tag = self.__get_tag(elem)
            
            # If namespace matched, retrieve all relevant fields
            # and build new Issue object
            if nspace.has_key(EventHandler.PRE_S) and\
                                prefix == nspace[EventHandler.PRE_S]:
                               
                if tag == "issueId":
                    issue_id = elem.text
                
                #TODO: reporter
                
                elif tag == "status":
                    issue_state = elem.text
                            
                elif tag == "resolution":
                    issue_resolution = elem.text
                
                elif tag == "description":
                    issue_description = elem.text
                
                #TODO: keyword
                #TODO: product
                #TODO: computer system
                #TODO: priority
                
                elif tag == "severity":
                    issue_severity = elem.text
                            
                #TODO: issue_CC_person
                
                elif tag == "issueUrl":
                    issue_url = elem.text
                
                #TODO: dependsOnId
                #TODO: blocksId
                #TODO: duplicateOfId
                #TODO: mergedIntoId
                
                elif tag == "dateOpened":
                    issue_date_opened = elem.text
                
                elif tag == "lastModified":
                    issue_last_modified = elem.text
                
                #TODO: milestone
                
                #TODO: Retrieve multiple comments
                
                elif tag == "issueComment":
                    issue_comment = elem.text
                            
                #TODO: List of attachments
                #TODO: List of activities
                #TODO: Tracker
            
        # Build issue object, pack with info and return
        # Short_desc missing from event fields
        issue = Issue(issue_id, "", issue_description, issue_date_opened,
                      None)
                    
        issue.set_state(issue_state)
        issue.set_resolution(issue_resolution)
        issue.set_issue_url(issue_url)
        issue.set_last_modified(issue_last_modified)
        issue.add_comment(issue_comment)
        
        return issue
