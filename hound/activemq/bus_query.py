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

import pyactivemq
import Queue
from pyactivemq import ActiveMQConnectionFactory, AcknowledgeMode


class MessageListener(pyactivemq.MessageListener):
    def __init__(self, name, queue):
        pyactivemq.MessageListener.__init__(self)
        self.name = name
        self.queue = queue

    def onMessage(self, message):
        #self.queue.put('%s got: %s' % (self.name, message.text))
        self.queue.put(message.text)


class BusQuery:

    def __init__(self, url, send_topic_name, message, receive_topic_name):

        f = ActiveMQConnectionFactory(url)
        self.conn = f.createConnection()
        self.send_topic_name = send_topic_name
        self.receive_topic_name = receive_topic_name
        self.message = message

        nmessages = 1
        nconsumers = 1

        self.consumers = []

        self._create_single_producer()

        # create infinite queue that is shared by consumers
        self.queue = Queue.Queue(0)

        self._create_single_consumer()

    def run(self):
        self.conn.start()
        self.producer.send(self.textMessage)

        """
        qsize = 1
        try:
            for i in xrange(qsize):
                message = self.queue.get(block=True, timeout=45)
                return message
        except Queue.Empty:
            raise AssertionError, 'Expected %d messages in queue' % qsize
        assert self.queue.empty()

        self.conn.close()
        """

        message = self.queue.get(block=True, timeout=45)
        self.conn.close()

        return message

    def _create_single_producer(self):
        producer_session = self.conn.createSession()
        topic = producer_session.createTopic(self.send_topic_name)
        self.producer = producer_session.createProducer(topic)
        self.textMessage = producer_session.createTextMessage(self.message)

    def _create_single_consumer(self):
        consumer_session = self.conn.createSession()
        topic = consumer_session.createTopic(self.receive_topic_name)
        self.consumer = consumer_session.createConsumer(topic)
        listener = MessageListener('consumer%d' % 1, self.queue)
        self.consumer.messageListener = listener
        self.consumers.append(self.consumer)
