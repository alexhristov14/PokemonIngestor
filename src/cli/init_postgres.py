import common.models.postgres_models as models
from common.database.postgres import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized with tables.")


if __name__ == "__main__":
    init_db()
