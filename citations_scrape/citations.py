import sys
import json
import requests
from bs4 import BeautifulSoup
import unicodedata
from headers import *
import base64
import os

from google.cloud import pubsub_v1


def scrape_citations():
    URL = "http://www.values.com/inspirational-quotes"
    r = requests.get(URL)
  
    soup = BeautifulSoup(r.content, 'html5lib')
    #print(r)
  
    quotes=[]  # a list to store quotes
  
    table = soup.find('div', attrs = {'id':'all_quotes'})
    #print(table)
  
    for row in table.findAll('div',
                         attrs = {'class':'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'}):
        quote = {}
        #print(row.a['href'])
        quote['theme'] = row.h5.text
        quote['url'] = row.a['href']
        quote['img'] = row.img['src']
        quote['lines'] = row.img['alt'].split(" #")[0]
        quote['author'] = row.img['alt'].split(" #")[1]
        quotes.append(quote)
    #print(quotes)
    publish_to_pubsub(json.dumps(quotes))
    return json.dumps(quotes)


def publish_to_pubsub(message):

    # Instantiates a Pub/Sub client
    publisher = pubsub_v1.PublisherClient()
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

    topic_name = os.environ.get("TOPIC")

    if not topic_name or not message:
        return ('Missing "topic" and/or "message" parameter.', 400)

    print(f'Publishing message to topic {topic_name}')

    # References an existing topic
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)

    message_json = json.dumps({
        'data': {'message': message},
    })
    message_bytes = message_json.encode('utf-8')

    # Publishes a message
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Message published.'
    except Exception as e:
        print(e)
        return (e, 500)
