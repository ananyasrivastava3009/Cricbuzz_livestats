from utils.db_connection import get_connection


def get_id(cursor, table, column, value):
    """Return the ID of a record using its name."""
    cursor.execute(
        f"SELECT {table[:-1]}_id FROM {table} WHERE {column} = ?",
        (value,)
    )
    result = cursor.fetchone()

    if result is None:
        raise ValueError(f"{value} not found in {table}")

    return result[0]


def insert_matches_and_performance():
    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------------------------------
    # CLEAR OLD MATCH DATA
    # This makes the script safe to run again.
    # -------------------------------------------------
    cursor.execute("DELETE FROM player_performance")
    cursor.execute("DELETE FROM matches")

    # -------------------------------------------------
    # TEAM IDs
    # -------------------------------------------------
    teams = {}

    team_names = [
        "India",
        "Australia",
        "England",
        "South Africa",
        "New Zealand",
        "Pakistan",
        "Sri Lanka",
        "West Indies"
    ]

    for team in team_names:
        cursor.execute(
            "SELECT team_id FROM teams WHERE team_name = ?",
            (team,)
        )
        teams[team] = cursor.fetchone()[0]

    # -------------------------------------------------
    # PLAYER IDs BY COUNTRY
    # -------------------------------------------------
    player_map = {}

    cursor.execute(
        """
        SELECT player_id, full_name, country
        FROM players
        """
    )

    for player_id, full_name, country in cursor.fetchall():
        if country not in player_map:
            player_map[country] = []

        player_map[country].append(
            (player_id, full_name)
        )

    # -------------------------------------------------
    # VENUE IDs
    # -------------------------------------------------
    venues = {}

    venue_names = [
        "Narendra Modi Stadium",
        "Wankhede Stadium",
        "Eden Gardens",
        "Melbourne Cricket Ground",
        "Lord's Cricket Ground",
        "Newlands Cricket Ground",
        "Gaddafi Stadium",
        "Basin Reserve"
    ]

    for venue in venue_names:
        cursor.execute(
            "SELECT venue_id FROM venues WHERE venue_name = ?",
            (venue,)
        )
        venues[venue] = cursor.fetchone()[0]

    # -------------------------------------------------
    # SERIES IDs
    # -------------------------------------------------
    series_ids = {}

    series_names = [
        "India vs Australia Series 2024",
        "India vs England Series 2024",
        "Australia vs New Zealand Series 2024"
    ]

    for series_name in series_names:
        cursor.execute(
            "SELECT series_id FROM series WHERE series_name = ?",
            (series_name,)
        )
        series_ids[series_name] = cursor.fetchone()[0]

    # -------------------------------------------------
    # MATCH DATA
    # -------------------------------------------------
    matches = [
        (
            "India vs Australia - 1st ODI",
            "ODI",
            "India",
            "Australia",
            "India",
            "Narendra Modi Stadium",
            "2024-01-12",
            "India",
            "bat",
            42,
            "runs",
            "India vs Australia Series 2024"
        ),
        (
            "India vs Australia - 2nd ODI",
            "ODI",
            "India",
            "Australia",
            "Australia",
            "Wankhede Stadium",
            "2024-01-15",
            "Australia",
            "bowl",
            5,
            "wickets",
            "India vs Australia Series 2024"
        ),
        (
            "India vs Australia - 3rd ODI",
            "ODI",
            "India",
            "Australia",
            "India",
            "Eden Gardens",
            "2024-01-18",
            "India",
            "bat",
            18,
            "runs",
            "India vs Australia Series 2024"
        ),
        (
            "India vs England - 1st Test",
            "Test",
            "India",
            "England",
            "India",
            "Wankhede Stadium",
            "2024-02-02",
            "England",
            "bowl",
            7,
            "wickets",
            "India vs England Series 2024"
        ),
        (
            "India vs England - 2nd Test",
            "Test",
            "India",
            "England",
            "England",
            "Eden Gardens",
            "2024-02-10",
            "India",
            "bat",
            95,
            "runs",
            "India vs England Series 2024"
        ),
        (
            "India vs England - 3rd Test",
            "Test",
            "India",
            "England",
            "India",
            "Narendra Modi Stadium",
            "2024-02-18",
            "England",
            "bowl",
            6,
            "wickets",
            "India vs England Series 2024"
        ),
        (
            "Australia vs New Zealand - 1st T20",
            "T20",
            "Australia",
            "New Zealand",
            "Australia",
            "Melbourne Cricket Ground",
            "2024-03-06",
            "Australia",
            "bat",
            12,
            "runs",
            "Australia vs New Zealand Series 2024"
        ),
        (
            "Australia vs New Zealand - 2nd T20",
            "T20",
            "Australia",
            "New Zealand",
            "New Zealand",
            "Basin Reserve",
            "2024-03-09",
            "New Zealand",
            "bowl",
            4,
            "wickets",
            "Australia vs New Zealand Series 2024"
        ),
        (
            "Australia vs New Zealand - 3rd T20",
            "T20",
            "Australia",
            "New Zealand",
            "Australia",
            "Melbourne Cricket Ground",
            "2024-03-12",
            "New Zealand",
            "bat",
            8,
            "runs",
            "Australia vs New Zealand Series 2024"
        ),

        # 2023 MATCHES
        (
            "India vs South Africa - ODI",
            "ODI",
            "India",
            "South Africa",
            "India",
            "Newlands Cricket Ground",
            "2023-01-15",
            "South Africa",
            "bowl",
            25,
            "runs",
            None
        ),
        (
            "India vs New Zealand - ODI",
            "ODI",
            "India",
            "New Zealand",
            "New Zealand",
            "Eden Gardens",
            "2023-02-12",
            "India",
            "bat",
            3,
            "wickets",
            None
        ),
        (
            "Australia vs England - ODI",
            "ODI",
            "Australia",
            "England",
            "Australia",
            "Melbourne Cricket Ground",
            "2023-03-08",
            "Australia",
            "bowl",
            31,
            "runs",
            None
        ),
        (
            "Pakistan vs New Zealand - T20",
            "T20",
            "Pakistan",
            "New Zealand",
            "Pakistan",
            "Gaddafi Stadium",
            "2023-04-10",
            "Pakistan",
            "bat",
            17,
            "runs",
            None
        ),
        (
            "South Africa vs England - Test",
            "Test",
            "South Africa",
            "England",
            "South Africa",
            "Newlands Cricket Ground",
            "2023-05-18",
            "England",
            "bowl",
            120,
            "runs",
            None
        ),
        (
            "Sri Lanka vs India - ODI",
            "ODI",
            "Sri Lanka",
            "India",
            "India",
            "Wankhede Stadium",
            "2023-06-21",
            "Sri Lanka",
            "bat",
            6,
            "wickets",
            None
        ),

        # 2022 MATCHES
        (
            "India vs Pakistan - T20",
            "T20",
            "India",
            "Pakistan",
            "India",
            "Wankhede Stadium",
            "2022-01-14",
            "Pakistan",
            "bowl",
            4,
            "wickets",
            None
        ),
        (
            "Australia vs South Africa - ODI",
            "ODI",
            "Australia",
            "South Africa",
            "South Africa",
            "Melbourne Cricket Ground",
            "2022-02-20",
            "Australia",
            "bat",
            22,
            "runs",
            None
        ),
        (
            "England vs New Zealand - Test",
            "Test",
            "England",
            "New Zealand",
            "England",
            "Lord's Cricket Ground",
            "2022-03-15",
            "New Zealand",
            "bowl",
            75,
            "runs",
            None
        ),
        (
            "India vs West Indies - T20",
            "T20",
            "India",
            "West Indies",
            "West Indies",
            "Eden Gardens",
            "2022-04-12",
            "India",
            "bat",
            2,
            "wickets",
            None
        ),
        (
            "Pakistan vs Sri Lanka - ODI",
            "ODI",
            "Pakistan",
            "Sri Lanka",
            "Pakistan",
            "Gaddafi Stadium",
            "2022-05-19",
            "Sri Lanka",
            "bowl",
            40,
            "runs",
            None
        ),
        (
            "New Zealand vs South Africa - Test",
            "Test",
            "New Zealand",
            "South Africa",
            "New Zealand",
            "Basin Reserve",
            "2022-06-22",
            "New Zealand",
            "bat",
            110,
            "runs",
            None
        )
    ]

    # -------------------------------------------------
    # INSERT MATCHES
    # -------------------------------------------------
    match_ids = []

    for match in matches:

        (
            description,
            match_type,
            team1,
            team2,
            winner,
            venue,
            match_date,
            toss_winner,
            toss_decision,
            victory_margin,
            victory_type,
            series_name
        ) = match

        team1_id = teams[team1]
        team2_id = teams[team2]
        winner_id = teams[winner]
        venue_id = venues[venue]
        toss_winner_id = teams[toss_winner]

        series_id = None

        if series_name:
            series_id = series_ids[series_name]

        cursor.execute(
            """
            INSERT INTO matches (
                series_id,
                description,
                match_type,
                team1_id,
                team2_id,
                winner_team_id,
                venue_id,
                match_date,
                toss_winner,
                toss_decision,
                victory_margin,
                victory_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                series_id,
                description,
                match_type,
                team1_id,
                team2_id,
                winner_id,
                venue_id,
                match_date,
                toss_winner_id,
                toss_decision,
                victory_margin,
                victory_type
            )
        )

        match_ids.append(
            (
                cursor.lastrowid,
                team1,
                team2
            )
        )

    # -------------------------------------------------
    # INSERT PLAYER PERFORMANCE
    # -------------------------------------------------
    # Deterministic sample statistics
    # are used for SQL practice.
    # -------------------------------------------------

    performance_number = 0

    for match_id, team1, team2 in match_ids:

        teams_in_match = [team1, team2]

        for innings_number, team in enumerate(
            teams_in_match,
            start=1
        ):

            players = player_map.get(team, [])

            for position, (player_id, player_name) in enumerate(
                players,
                start=1
            ):

                performance_number += 1

                # Generate varied batting numbers
                runs = (
                    (performance_number * 17 + position * 11)
                    % 101
                )

                balls = max(
                    10,
                    runs + 15 + (position * 3)
                )

                strike_rate = round(
                    (runs / balls) * 100,
                    2
                )

                # Some players receive wickets
                wickets = (
                    performance_number * 3 + position
                ) % 6

                overs = round(
                    2 + ((position * 2) % 5),
                    1
                )

                economy_rate = round(
                    4.0 + ((performance_number + position) % 5)
                    * 0.45,
                    2
                )

                catches = (
                    performance_number + position
                ) % 4

                stumpings = 0

                # Wicket-keepers get occasional stumpings
                if "Wicket-keeper" in player_name:
                    stumpings = 1

                cursor.execute(
                    """
                    INSERT INTO player_performance (
                        match_id,
                        player_id,
                        runs,
                        balls,
                        strike_rate,
                        wickets,
                        overs,
                        economy_rate,
                        batting_position,
                        innings,
                        catches,
                        stumpings
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        match_id,
                        player_id,
                        runs,
                        balls,
                        strike_rate,
                        wickets,
                        overs,
                        economy_rate,
                        position,
                        innings_number,
                        catches,
                        stumpings
                    )
                )

    connection.commit()
    connection.close()

    print("Matches and player performance data inserted successfully!")
    print(f"Total matches inserted: {len(match_ids)}")
    print(f"Player performance records created: {performance_number}")


if __name__ == "__main__":
    insert_matches_and_performance()