from utils.db_connection import get_connection


def create_database():
    connection = get_connection()

    with open("database/schema.sql", "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_database()