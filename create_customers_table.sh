
set -eux

path="data_test/data/"

# Union query creating the table
UNION_QUERY=""
#file="test01.csv"
#load env variables and exports as args
if [ -f ./.env ]; then
	export $(grep -v '^#' ./.env | xargs)
else
	echo "No .env file, please make sure you make one";
	exit 2;
fi

mkdir -p data_test/data && cd data_test/data

wget https://cdn.intra.42.fr/document/document/33137/data_2023_feb.csv
wget https://cdn.intra.42.fr/document/document/42145/subject.zip
unzip subject.zip
mv ./subject/customer/*
mv ./subject/item/*
rm -rf subject subject.zip

#since I'm not using docker for this project
#we will need to check for the presence of psql
if ! command -v psql &> /dev/null; then
	echo "Error: psql is not installed"
	exit 2
fi

for file in data_test/data/data_202*.csv; do
	#check for file if it exists
	[ -e "$file" ] || continue
	echo "psql detected. Processing the command..."
	# create the table's name
	tablename=${file%.*}
	echo "Processing $tablename"
	#executing SQL commands to create table
	psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
		DROP TABLE IF EXISTS $tablename;
		CREATE TABLE $tablename (
			event_time TIMESTAMPTZ,
			event_type VARCHAR(255),
			product_id INTEGER,
			price FLOAT,
			user_id BIGINT,
			user_session TEXT
		);
		-- copy from csv to table
		COPY $tablename -- change to \copy
		FROM '/var/lib/postgresql/data/downloaded/$tablename.csv'
		DELIMITER ','
		CSV HEADER;
	"
	#checking for empty string UNION_QUERY to build
	#else UNION_ALL

	if [ -z "$UNION_QUERY" ]; then
		UNION_QUERY="SELECT * FROM $tablename"
	else
		UNION_QUERY="$UNION_QUERY UNION ALL SELECT * FROM $tablename"
	fi
done

echo "Creating customers table"

if [ -z "$UNION_QUERY" ]; then
	echo "Error: no data_202* files are found"
	exit 2
fi

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
	DROP TABLE IF EXISTS customers;
	CREATE TABLE IF NOT EXISTS customers AS $UNION_QUERY;
	"
echo "finished"
