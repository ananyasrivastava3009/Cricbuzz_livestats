-- ==========================================
-- CRICBUZZ LIVESTATS DATABASE SCHEMA
-- ==========================================

-- 1. TEAMS TABLE
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name VARCHAR(100) NOT NULL,
    country VARCHAR(100)
);


-- 2. PLAYERS TABLE
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    playing_role VARCHAR(50),
    batting_style VARCHAR(100),
    bowling_style VARCHAR(100)
);


-- 3. VENUES TABLE
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INTEGER
);


-- 4. SERIES TABLE
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type VARCHAR(50),
    start_date DATE,
    planned_matches INTEGER
);


-- 5. MATCHES TABLE
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER,
    description TEXT,
    match_type VARCHAR(50),
    team1_id INTEGER,
    team2_id INTEGER,
    winner_team_id INTEGER,
    venue_id INTEGER,
    match_date DATE,
    toss_winner INTEGER,
    toss_decision VARCHAR(20),
    victory_margin INTEGER,
    victory_type VARCHAR(20),

    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner) REFERENCES teams(team_id)
);


-- 6. PLAYER PERFORMANCE TABLE
CREATE TABLE IF NOT EXISTS player_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    runs INTEGER DEFAULT 0,
    balls INTEGER DEFAULT 0,
    strike_rate DECIMAL(6,2),
    wickets INTEGER DEFAULT 0,
    overs DECIMAL(5,1),
    economy_rate DECIMAL(6,2),
    batting_position INTEGER,
    innings INTEGER,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,

    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);