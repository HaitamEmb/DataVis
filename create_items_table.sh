set -eux

path=''

if [ -f ./.env ]; then
	export $(grep -v "^#" ./.env | xargs)
else
	echo "No .env file found, Please create one";
	exit 2;
fi

echo "Loading and creating items table"

#check for psql

if !command -v psql &> /dev/null; then
	echo "Error: psql is not installed!"
	exit 2;
else
	echo "Creating..."
fi

#load and create items table

psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
	DROP TABLE IF EXISTS items;
	CREATE TABLE IF NOT EXISTS items (
		product-id	INTEGER,
		category_id	BIGINT,
		category_code	TEXT,
		brand		VARCHAR(255)
	);
	COPY items
	FROM ''
	DELIMITER ','
	CSV HEADER
	NULL AS '';
"
#check items and customers are existant before fusion

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "

	DO \$\$
	BEGIN
		IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'customers') THEN
			RAISE EXCEPTION 'ERROR: Table \"customers\" is non existant.';
		END IF;

		IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'items') THEN
			RAISE EXCEPTION 'ERROR: Table \"items\" is non existant.';
		END IF;

	END \$\$;
"

#fusion; Here we will use LEFT JOIN intead of INNER JOIN, to prevent any data loss
#If we ever have a case empty or missing, we will not get rid off the whole remaining info
#it will be retained.

psql -U "$POSTGRESS_USER" -d "$POSTGRESS_DB" -c "

	DROP TABLE IF EXISTS fusion_table;
	--make a temp table with the joined data
	CREATE TABLE fusion_table AS
	SELECT
		c.event_time,
		c.event_type,
		c.product_id,
		c.price,
		c.user_id,
		c.user_session,
		i.category_id,
		i.category_code,
		i.brand
	FROM customers c
	--we use SELECT DISTINCT instead of SELECT to get only the different values
	LEFT JOIN (SELECT DISTINCT ON (product_id) product_id, category_id, category_code, brand FROM items ORDER BY product_id) i ON c.product_id = i.product_id;

	--drop old customers table
	DROP TABLE IF EXISTS customers;

	ALTER TABLE fusion_table RENAME TO customers;
"
echo "Fusion of the two tables has completed successfully"
