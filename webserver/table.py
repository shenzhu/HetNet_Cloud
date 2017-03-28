class table:
	LOGIN = "CREATE TABLE IF NOT EXISTS login (device_id text, password text NOT NULL, email text NOT NULL,PRIMARY KEY (device_id));"
	NETWORK = "CREATE TABLE IF NOT EXISTS networks (ssid text, bandwidth text NOT NULL, security text NOT NULL, location text NOT NULL,AvgSS integer NOT NULL,device_id text REFERENCES login, PRIMARY KEY (ssid,location));"
	APPLICATION = "CREATE TABLE IF NOT EXISTS application (name text, device_id text REFERENCES login,PRIMARY KEY (name,device_id));"
	APPDETL = "CREATE TABLE IF NOT EXISTS appdetl (access_time date, type text, name text REFERENCES application, value numeric, device_id text REFERENCES login,PRIMARY KEY (AccessTime, type));"
	# Type indicate the CPU/Battery/DataUsage
