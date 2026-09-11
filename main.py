import sqlite3

DB_FILE = "database/cricket.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def show_players():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_id, full_name, country,
               playing_role, batting_style, bowling_style
        FROM players
        ORDER BY full_name
    """)

    rows = cursor.fetchall()

    print("\n========== PLAYERS ==========\n")

    for row in rows:
        print(row)

    conn.close()


def show_teams():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT team_id, team_name, country
        FROM teams
        ORDER BY team_name
    """)

    rows = cursor.fetchall()

    print("\n========== TEAMS ==========\n")

    for row in rows:
        print(row)

    conn.close()


def show_venues():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT venue_id, venue_name, city, country, capacity
        FROM venues
        ORDER BY venue_name
    """)

    rows = cursor.fetchall()

    print("\n========== VENUES ==========\n")

    for row in rows:
        print(row)

    conn.close()


def show_matches():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT match_id, description, match_type,
               team1_id, team2_id, winner_team_id,
               venue_id, match_date
        FROM matches
        ORDER BY match_date DESC
    """)

    rows = cursor.fetchall()

    print("\n========== MATCHES ==========\n")

    for row in rows:
        print(row)

    conn.close()


def search_player():
    name = input("\nEnter player name: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_id, full_name, country,
               playing_role, batting_style, bowling_style
        FROM players
        WHERE full_name LIKE ?
        ORDER BY full_name
    """, (f"%{name}%",))

    rows = cursor.fetchall()

    print("\n========== SEARCH RESULT ==========\n")

    if rows:
        for row in rows:
            print(row)
    else:
        print("No player found.")

    conn.close()


def player_statistics():
    player_id = input("\nEnter player ID: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT performance_id, match_id, player_id,
               runs, balls, strike_rate,
               wickets, overs, economy_rate,
               batting_position, innings,
               catches, stumpings
        FROM player_performance
        WHERE player_id = ?
    """, (player_id,))

    rows = cursor.fetchall()

    print("\n========== PLAYER STATISTICS ==========\n")

    if rows:
        for row in rows:
            print(row)
    else:
        print("No statistics found for this player.")

    conn.close()


def main():

    while True:

        print("\n")
        print("========================================")
        print("          CRICBUZZ LIVESTATS")
        print("========================================")
        print("1. View Players")
        print("2. View Teams")
        print("3. View Venues")
        print("4. View Matches")
        print("5. Search Player")
        print("6. View Player Statistics")
        print("0. Exit")
        print("========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_players()

        elif choice == "2":
            show_teams()

        elif choice == "3":
            show_venues()

        elif choice == "4":
            show_matches()

        elif choice == "5":
            search_player()

        elif choice == "6":
            player_statistics()

        elif choice == "0":
            print("\nThank you for using Cricbuzz LiveStats!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()