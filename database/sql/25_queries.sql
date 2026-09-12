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

-- Question 2
SELECT
    m.description AS match_description,
    t1.team_name AS team1,
    t2.team_name AS team2,
    v.venue_name,
    v.city,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE date(m.match_date) >= date('now', '-30 days')
ORDER BY date(m.match_date) DESC;


-- =========================================================
-- QUESTION 3
-- Top 10 highest run scorers in ODI cricket
-- =========================================================

-- Question 3
SELECT
    p.full_name AS player_name,
    SUM(pp.runs) AS total_runs,
    ROUND(
        CAST(SUM(pp.runs) AS REAL) / NULLIF(COUNT(pp.performance_id), 0),
        2
    ) AS batting_average,
    SUM(
        CASE WHEN pp.runs >= 100 THEN 1 ELSE 0 END
    ) AS centuries
FROM player_performance pp
JOIN players p ON pp.player_id = p.player_id
JOIN matches m ON pp.match_id = m.match_id
WHERE UPPER(m.match_type) = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;

-- Question 4
SELECT
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;


-- Question 5
SELECT
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
LEFT JOIN matches m
    ON t.team_id = m.winner_team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
-- Question 6
SELECT
    playing_role,
    COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
-- Question 7
SELECT
    m.match_type AS format,
    MAX(pp.runs) AS highest_score
FROM player_performance pp
JOIN matches m ON pp.match_id = m.match_id
WHERE UPPER(m.match_type) IN ('TEST', 'ODI', 'T20I')
GROUP BY m.match_type
ORDER BY m.match_type;
-- Question 8
SELECT
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY date(start_date);
-- Question 9
SELECT
    p.full_name AS player_name,
    SUM(pp.runs) AS total_runs,
    SUM(pp.wickets) AS total_wickets,
    m.match_type AS format
FROM player_performance pp
JOIN players p ON pp.player_id = p.player_id
JOIN matches m ON pp.match_id = m.match_id
WHERE LOWER(p.playing_role) = 'all-rounder'
GROUP BY p.player_id, p.full_name, m.match_type
HAVING SUM(pp.runs) > 1000
   AND SUM(pp.wickets) > 50
ORDER BY total_runs DESC;
-- Question 10
SELECT
    m.description AS match_description,
    t1.team_name AS team1,
    t2.team_name AS team2,
    wt.team_name AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams wt ON m.winner_team_id = wt.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.winner_team_id IS NOT NULL
ORDER BY date(m.match_date) DESC
LIMIT 20;
-- Question 11
WITH player_formats AS (
    SELECT
        p.player_id,
        p.full_name,
        m.match_type,
        SUM(pp.runs) AS format_runs
    FROM player_performance pp
    JOIN players p ON pp.player_id = p.player_id
    JOIN matches m ON pp.match_id = m.match_id
    GROUP BY p.player_id, p.full_name, m.match_type
),
format_summary AS (
    SELECT
        player_id,
        full_name,
        MAX(CASE WHEN UPPER(match_type) = 'TEST'
                 THEN format_runs ELSE 0 END) AS test_runs,
        MAX(CASE WHEN UPPER(match_type) = 'ODI'
                 THEN format_runs ELSE 0 END) AS odi_runs,
        MAX(CASE WHEN UPPER(match_type) = 'T20I'
                 THEN format_runs ELSE 0 END) AS t20i_runs,
        COUNT(DISTINCT match_type) AS formats_played
    FROM player_formats
    GROUP BY player_id, full_name
)
SELECT
    full_name,
    test_runs,
    odi_runs,
    t20i_runs,
    formats_played
FROM format_summary
WHERE formats_played >= 2
ORDER BY full_name;
-- Question 12
SELECT
    t.team_name,
    CASE
        WHEN v.country = t.country THEN 'Home'
        ELSE 'Away'
    END AS match_location,
    COUNT(m.match_id) AS matches_played,
    SUM(
        CASE
            WHEN m.winner_team_id = t.team_id THEN 1
            ELSE 0
        END
    ) AS wins
FROM teams t
JOIN matches m
    ON t.team_id IN (m.team1_id, m.team2_id)
JOIN venues v
    ON m.venue_id = v.venue_id
GROUP BY
    t.team_id,
    t.team_name,
    match_location
ORDER BY t.team_name, match_location;
-- Question 13
SELECT
    p1.full_name AS player1,
    p2.full_name AS player2,
    m.match_id,
    pp1.innings,
    pp1.runs + pp2.runs AS partnership_runs
FROM player_performance pp1
JOIN player_performance pp2
    ON pp1.match_id = pp2.match_id
    AND pp1.innings = pp2.innings
    AND ABS(pp1.batting_position - pp2.batting_position) = 1
    AND pp1.player_id < pp2.player_id
JOIN players p1 ON pp1.player_id = p1.player_id
JOIN players p2 ON pp2.player_id = p2.player_id
JOIN matches m ON pp1.match_id = m.match_id
WHERE pp1.runs + pp2.runs >= 100
ORDER BY partnership_runs DESC;
-- Question 14
WITH match_bowling AS (
    SELECT
        pp.player_id,
        pp.match_id,
        m.venue_id,
        pp.economy_rate,
        pp.wickets,
        pp.overs
    FROM player_performance pp
    JOIN matches m ON pp.match_id = m.match_id
    WHERE pp.overs >= 4
),
venue_summary AS (
    SELECT
        player_id,
        venue_id,
        COUNT(DISTINCT match_id) AS matches_played,
        AVG(economy_rate) AS average_economy_rate,
        SUM(wickets) AS total_wickets
    FROM match_bowling
    GROUP BY player_id, venue_id
)
SELECT
    p.full_name,
    v.venue_name,
    matches_played,
    ROUND(average_economy_rate, 2) AS average_economy_rate,
    total_wickets
FROM venue_summary s
JOIN players p ON s.player_id = p.player_id
JOIN venues v ON s.venue_id = v.venue_id
WHERE matches_played >= 3
ORDER BY average_economy_rate ASC;
-- Question 15
SELECT
    p.full_name,
    ROUND(AVG(pp.runs), 2) AS average_runs,
    COUNT(DISTINCT pp.match_id) AS close_matches_played,
    SUM(
        CASE
            WHEN m.winner_team_id IS NOT NULL
            THEN 1
            ELSE 0
        END
    ) AS winning_matches
FROM player_performance pp
JOIN players p ON pp.player_id = p.player_id
JOIN matches m ON pp.match_id = m.match_id
WHERE
    (m.victory_type = 'runs' AND m.victory_margin < 50)
    OR
    (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.full_name
ORDER BY average_runs DESC;
-- Question 16
SELECT
    p.full_name,
    strftime('%Y', m.match_date) AS year,
    ROUND(AVG(pp.runs), 2) AS average_runs_per_match,
    ROUND(AVG(pp.strike_rate), 2) AS average_strike_rate,
    COUNT(DISTINCT pp.match_id) AS matches_played
FROM player_performance pp
JOIN players p ON pp.player_id = p.player_id
JOIN matches m ON pp.match_id = m.match_id
WHERE CAST(strftime('%Y', m.match_date) AS INTEGER) >= 2020
GROUP BY
    p.player_id,
    p.full_name,
    year
HAVING COUNT(DISTINCT pp.match_id) >= 5
ORDER BY year, average_runs_per_match DESC;


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
