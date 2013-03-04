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
from pyactivemq import DeliveryMode


class EventPublisher:

    def __init__(self, topicName):

        ## FIXME to be read from configuration file
        self.url = 'tcp://localhost:61616'
        ##

        connectionFactory = pyactivemq.ActiveMQConnectionFactory(self.url)
        self.connection = connectionFactory.createConnection()
        #transacted = True
        self.session = self.connection.createSession(
            AcknowledgeMode.AUTO_ACKNOWLEDGE)
        topic = self.session.createTopic(topicName)
        self.producer = self.session.createProducer(topic)
        self.producer.deliveryMode = DeliveryMode.NON_PERSISTENT

        self.startindex = 0

    def publishMessage(self, data):
        #
        # it just publishes the data via the producer
        #
        message = self.session.createTextMessage()
        message.text = data
        self.producer.send(message)

    def testMessages(self):
        #
        # it sends three simple messages
        #
        NUMMSGS = 3
        MSG_TEXT = 'Here is a message'
        message = self.session.createTextMessage()
        for i in xrange(self.startindex, self.startindex + NUMMSGS):
            message.text = MSG_TEXT + ' %d' % (i + 1)
            print 'PUBLISHER: Publishing message: ' + message.text
            self.producer.send(message)
        self.startindex = self.startindex + NUMMSGS

    def finish(self):
        self.connection.close()
