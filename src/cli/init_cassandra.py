from common.database.cassandra import session


def init_db():
    try:
        session.execute(
            """
            create table if not exists card_price_history (
            card_id text,
            scrape_id timeuuid,
            grade text,
            date date,
            price float,
            source text,
            primary key (card_id, grade, scrape_id)
            ) with clustering order by (grade ASC, scrape_id DESC);
        """
        )

        print("Created table card_price_history successfuly!")
    except Exception as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    init_db()
