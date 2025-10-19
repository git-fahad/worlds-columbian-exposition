-- Test Queries for TimescaleDB

-- 1. Recent pavilion data (last 10 minutes)
SELECT
    time,
    pavilion_id,
    visitor_count,
    temperature_f,
    wait_time_minutes,
    operational_status
FROM sensor_data
WHERE time > NOW() - INTERVAL '10 minutes'
ORDER BY time DESC
LIMIT 50;

-- 2. Average visitors per pavilion (last hour)
SELECT
    pavilion_id,
    COUNT(*) as measurements,
    AVG(visitor_count)::INTEGER as avg_visitors,
    MAX(visitor_count) as peak_visitors,
    AVG(wait_time_minutes)::INTEGER as avg_wait_time
FROM sensor_data
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY pavilion_id
ORDER BY avg_visitors DESC;

-- 3. Crowded pavilions alert
SELECT
    time,
    pavilion_id,
    visitor_count,
    wait_time_minutes
FROM sensor_data
WHERE operational_status = 'crowded'
  AND time > NOW() - INTERVAL '30 minutes'
ORDER BY time DESC;

-- 4. Visitor entry/exit summary
SELECT
    DATE_TRUNC('hour', time) as hour,
    event_type,
    COUNT(*) as count
FROM visitor_events
WHERE time > NOW() - INTERVAL '6 hours'
GROUP BY hour, event_type
ORDER BY hour DESC, event_type;

-- 5. Ferris wheel operational summary
SELECT
    time_bucket('5 minutes', time) as bucket,
    AVG(rotation_speed_rpm)::NUMERIC(5,2) as avg_speed,
    AVG(passenger_count)::INTEGER as avg_passengers,
    MAX(vibration_level)::NUMERIC(5,3) as max_vibration
FROM ferris_wheel_data
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY bucket
ORDER BY bucket DESC;

-- 6. Hourly aggregate (from materialized view)
SELECT * FROM hourly_pavilion_stats
WHERE bucket > NOW() - INTERVAL '24 hours'
ORDER BY bucket DESC, pavilion_id;

-- 7. Count all messages
SELECT
    'Pavilion Sensors' as source, COUNT(*) as count FROM sensor_data
UNION ALL
SELECT 'Visitor Events', COUNT(*) FROM visitor_events
UNION ALL
SELECT 'Ferris Wheel', COUNT(*) FROM ferris_wheel_data;