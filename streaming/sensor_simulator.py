"""
Chicago World's Fair - IoT Sensor Simulator
Generates realistic sensor data and publishes to Kafka
"""

import time
import random
import json
from datetime import datetime, timezone
from typing import Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SensorSimulator:
    """Simulates IoT sensors at the Chicago World's Fair"""

    def __init__(self, kafka_bootstrap_servers='localhost:9092'):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',  # Wait for all replicas
                retries=3
            )
            logger.info("✅ Connected to Kafka")
        except KafkaError as e:
            logger.error(f"❌ Failed to connect to Kafka: {e}")
            raise

        # Pavilion configurations
        self.pavilions = {
            'ferris_wheel': {
                'base_visitors': 300,
                'variance': 150,
                'base_temp': 72,
                'base_wait': 25
            },
            'palace_of_fine_arts': {
                'base_visitors': 200,
                'variance': 100,
                'base_temp': 70,
                'base_wait': 10
            },
            'electricity_building': {
                'base_visitors': 250,
                'variance': 120,
                'base_temp': 75,
                'base_wait': 15
            },
            'manufactures_building': {
                'base_visitors': 180,
                'variance': 90,
                'base_temp': 71,
                'base_wait': 12
            },
            'transportation_building': {
                'base_visitors': 220,
                'variance': 110,
                'base_temp': 73,
                'base_wait': 18
            }
        }

        # Gate IDs
        self.gates = ['north_entrance_1', 'north_entrance_2', 'south_entrance_1',
                      'east_entrance_1', 'west_entrance_1']

        # Ticket types
        self.ticket_types = ['general', 'season_pass', 'group', 'student']

    def generate_pavilion_data(self, pavilion_id: str) -> Dict[str, Any]:
        """Generate sensor data for a pavilion"""
        config = self.pavilions[pavilion_id]

        # Add time-of-day variations
        hour = datetime.now().hour
        time_multiplier = 1.0
        if 10 <= hour < 14:  # Peak hours
            time_multiplier = 1.5
        elif hour < 9 or hour > 18:  # Off-peak
            time_multiplier = 0.5

        visitor_count = int(config['base_visitors'] * time_multiplier +
                            random.randint(-config['variance'], config['variance']))
        visitor_count = max(0, visitor_count)  # No negative visitors

        # Determine operational status
        if visitor_count > config['base_visitors'] * 1.8:
            status = 'crowded'
        elif visitor_count < config['base_visitors'] * 0.3:
            status = 'quiet'
        else:
            status = 'normal'

        data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'pavilion_id': pavilion_id,
            'visitor_count': visitor_count,
            'temperature_f': round(config['base_temp'] + random.uniform(-3, 3), 2),
            'humidity_percent': round(random.uniform(40, 65), 2),
            'wait_time_minutes': max(0, int(config['base_wait'] + random.randint(-5, 10))),
            'operational_status': status,
            'metadata': {
                'sensor_id': f"sensor_{pavilion_id}_{random.randint(1, 5)}",
                'battery_level': round(random.uniform(75, 100), 1),
                'signal_strength': random.randint(3, 5)
            }
        }

        return data

    def generate_visitor_event(self) -> Dict[str, Any]:
        """Generate visitor entry/exit event"""
        data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'gate_id': random.choice(self.gates),
            'event_type': random.choice(['entry', 'exit']),
            'ticket_type': random.choice(self.ticket_types),
            'visitor_id': f"visitor_{random.randint(10000, 99999)}",
            'metadata': {
                'scan_duration_ms': random.randint(100, 500)
            }
        }

        return data

    def generate_ferris_wheel_data(self) -> Dict[str, Any]:
        """Generate Ferris wheel operational data"""
        cart_id = random.randint(1, 36)  # 36 carts on the wheel

        # Simulate rotation cycle (0-264 feet)
        cycle_position = (time.time() % 180) / 180  # 3-minute rotation
        current_height = 264 * abs(2 * cycle_position - 1)  # Triangle wave

        data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'cart_id': cart_id,
            'rotation_speed_rpm': round(random.uniform(0.3, 0.4), 3),
            'current_height_feet': round(current_height, 2),
            'passenger_count': random.randint(0, 60),  # Max 60 per cart
            'vibration_level': round(random.uniform(0.01, 0.05), 3),
            'operational_status': random.choice(['running', 'running', 'running', 'boarding']),
            'metadata': {
                'maintenance_due_hours': random.randint(100, 500),
                'last_inspection': (datetime.now(timezone.utc).replace(hour=0, minute=0)).isoformat()
            }
        }

        return data

    def send_to_kafka(self, topic: str, key: str, data: Dict[str, Any]):
        """Send data to Kafka topic"""
        try:
            future = self.producer.send(topic, key=key, value=data)
            record_metadata = future.get(timeout=10)
            logger.debug(f"✅ Sent to {topic}: partition={record_metadata.partition}, offset={record_metadata.offset}")
            return True
        except KafkaError as e:
            logger.error(f"❌ Failed to send to {topic}: {e}")
            return False

    def run(self, interval_seconds=5):
        """Main simulation loop"""
        logger.info("🚀 Starting sensor simulation...")
        logger.info(f"📊 Monitoring {len(self.pavilions)} pavilions")
        logger.info(f"🎡 Tracking Ferris wheel operations")
        logger.info(f"🚪 Monitoring {len(self.gates)} entry/exit gates")
        logger.info(f"⏱️  Sending data every {interval_seconds} seconds")

        iteration = 0

        try:
            while True:
                iteration += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Generate pavilion sensor data
                for pavilion_id in self.pavilions:
                    data = self.generate_pavilion_data(pavilion_id)
                    self.send_to_kafka('pavilion-sensors', pavilion_id, data)

                # Generate visitor events (more frequent)
                for _ in range(random.randint(3, 8)):
                    event = self.generate_visitor_event()
                    self.send_to_kafka('visitor-events', event['gate_id'], event)

                # Generate Ferris wheel data
                wheel_data = self.generate_ferris_wheel_data()
                self.send_to_kafka('ferris-wheel-ops', str(wheel_data['cart_id']), wheel_data)

                if iteration % 10 == 0:
                    logger.info(f"📈 [{timestamp}] Iteration {iteration} - All sensors operational")

                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping simulation...")
        finally:
            self.producer.close()
            logger.info("✅ Kafka producer closed")


if __name__ == '__main__':
    # Configuration
    KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
    INTERVAL_SECONDS = 5  # Send data every 5 seconds

    simulator = SensorSimulator(kafka_bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    simulator.run(interval_seconds=INTERVAL_SECONDS)