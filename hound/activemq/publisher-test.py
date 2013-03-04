#!/usr/bin/env python

from EventPublisher import EventPublisher

if __name__ == "__main__":
    topic_name = 'Monty Python and the Holy Grail'    
    pub = EventPublisher(topic_name)
    pub.publishMessage("<?xml version=\"1.0\" encoding=\"UTF-8\"?><s:Envelope xmlns:s=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:wsnt=\"http://docs.oasis-open.org/wsn/b-2\" xmlns:wsa=\"http://www.w3.org/2005/08/addressing\"><s:Header></s:Header><s:Body></s:Body></s:Envelope>")
    pub.finish()

    topic_name = 'The meaning of life'    
    pub = EventPublisher(topic_name)
    pub.publishMessage("<?xml version=\"1.0\" encoding=\"UTF-8\"?><s:Envelope xmlns:s=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:wsnt=\"http://docs.oasis-open.org/wsn/b-2\" xmlns:wsa=\"http://www.w3.org/2005/08/addressing\"><s:Header></s:Header><s:Body></s:Body></s:Envelope>")
    pub.finish()

    topic_name = 'Brian\'s life'
    pub = EventPublisher(topic_name)
    pub.testMessages()
    pub.finish()
    
    
