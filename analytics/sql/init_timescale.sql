-- Create extension for TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Sensor data table
CREATE TABLE IF NOT EXISTS sensor_data (
    time TIMESTAMPTZ NOT NULL,
    pavilion_id VARCHAR(50) NOT NULL,
    visitor_count INTEGER,
    temperature_f NUMERIC(5,2),
    humidity_percent NUMERIC(5,2),
    wait_time_minutes INTEGER,
    operational_status VARCHAR(20),
    metadata JSONB
);

-- Convert to hypertable (TimescaleDB optimization)
SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_pavilion_time ON sensor_data (pavilion_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_status ON sensor_data (operational_status, time DESC);

-- Visitor entry/exit events table
CREATE TABLE IF NOT EXISTS visitor_events (
    time TIMESTAMPTZ NOT NULL,
    gate_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(20) NOT NULL, -- 'entry' or 'exit'
    ticket_type VARCHAR(30),
    visitor_id UUID,
    metadata JSONB
);

SELECT create_hypertable('visitor_events', 'time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_gate_time ON visitor_events (gate_id, time DESC);

-- Ferris wheel operations table
CREATE TABLE IF NOT EXISTS ferris_wheel_data (
    time TIMESTAMPTZ NOT NULL,
    cart_id INTEGER NOT NULL,
    rotation_speed_rpm NUMERIC(5,2),
    current_height_feet NUMERIC(6,2),
    passenger_count INTEGER,
    vibration_level NUMERIC(5,3),
    operational_status VARCHAR(20),
    metadata JSONB
);

SELECT create_hypertable('ferris_wheel_data', 'time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_cart_time ON ferris_wheel_data (cart_id, time DESC);

-- Create materialized view for hourly aggregations
CREATE MATERIALIZED VIEW IF NOT EXISTS hourly_pavilion_stats
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    pavilion_id,
    AVG(visitor_count) as avg_visitors,
    MAX(visitor_count) as peak_visitors,
    AVG(temperature_f) as avg_temp,
    AVG(wait_time_minutes) as avg_wait_time,
    COUNT(*) as measurement_count
FROM sensor_data
GROUP BY bucket, pavilion_id
WITH NO DATA;

-- Refresh policy for continuous aggregation
SELECT add_continuous_aggregate_policy('hourly_pavilion_stats',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- Data retention policy (keep data for 90 days)
SELECT add_retention_policy('sensor_data', INTERVAL '90 days', if_not_exists => TRUE);
SELECT add_retention_policy('visitor_events', INTERVAL '90 days', if_not_exists => TRUE);
SELECT add_retention_policy('ferris_wheel_data', INTERVAL '90 days', if_not_exists => TRUE);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO timescale;