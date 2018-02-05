while ! timeout 1 bash -c "echo > /dev/tcp/postgres/5432" 2>/dev/null; do
    trial_count=$((trial_count+1))
    if ((trial_count == 12)); then
        echo "Postgres took too long to start."
        exit 1
    fi
    sleep 5;
done

echo "Setting up database"
psql "$POSTGRES_URI" -f ./Database/create_listings.sql --quiet

pip install -q -r requirements.txt

flask run --host 0.0.0.0 --port $SERVER_PORT
