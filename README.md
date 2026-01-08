just a basic data engineering project in order to track pokemon cards and their respective for each grade 7 and up.

Creating a table for the prices in raw format.

```sql
create table raw_card_prices  (
    card_id serial primary key,
    card_name text,
    set_name text,
    raw_price real,
    grade7_price real,
    grade8_price real,
    grade9_price real,
    grade9_5_price real,
    grade10_price real,
    scraped_at timestamp,
    ingested_at timestamp default now()
);
```


Init the airflow db and create the admin user in order to access from localhost:8080

```bash
docker compose up airflow-db -d
docker compose run --rm airflow-webserver airflow db init
docker compose run --rm airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```
