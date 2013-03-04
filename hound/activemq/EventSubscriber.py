#!/usr/bin/env python

# Copyright 2007 Albert Strasheim <fullung@gmail.com>
# Copyright 2012 GSyC/LibreSoft, Universidad Rey Juan Carlos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This example corresponds to DurableSubscriberExample.java from the
# Java EE 5 Tutorial, Chapter 31, Creating Robust JMS Applications.
#

import pyactivemq
from pyactivemq import AcknowledgeMode
from threading import Event

from tempfile import mktemp

class EventSubscriber:
    class TextListener(pyactivemq.MessageListener):
        def __init__(self):
            pyactivemq.MessageListener.__init__(self)
            self.monitor = Event()

        def onMessage(self, message):
            # Called asynchronously when a new message is received,
            # the message reference can be to any other Message types.

            if isinstance(message, pyactivemq.TextMessage):
                print "onMessage" #DELETEME
                print 'SUBSCRIBER: Reading Message: ' + message.text
                fd = open(mktemp(dir="/tmp/alert"), "w")
                print "--> stored in " + fd.name
                fd.write(message.text)
                fd.close()
            else:
                print "onMessage else" #DELETEME
                self.monitor.set()

    def __init__(self, topicName):
        url = 'tcp://localhost:61616'
        connectionFactory = pyactivemq.ActiveMQConnectionFactory(url)
        connection = connectionFactory.createConnection()
        # XXX should throw without this
        #connection.clientID = 'client1234'
        session = connection.createSession(AcknowledgeMode.AUTO_ACKNOWLEDGE)
        topic = session.createTopic(topicName)
        self.connection = connection
        self.session = session
        self.topic = topic

    def startSubscriber(self):
        print 'Starting subscriber'
        self.connection.stop()
        
        #Creates a durable subscriber to the specified topic, using a message selector.
        #subscriber = self.session.createDurableConsumer(self.topic, "MakeItLast", '', False)

        #If we create a durable subscriber, messages are not dequeued!
        #subscriber = self.session.createConsumer(self.topic, '', False)
        subscriber = self.session.createDurableConsumer(self.topic, 'MakeItLast','', False)
        
        listener = self.TextListener()
        subscriber.messageListener = listener
        self.subscriber = subscriber
        self.connection.start()
        print "connection started"  # DELETEME

    def closeSubscriber(self):
        subscriber = self.subscriber
        listener = subscriber.messageListener
        listener.monitor.wait()
        print 'Closing subscriber'
        subscriber.close()

    def finish(self):
        #no longer needed
        #self.session.unsubscribe("MakeItLast")
        self.session.unsubscribe("MakeItLast")
        self.connection.close()
