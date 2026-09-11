from utils.db_connection import get_connection


def check_database():
    connection = get_connection()
    cursor = connection.cursor()

    tables = [
        "teams",
        "players",
        "venues",
        "series",
        "matches",
        "player_performance"
    ]

    print("\n===== DATABASE VERIFICATION =====\n")

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        print(f"{table}: {count} records")

    print("\n===== SAMPLE PLAYERS =====\n")

    cursor.execute("""
        SELECT player_id, full_name, country, playing_role
        FROM players
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    print("\n===== SAMPLE MATCHES =====\n")

    cursor.execute("""
        SELECT
            match_id,
            description,
            match_type,
            match_date
        FROM matches
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(row)

    connection.close()


if __name__ == "__main__":
    check_database()
    