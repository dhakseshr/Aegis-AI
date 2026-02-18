"""Kafka producer — async JSON publisher."""
import json, os
from confluent_kafka import Producer

_producer = None

def _get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer({"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")})
    return _producer

def publish(topic: str, key: str, value: dict):
    try:
        p = _get_producer()
        p.produce(topic, key=key, value=json.dumps(value).encode())
        p.flush(timeout=2)
    except Exception as e:
        print(f"[Kafka] publish error: {e}")
