# 🏏 Cricbuzz LiveStats
## Real-Time Cricket Insights & SQL-Based Analytics

Cricbuzz LiveStats is an interactive cricket analytics web application
that integrates cricket data with a SQL database and provides real-time
insights, player statistics, SQL analytics, and database management
through a Streamlit dashboard.

---

## 📌 Project Overview

The project is designed to provide a comprehensive platform for
analyzing cricket matches and player performances.

The application combines:

- Python
- SQL Database
- Cricbuzz REST API
- Streamlit
- Pandas
- Requests
- Data Analytics

The dashboard provides live match information, player statistics,
25 SQL analytical queries, and CRUD operations for database management.

---

## 🎯 Objectives

The main objectives of Cricbuzz LiveStats are:

- Fetch cricket information using a REST API.
- Display live and recent cricket match information.
- Analyze player performance.
- Perform SQL-based cricket analytics.
- Provide interactive data visualization.
- Implement Create, Read, Update and Delete operations.
- Provide an easy-to-use Streamlit dashboard.

---

## 🚀 Key Features

### 1. ⚡ Live Match

The Live Match page provides cricket match information including:

- Ongoing matches
- Match status
- Team information
- Venue details
- Scorecard information
- Batsmen information
- Bowler information

Live match information is designed to be fetched using the Cricbuzz API.

---

### 2. 👤 Top Player Stats

The Top Player Stats page provides player performance analysis.

It includes:

- Top run scorers
- Highest individual scores
- Top wicket takers
- Player performance statistics
- Batting statistics
- Bowling statistics

---

### 3. 📊 SQL Analytics

The project contains **25 SQL analytical questions** divided into
three difficulty levels:

#### Beginner Level
Questions 1–8

Topics include:

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- Basic filtering
- Aggregation

#### Intermediate Level
Questions 9–16

Topics include:

- JOIN
- Subqueries
- Aggregate functions
- Performance analysis
- Multiple-table analysis

#### Advanced Level
Questions 17–25

Topics include:

- Window functions
- CTEs
- Statistical calculations
- Performance ranking
- Time-series analysis
- Advanced cricket analytics

The SQL Analytics page allows users to select a question and view
its result directly in the Streamlit application.

---

### 4. 🗄️ CRUD Operations

The CRUD module provides database management functionality.

CRUD stands for:

- **Create** – Add new player records
- **Read** – View existing player records
- **Update** – Modify player information
- **Delete** – Remove player records

The operations are implemented using a form-based Streamlit interface.

---

### 5. 🏠 Home Page

The Home page provides:

- Project introduction
- Project objectives
- Technologies used
- Dashboard navigation
- Project instructions
- Database information

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Streamlit | Interactive web dashboard |
| SQL | Database management and analytics |
| SQLite | Database |
| Pandas | Data analysis |
| Requests | API requests |
| REST API | Cricket data integration |
| JSON | API data handling |

---

## 📁 Project Structure

```text
Cricbuzz_livestats/
│
├── api/
│   └── cricbuzz_api.py
│
├── data/
│
├── database/
│   ├── cricket.db
│   ├── schema.sql
│   └── sql/
│       └── 25_queries.sql
│
├── utils/
│   └── db_connection.py
│
├── streamlit_app/
│   └── app.py
│
├── main.py
├── seed_data.py
├── seed_matches.py
├── check_database.py
├── run_query.py
├── README.md
└── requirements.txt