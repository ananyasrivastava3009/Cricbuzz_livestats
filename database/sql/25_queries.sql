-- =========================================================
-- QUESTION 1
-- Find all players who represent India
-- =========================================================

SELECT
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India';


-- =========================================================
-- QUESTION 2
-- Show matches played in the last 30 days
-- =========================================================

SELECT
    match_description,
    team1,
    team2,
    venue_name,
    venue_city,
    match_date
FROM matches
WHERE match_date >= DATE('now', '-30 days')
ORDER BY match_date DESC;


-- =========================================================
-- QUESTION 3
-- Top 10 highest run scorers in ODI cricket
-- =========================================================

SELECT
    p.full_name,
    SUM(pp.runs_scored) AS total_runs,
    ROUND(AVG(pp.batting_average), 2) AS batting_average,
    SUM(pp.centuries) AS centuries
FROM players p
JOIN player_performance pp
    ON p.player_id = pp.player_id
WHERE pp.format = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;


-- =========================================================
-- QUESTION 4
-- Venues with seating capacity greater than 50,000
-- =========================================================

SELECT
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;


-- =========================================================
-- QUESTION 5
-- Number of matches won by each team
-- =========================================================

SELECT
    winner AS team_name,
    COUNT(*) AS total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC;


-- =========================================================
-- QUESTION 6
-- Count players according to playing role
-- =========================================================

SELECT
    playing_role,
    COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;


-- =========================================================
-- QUESTION 7
-- Highest individual batting score in each format
-- =========================================================

SELECT
    format,
    MAX(highest_score) AS highest_individual_score
FROM player_performance
GROUP BY format
ORDER BY highest_individual_score DESC;


-- =========================================================
-- QUESTION 8
-- Cricket series started in 2024
-- =========================================================

SELECT
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date;


-- =========================================================
-- QUESTION 9
-- All-rounders with more than 1000 runs
-- AND more than 50 wickets
-- =========================================================

SELECT
    p.full_name,
    pp.format,
    SUM(pp.runs_scored) AS total_runs,
    SUM(pp.wickets) AS total_wickets
FROM players p
JOIN player_performance pp
    ON p.player_id = pp.player_id
WHERE p.playing_role = 'All-rounder'
GROUP BY p.player_id, p.full_name, pp.format
HAVING SUM(pp.runs_scored) > 1000
   AND SUM(pp.wickets) > 50
ORDER BY total_runs DESC;


-- =========================================================
-- QUESTION 10
-- Last 20 completed matches
-- =========================================================

SELECT
    match_description,
    team1,
    team2,
    winner,
    victory_margin,
    victory_type,
    venue_name
FROM matches
WHERE status = 'Completed'
ORDER BY match_date DESC
LIMIT 20;


-- =========================================================
-- QUESTION 11
-- Player performance across different formats
-- =========================================================

SELECT
    p.full_name,

    SUM(
        CASE
            WHEN pp.format = 'Test'
            THEN pp.runs_scored
            ELSE 0
        END
    ) AS test_runs,

    SUM(
        CASE
            WHEN pp.format = 'ODI'
            THEN pp.runs_scored
            ELSE 0
        END
    ) AS odi_runs,

    SUM(
        CASE
            WHEN pp.format = 'T20I'
            THEN pp.runs_scored
            ELSE 0
        END
    ) AS t20i_runs,

    ROUND(AVG(pp.batting_average), 2)
        AS overall_batting_average,

    COUNT(DISTINCT pp.format)
        AS formats_played

FROM players p
JOIN player_performance pp
    ON p.player_id = pp.player_id

GROUP BY p.player_id, p.full_name

HAVING COUNT(DISTINCT pp.format) >= 2

ORDER BY overall_batting_average DESC;


-- =========================================================
-- QUESTION 12
-- Team performance at home vs away
-- =========================================================

SELECT
    team,
    playing_condition,
    COUNT(*) AS matches_played,
    SUM(
        CASE
            WHEN winner = team THEN 1
            ELSE 0
        END
    ) AS wins
FROM
(
    SELECT
        team1 AS team,
        CASE
            WHEN venue_country = team1_country
            THEN 'Home'
            ELSE 'Away'
        END AS playing_condition,
        winner
    FROM matches

    UNION ALL

    SELECT
        team2 AS team,
        CASE
            WHEN venue_country = team2_country
            THEN 'Home'
            ELSE 'Away'
        END AS playing_condition,
        winner
    FROM matches
)
GROUP BY team, playing_condition
ORDER BY team, playing_condition;


-- =========================================================
-- QUESTION 13
-- Consecutive batsmen with combined score >= 100
-- =========================================================

SELECT
    a.player_name AS player_1,
    b.player_name AS player_2,
    a.innings,
    (a.runs + b.runs) AS partnership_runs
FROM batting_performance a
JOIN batting_performance b
    ON a.match_id = b.match_id
    AND a.innings = b.innings
    AND ABS(a.batting_position - b.batting_position) = 1
    AND a.batting_position < b.batting_position
WHERE (a.runs + b.runs) >= 100
ORDER BY partnership_runs DESC;


-- =========================================================
-- QUESTION 14
-- Bowling performance at different venues
-- =========================================================

SELECT
    bowler,
    venue_name,
    COUNT(DISTINCT match_id) AS matches_played,
    ROUND(AVG(economy_rate), 2) AS average_economy_rate,
    SUM(wickets) AS total_wickets
FROM bowling_performance
WHERE overs >= 4
GROUP BY bowler, venue_name
HAVING COUNT(DISTINCT match_id) >= 3
ORDER BY average_economy_rate ASC;


-- =========================================================
-- QUESTION 15
-- Players performing exceptionally in close matches
-- =========================================================

SELECT
    bp.player_name,
    ROUND(AVG(bp.runs), 2) AS average_runs,
    COUNT(DISTINCT bp.match_id) AS close_matches_played,

    SUM(
        CASE
            WHEN m.winner = bp.team
            THEN 1
            ELSE 0
        END
    ) AS team_wins

FROM batting_performance bp

JOIN matches m
    ON bp.match_id = m.match_id

WHERE
    (m.victory_type = 'runs' AND m.victory_margin < 50)
    OR
    (m.victory_type = 'wickets' AND m.victory_margin < 5)

GROUP BY bp.player_name
ORDER BY average_runs DESC;


-- =========================================================
-- QUESTION 16
-- Player batting performance since 2020
-- =========================================================

SELECT
    p.full_name,
    strftime('%Y', m.match_date) AS year,

    ROUND(AVG(pp.runs_scored), 2)
        AS average_runs,

    ROUND(AVG(pp.strike_rate), 2)
        AS average_strike_rate,

    COUNT(DISTINCT pp.match_id)
        AS matches_played

FROM players p

JOIN player_performance pp
    ON p.player_id = pp.player_id

JOIN matches m
    ON pp.match_id = m.match_id

WHERE CAST(strftime('%Y', m.match_date) AS INTEGER) >= 2020

GROUP BY
    p.player_id,
    p.full_name,
    year

HAVING COUNT(DISTINCT pp.match_id) >= 5

ORDER BY year DESC, average_runs DESC;


-- =========================================================
-- QUESTION 17
-- Toss winner advantage
-- =========================================================

-- Question 17
SELECT
    m.toss_decision,
    COUNT(*) AS total_matches,

    SUM(
        CASE
            WHEN CAST(m.toss_winner AS TEXT) = CAST(m.winner_team_id AS TEXT)
            THEN 1
            ELSE 0
        END
    ) AS toss_winner_wins,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN CAST(m.toss_winner AS TEXT) = CAST(m.winner_team_id AS TEXT)
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS win_percentage

FROM matches m

WHERE m.winner_team_id IS NOT NULL

GROUP BY m.toss_decision;


-- =========================================================
-- QUESTION 18
-- Most economical ODI and T20 bowlers
-- =========================================================

SELECT
    bowler,
    format,
    ROUND(
        SUM(runs_conceded) * 6.0 /
        NULLIF(SUM(legal_balls), 0),
        2
    ) AS economy_rate,

    SUM(wickets) AS total_wickets,

    COUNT(DISTINCT match_id) AS matches_bowled

FROM bowling_performance

WHERE format IN ('ODI', 'T20', 'T20I')

GROUP BY bowler, format

HAVING COUNT(DISTINCT match_id) >= 10

ORDER BY economy_rate ASC;


-- =========================================================
-- QUESTION 19
-- Most consistent batsmen
-- =========================================================

SELECT
    player_name,

    ROUND(AVG(runs), 2)
        AS average_runs,

    ROUND(
        SQRT(
            AVG(runs * runs)
            - AVG(runs) * AVG(runs)
        ),
        2
    ) AS standard_deviation,

    COUNT(DISTINCT match_id)
        AS innings_played,

    SUM(balls_faced)
        AS total_balls_faced

FROM batting_performance

WHERE match_date >= '2022-01-01'

GROUP BY player_name

HAVING SUM(balls_faced) >= 10

ORDER BY standard_deviation ASC;


-- =========================================================
-- QUESTION 20
-- Matches and batting average by format
-- =========================================================

SELECT
    p.full_name,

    SUM(
        CASE
            WHEN pp.format = 'Test'
            THEN 1 ELSE 0
        END
    ) AS test_matches,

    ROUND(
        AVG(
            CASE
                WHEN pp.format = 'Test'
                THEN pp.batting_average
            END
        ), 2
    ) AS test_average,

    SUM(
        CASE
            WHEN pp.format = 'ODI'
            THEN 1 ELSE 0
        END
    ) AS odi_matches,

    ROUND(
        AVG(
            CASE
                WHEN pp.format = 'ODI'
                THEN pp.batting_average
            END
        ), 2
    ) AS odi_average,

    SUM(
        CASE
            WHEN pp.format = 'T20I'
            THEN 1 ELSE 0
        END
    ) AS t20_matches,

    ROUND(
        AVG(
            CASE
                WHEN pp.format = 'T20I'
                THEN pp.batting_average
            END
        ), 2
    ) AS t20_average

FROM players p

JOIN player_performance pp
    ON p.player_id = pp.player_id

GROUP BY p.player_id, p.full_name

HAVING COUNT(DISTINCT pp.format) >= 1

ORDER BY p.full_name;


-- =========================================================
-- QUESTION 21
-- Comprehensive player performance ranking
-- =========================================================

SELECT
    p.full_name,
    pp.format,

    (
        (SUM(pp.runs_scored) * 0.01)
        +
        (AVG(pp.batting_average) * 0.5)
        +
        (AVG(pp.strike_rate) * 0.3)
        +
        (SUM(pp.wickets) * 2)
        +
        ((50 - AVG(pp.bowling_average)) * 0.5)
        +
        ((6 - AVG(pp.economy_rate)) * 2)
        +
        (SUM(pp.catches) * 3)
        +
        (SUM(pp.stumpings) * 5)
    ) AS performance_score

FROM players p

JOIN player_performance pp
    ON p.player_id = pp.player_id

GROUP BY
    p.player_id,
    p.full_name,
    pp.format

ORDER BY performance_score DESC;


-- =========================================================
-- QUESTION 22
-- Head-to-head team analysis
-- =========================================================

SELECT

    CASE
        WHEN team1 < team2
        THEN team1
        ELSE team2
    END AS team_a,

    CASE
        WHEN team1 < team2
        THEN team2
        ELSE team1
    END AS team_b,

    COUNT(*) AS matches_played,

    SUM(
        CASE
            WHEN winner =
                CASE
                    WHEN team1 < team2 THEN team1
                    ELSE team2
                END
            THEN 1
            ELSE 0
        END
    ) AS team_a_wins,

    SUM(
        CASE
            WHEN winner =
                CASE
                    WHEN team1 < team2 THEN team2
                    ELSE team1
                END
            THEN 1
            ELSE 0
        END
    ) AS team_b_wins

FROM matches

WHERE match_date >= DATE('now', '-3 years')

GROUP BY team_a, team_b

HAVING COUNT(*) >= 5

ORDER BY matches_played DESC;


-- =========================================================
-- QUESTION 23
-- Recent player form and momentum
-- =========================================================

WITH recent_matches AS
(
    SELECT
        player_name,
        match_id,
        match_date,
        runs,
        strike_rate,

        ROW_NUMBER() OVER (
            PARTITION BY player_name
            ORDER BY match_date DESC
        ) AS rn

    FROM batting_performance
)

SELECT
    player_name,

    ROUND(
        AVG(
            CASE
                WHEN rn <= 5 THEN runs
            END
        ), 2
    ) AS average_last_5,

    ROUND(
        AVG(
            CASE
                WHEN rn <= 10 THEN runs
            END
        ), 2
    ) AS average_last_10,

    ROUND(
        AVG(
            CASE
                WHEN rn <= 10 THEN strike_rate
            END
        ), 2
    ) AS recent_strike_rate,

    SUM(
        CASE
            WHEN rn <= 10 AND runs > 50
            THEN 1
            ELSE 0
        END
    ) AS scores_above_50,

    ROUND(
        SQRT(
            AVG(
                CASE
                    WHEN rn <= 10
                    THEN runs * runs
                END
            )
            -
            AVG(
                CASE
                    WHEN rn <= 10
                    THEN runs
                END
            )
            *
            AVG(
                CASE
                    WHEN rn <= 10
                    THEN runs
                END
            )
        ), 2
    ) AS consistency_score

FROM recent_matches

WHERE rn <= 10

GROUP BY player_name

ORDER BY average_last_5 DESC;


-- =========================================================
-- QUESTION 24
-- Successful batting partnerships
-- =========================================================

WITH partnerships AS
(
    SELECT

        a.player_name AS player_1,
        b.player_name AS player_2,

        a.match_id,
        a.innings,

        (a.runs + b.runs)
            AS partnership_runs

    FROM batting_performance a

    JOIN batting_performance b

        ON a.match_id = b.match_id
        AND a.innings = b.innings
        AND b.batting_position = a.batting_position + 1
)

SELECT

    player_1,
    player_2,

    COUNT(*) AS partnerships,

    ROUND(
        AVG(partnership_runs),
        2
    ) AS average_partnership_runs,

    SUM(
        CASE
            WHEN partnership_runs > 50
            THEN 1
            ELSE 0
        END
    ) AS partnerships_over_50,

    MAX(partnership_runs)
        AS highest_partnership,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN partnership_runs > 50
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS success_rate

FROM partnerships

GROUP BY player_1, player_2

HAVING COUNT(*) >= 5

ORDER BY success_rate DESC;


-- =========================================================
-- QUESTION 25
-- Time-series player performance evolution
-- =========================================================

WITH quarterly_stats AS
(
    SELECT

        player_name,

        strftime(
            '%Y',
            match_date
        ) AS year,

        ((CAST(
            strftime('%m', match_date)
            AS INTEGER
        ) - 1) / 3) + 1 AS quarter,

        AVG(runs) AS avg_runs,

        AVG(strike_rate)
            AS avg_strike_rate,

        COUNT(DISTINCT match_id)
            AS matches_played

    FROM batting_performance

    GROUP BY
        player_name,
        year,
        quarter

    HAVING COUNT(DISTINCT match_id) >= 3
),

performance_change AS
(
    SELECT

        *,

        LAG(avg_runs) OVER (
            PARTITION BY player_name
            ORDER BY year, quarter
        ) AS previous_avg_runs,

        LAG(avg_strike_rate) OVER (
            PARTITION BY player_name
            ORDER BY year, quarter
        ) AS previous_avg_strike_rate

    FROM quarterly_stats
)

SELECT

    player_name,
    year,
    quarter,

    ROUND(avg_runs, 2)
        AS average_runs,

    ROUND(avg_strike_rate, 2)
        AS average_strike_rate,

    ROUND(
        avg_runs - previous_avg_runs,
        2
    ) AS run_change,

    ROUND(
        avg_strike_rate - previous_avg_strike_rate,
        2
    ) AS strike_rate_change,

    CASE
        WHEN avg_runs > previous_avg_runs
             AND avg_strike_rate > previous_avg_strike_rate
        THEN 'Improving'

        WHEN avg_runs < previous_avg_runs
             AND avg_strike_rate < previous_avg_strike_rate
        THEN 'Declining'

        ELSE 'Stable'
    END AS performance_trend

FROM performance_change

ORDER BY
    player_name,
    year,
    quarter;
