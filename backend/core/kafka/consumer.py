"""Kafka consumer — topic subscription with callbacks."""
import json, os
from confluent_kafka import Consumer, KafkaError
from typing import Callable, Dict

TOPICS = ["incident-topic", "research-topic", "risk-topic",
          "resource-topic", "strategy-topic", "report-topic"]


class AegisConsumer:
    def __init__(self, group_id: str, topics: list):
        self.consumer = Consumer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        })
        self.consumer.subscribe(topics)
        self.handlers: Dict[str, Callable] = {}

    def register(self, topic: str, handler: Callable):
        self.handlers[topic] = handler

    def run(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        print(f"[Kafka] error: {msg.error()}")
                    continue
                topic = msg.topic()
                data = json.loads(msg.value().decode())
                if topic in self.handlers:
                    self.handlers[topic](data)
        finally:
            self.consumer.close()
