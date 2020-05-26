import json

from kafka import KafkaProducer

from utils.common_config import kafka_host


class KafkaData(object):
    def __init__(self):
        self._producer = None

    def send_data(self, name, data):
        self._producer = KafkaProducer(bootstrap_servers=kafka_host,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        for dict_data in data:
            self._producer.send(name, dict_data)
        self._producer.flush()
        self._producer.close()
