class table:
	LOGIN = "CREATE TABLE IF NOT EXISTS login (device_id text, password text NOT NULL, email text NOT NULL,PRIMARY KEY (device_id));"
	NETWORK = "CREATE TABLE IF NOT EXISTS networks (ssid text, bandwidth text NOT NULL, security text NOT NULL, location text NOT NULL,AvgSS integer NOT NULL,device_id text REFERENCES login on delete cascade, PRIMARY KEY (ssid,location));"
	APPLICATION = "CREATE TABLE IF NOT EXISTS application (name text, device_id text REFERENCES login on delete cascade,PRIMARY KEY (name,device_id));"
	APPDETL = "CREATE TABLE IF NOT EXISTS appdetl (access_time date, type text, name text, interval numeric, value numeric, device_id text,PRIMARY KEY (access_time, type), FOREIGN KEY (name, device_id) REFERENCES application(name, device_id) on delete cascade);"
	# Type indicate the CPU/Battery/DataUsage

	"""
	psql \
   --host=hetpot.c8dtasexwftg.us-east-1.rds.amazonaws.com \
   --port=5432 \
   --username hetnet \
   --password hetnet123\
   --dbname=HetNet

	"""