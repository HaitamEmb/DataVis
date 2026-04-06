set -eux

if [ -f ./.env ]; then
	export $(grep -v "^#" | xargs)
else
	echo "No .env file found, please create one.";
	exit 2;
fi

echo "Removing duplicates..."

# we need to delete duplicates and 1-second interval matches using DELETE statement
# I'm using ctid as a way to distinct between two duplicates for removal
psq -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "

	DELETE FROM customers
	WHERE ctid IN (
		SELECT ctid
		FROM (
			SELECT ctid, event_time, event_time - LAG(event_time) OVER (
				PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_time
			) as time_diff
		FROM customers
		) sub
		WHERE time_diff <= interval '1 second'
	);
"
echo "Duplicates have been removed"