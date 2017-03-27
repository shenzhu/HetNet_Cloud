class table:
	LOGIN = "CREATE TABLE IF NOT EXISTS login (device_id text, password text NOT NULL, email text NOT NULL,PRIMARY KEY (device_id));"
	NETWORK = "CREATE TABLE IF NOT EXISTS networks (ssid text, bandwidth text NOT NULL, AvgSS integer NOT NULL,device_id text REFERENCES login, PRIMARY KEY (ssid,location));"