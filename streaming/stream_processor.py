"""
Chicago World's Fair - Kafka Stream Processor
Consumes sensor data from Kafka and writes to TimescaleDB
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import psycopg2
from psycopg2.extras import execute_values
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StreamProcessor:
    """Processes sensor data from Kafka and stores in TimescaleDB"""

    def __init__(
            self,
            kafka_bootstrap_servers='localhost:9092',
            timescale_config=None
    ):
        """Initialize Kafka consumer and database connection"""

        # Kafka Consumer
        try:
            self.consumer = KafkaConsumer(
                'pavilion-sensors',
                'visitor-events',
                'ferris-wheel-ops',
                bootstrap_servers=kafka_bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='latest',  # Start from latest message
                enable_auto_commit=True,
                group_id='chicago-fair-processor',
                max_poll_records=100
            )
            logger.info("✅ Connected to Kafka consumer")
        except KafkaError as e:
            logger.error(f"❌ Failed to connect to Kafka: {e}")
            raise

        # TimescaleDB Connection
        if timescale_config is None:
            timescale_config = {
                'host': 'localhost',
                'port': 5433,
                'database': 'chicago_timeseries',
                'user': 'timescale',
                'password': 'timescale123'
            }

        self.timescale_config = timescale_config
        self.db_conn = None
        self.connect_to_database()

        # Statistics
        self.stats = {
            'pavilion_messages': 0,
            'visitor_events': 0,
            'ferris_wheel_messages': 0,
            'errors': 0
        }

    def connect_to_database(self):
        """Establish database connection"""
        try:
            self.db_conn = psycopg2.connect(**self.timescale_config)
            self.db_conn.autocommit = False
            logger.info("✅ Connected to TimescaleDB")
        except psycopg2.Error as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    def reconnect_database(self):
        """Reconnect to database if connection is lost"""
        try:
            if self.db_conn:
                self.db_conn.close()
            self.connect_to_database()
        except Exception as e:
            logger.error(f"❌ Reconnection failed: {e}")
            time.sleep(5)  # Wait before retry

    def process_pavilion_data(self, data: Dict[str, Any]):
        """Process and store pavilion sensor data"""
        try:
            cursor = self.db_conn.cursor()

            sql = """
                INSERT INTO sensor_data 
                (time, pavilion_id, visitor_count, temperature_f, humidity_percent, 
                 wait_time_minutes, operational_status, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                data['timestamp'],
                data['pavilion_id'],
                data['visitor_count'],
                data['temperature_f'],
                data['humidity_percent'],
                data['wait_time_minutes'],
                data['operational_status'],
                json.dumps(data['metadata'])
            ))

            self.db_conn.commit()
            self.stats['pavilion_messages'] += 1

            # Check for alerts
            if data['operational_status'] == 'crowded':
                logger.warning(f"🚨 ALERT: {data['pavilion_id']} is crowded! "
                               f"Visitors: {data['visitor_count']}")

        except psycopg2.Error as e:
            logger.error(f"❌ Database error (pavilion): {e}")
            self.db_conn.rollback()
            self.stats['errors'] += 1
            self.reconnect_database()

    def process_visitor_event(self, data: Dict[str, Any]):
        """Process and store visitor entry/exit events"""
        try:
            cursor = self.db_conn.cursor()

            sql = """
                INSERT INTO visitor_events 
                (time, gate_id, event_type, ticket_type, visitor_id, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                data['timestamp'],
                data['gate_id'],
                data['event_type'],
                data['ticket_type'],
                data['visitor_id'],
                json.dumps(data['metadata'])
            ))

            self.db_conn.commit()
            self.stats['visitor_events'] += 1

        except psycopg2.Error as e:
            logger.error(f"❌ Database error (visitor): {e}")
            self.db_conn.rollback()
            self.stats['errors'] += 1
            self.reconnect_database()

    def process_ferris_wheel_data(self, data: Dict[str, Any]):
        """Process and store Ferris wheel operational data"""
        try:
            cursor = self.db_conn.cursor()

            sql = """
                INSERT INTO ferris_wheel_data 
                (time, cart_id, rotation_speed_rpm, current_height_feet, 
                 passenger_count, vibration_level, operational_status, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                data['timestamp'],
                data['cart_id'],
                data['rotation_speed_rpm'],
                data['current_height_feet'],
                data['passenger_count'],
                data['vibration_level'],
                data['operational_status'],
                json.dumps(data['metadata'])
            ))

            self.db_conn.commit()
            self.stats['ferris_wheel_messages'] += 1

            # Safety check
            if data['vibration_level'] > 0.04:
                logger.warning(f"⚠️ High vibration detected on cart {data['cart_id']}: "
                               f"{data['vibration_level']}")

        except psycopg2.Error as e:
            logger.error(f"❌ Database error (ferris wheel): {e}")
            self.db_conn.rollback()
            self.stats['errors'] += 1
            self.reconnect_database()

    def print_stats(self):
        """Print processing statistics"""
        total = sum([
            self.stats['pavilion_messages'],
            self.stats['visitor_events'],
            self.stats['ferris_wheel_messages']
        ])

        logger.info(f"\n📊 Processing Statistics:")
        logger.info(f"  Total messages: {total}")
        logger.info(f"  Pavilion sensors: {self.stats['pavilion_messages']}")
        logger.info(f"  Visitor events: {self.stats['visitor_events']}")
        logger.info(f"  Ferris wheel ops: {self.stats['ferris_wheel_messages']}")
        logger.info(f"  Errors: {self.stats['errors']}\n")

    def run(self):
        """Main processing loop"""
        logger.info("🚀 Starting stream processor...")
        logger.info("👂 Listening to Kafka topics...")

        message_count = 0

        try:
            for message in self.consumer:
                message_count += 1
                topic = message.topic
                data = message.value

                # Route to appropriate processor
                if topic == 'pavilion-sensors':
                    self.process_pavilion_data(data)
                elif topic == 'visitor-events':
                    self.process_visitor_event(data)
                elif topic == 'ferris-wheel-ops':
                    self.process_ferris_wheel_data(data)

                # Print stats every 100 messages
                if message_count % 100 == 0:
                    self.print_stats()

        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping processor...")
        finally:
            self.consumer.close()
            if self.db_conn:
                self.db_conn.close()
            logger.info("✅ Connections closed")
            self.print_stats()


if __name__ == '__main__':
    processor = StreamProcessor()
    processor.run()