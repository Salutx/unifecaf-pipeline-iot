-- ============================================================
--           Pipeline de Dados IoT - UniFECAF
-- ============================================================

CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    ROUND(AVG(temperature)::numeric, 2)  AS avg_temp,
    ROUND(MIN(temperature)::numeric, 2)  AS min_temp,
    ROUND(MAX(temperature)::numeric, 2)  AS max_temp,
    COUNT(*)                             AS total_leituras
FROM temperature_readings
GROUP BY device_id
ORDER BY avg_temp DESC;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM reading_timestamp)::int AS hora,
    COUNT(*)                                  AS contagem,
    ROUND(AVG(temperature)::numeric, 2)       AS avg_temp_hora
FROM temperature_readings
GROUP BY hora
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(reading_timestamp)              AS data,
    ROUND(MAX(temperature)::numeric, 2)  AS temp_max,
    ROUND(MIN(temperature)::numeric, 2)  AS temp_min,
    ROUND(AVG(temperature)::numeric, 2)  AS temp_media,
    COUNT(*)                             AS leituras_dia
FROM temperature_readings
GROUP BY DATE(reading_timestamp)
ORDER BY data;
