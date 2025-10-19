#!/bin/bash

echo "Starting Chicago World's Fair Streaming Pipeline"
echo ""

if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

echo "Starting Docker containers..."
docker-compose -f docker-compose.yml up -d

echo "Waiting for services to start..."
sleep 15

echo "🔍 Checking Kafka..."
docker exec chicago_kafka kafka-topics --bootstrap-server localhost:9093 --list

echo "📝 Creating Kafka topics..."
docker exec chicago_kafka kafka-topics --bootstrap-server localhost:9093 --create --topic pavilion-sensors --partitions 3 --replication-factor 1 --if-not-exists
docker exec chicago_kafka kafka-topics --bootstrap-server localhost:9093 --create --topic visitor-events --partitions 3 --replication-factor 1 --if-not-exists
docker exec chicago_kafka kafka-topics --bootstrap-server localhost:9093 --create --topic ferris-wheel-ops --partitions 2 --replication-factor 1 --if-not-exists

echo ""
echo "Streaming infrastructure is ready!"
echo ""
echo "Access points:"
echo "  - Kafka UI: http://localhost:8080"
echo "  - Grafana: http://localhost:3000 (admin/admin123)"
echo "  - TimescaleDB: localhost:5433"
echo ""
echo "To start simulation:"
echo "  python streaming/sensor_simulator.py"
echo ""
echo "To start processor:"
echo "  python streaming/stream_processor.py"
echo ""