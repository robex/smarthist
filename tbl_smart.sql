DROP TABLE IF EXISTS smarthist;

CREATE TABLE IF NOT EXISTS smarthist(
        id INTEGER NOT NULL,
	serial TEXT NOT NULL,
	ts INTEGER NOT NULL,
	is_ssd INTEGER NOT NULL,
	raw_read_error_rate INTEGER,
	power_on_hours INTEGER,
	power_cycle_count INTEGER,
	load_cycle_count INTEGER,
	temperature_celsius INTEGER,
	reallocated_event_count INTEGER,
	offline_uncorrectable INTEGER,
        PRIMARY KEY(id)
);

