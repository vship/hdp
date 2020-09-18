#!/usr/bin/python3

from numpy.random import choice, randint
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError

def get_random_value():
    new_dict = {}

    branch_list = ['Soup', 'Burger', 'Pasta', 'Pizza']
    currency_list = ['RUB', 'USD', 'EUR', 'GBP']

    new_dict['food'] = choice(food_list)
    new_dict['currency'] = choice(currency_list)
    new_dict['amount'] = randint(1, 500)

    return new_dict


if __name__ == "__main__":

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:dumps(x).encode('utf-8'),
                             compression_type='gzip')

    my_topic = 'test'

    while True:  
        for _ in range(100):
            data = get_random_value()

            try:
                future = producer.send(topic = my_topic, value = data)
                record_metadata = future.get(timeout=10)
                
                print('--> The message has been sent to a topic: {}, partition: {}, offset: {}' \
                        .format(record_metadata.topic, 
                            record_metadata.partition, 
                            record_metadata.offset ))   
                                         
            except Exception as e:
                print('--> It seems an Error occurred: {}'.format(e))

            finally:
                producer.flush()

        sleep(1)

    producer.close()