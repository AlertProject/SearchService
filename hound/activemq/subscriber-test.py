#!/usr/bin/env python

from EventSubscriber import EventSubscriber
import pyactivemq

if __name__ == "__main__":
    url = 'tcp://localhost:61616'
    topicName = 'requete-topic-69'
    f = pyactivemq.ActiveMQConnectionFactory(url)
    durableSubscriber = EventSubscriber(f, topicName)
    durableSubscriber.startSubscriber()
    durableSubscriber.closeSubscriber()
    durableSubscriber.finish()
