from utils.db_connection import get_connection


def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------------
    # TEAMS
    # -------------------------------
    teams = [
        ("India", "India"),
        ("Australia", "Australia"),
        ("England", "England"),
        ("South Africa", "South Africa"),
        ("New Zealand", "New Zealand"),
        ("Pakistan", "Pakistan"),
        ("Sri Lanka", "Sri Lanka"),
        ("West Indies", "West Indies")
    ]

    cursor.executemany(
        """
        INSERT INTO teams (team_name, country)
        VALUES (?, ?)
        """,
        teams
    )

    # -------------------------------
    # PLAYERS
    # -------------------------------
    players = [
        ("Virat Kohli", "India", "Batsman",
         "Right-hand Bat", "Right-arm Medium"),
        ("Rohit Sharma", "India", "Batsman",
         "Right-hand Bat", "Right-arm Off Break"),
        ("Jasprit Bumrah", "India", "Bowler",
         "Right-hand Bat", "Right-arm Fast"),
        ("Ravindra Jadeja", "India", "All-rounder",
         "Left-hand Bat", "Left-arm Orthodox"),
        ("Rishabh Pant", "India", "Wicket-keeper",
         "Left-hand Bat", "Right-arm Medium"),
        ("Steve Smith", "Australia", "Batsman",
         "Right-hand Bat", "Right-arm Leg Break"),
        ("Pat Cummins", "Australia", "Bowler",
         "Right-hand Bat", "Right-arm Fast"),
        ("Glenn Maxwell", "Australia", "All-rounder",
         "Right-hand Bat", "Right-arm Off Break"),
        ("Joe Root", "England", "Batsman",
         "Right-hand Bat", "Right-arm Off Break"),
        ("Ben Stokes", "England", "All-rounder",
         "Left-hand Bat", "Right-arm Fast Medium"),
        ("Kane Williamson", "New Zealand", "Batsman",
         "Right-hand Bat", "Right-arm Off Break"),
        ("Trent Boult", "New Zealand", "Bowler",
         "Left-hand Bat", "Left-arm Fast Medium"),
        ("Babar Azam", "Pakistan", "Batsman",
         "Right-hand Bat", "Right-arm Off Break"),
        ("Shaheen Afridi", "Pakistan", "Bowler",
         "Left-hand Bat", "Left-arm Fast"),
        ("Quinton de Kock", "South Africa", "Wicket-keeper",
         "Left-hand Bat", "Right-arm Medium"),
        ("Kagiso Rabada", "South Africa", "Bowler",
         "Left-hand Bat", "Right-arm Fast"),
        ("Kumar Sangakkara", "Sri Lanka", "Wicket-keeper",
         "Left-hand Bat", "Right-arm Medium"),
        ("Chris Gayle", "West Indies", "Batsman",
         "Left-hand Bat", "Right-arm Off Break")
    ]

    cursor.executemany(
        """
        INSERT INTO players
        (full_name, country, playing_role, batting_style, bowling_style)
        VALUES (?, ?, ?, ?, ?)
        """,
        players
    )

    # -------------------------------
    # VENUES
    # -------------------------------
    venues = [
        ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
        ("Wankhede Stadium", "Mumbai", "India", 33000),
        ("Eden Gardens", "Kolkata", "India", 68000),
        ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        ("Lord's Cricket Ground", "London", "England", 30000),
        ("Newlands Cricket Ground", "Cape Town", "South Africa", 25000),
        ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
        ("Basin Reserve", "Wellington", "New Zealand", 11600)
    ]

    cursor.executemany(
        """
        INSERT INTO venues
        (venue_name, city, country, capacity)
        VALUES (?, ?, ?, ?)
        """,
        venues
    )

    # -------------------------------
    # SERIES
    # -------------------------------
    series = [
        (
            "India vs Australia Series 2024",
            "India",
            "ODI",
            "2024-01-10",
            3
        ),
        (
            "India vs England Series 2024",
            "India",
            "Test",
            "2024-02-01",
            5
        ),
        (
            "Australia vs New Zealand Series 2024",
            "Australia",
            "T20",
            "2024-03-05",
            3
        )
    ]

    cursor.executemany(
        """
        INSERT INTO series
        (series_name, host_country, match_type, start_date, planned_matches)
        VALUES (?, ?, ?, ?, ?)
        """,
        series
    )

    connection.commit()
    connection.close()

    print("Sample cricket data inserted successfully!")


if __name__ == "__main__":
    insert_sample_data()
    