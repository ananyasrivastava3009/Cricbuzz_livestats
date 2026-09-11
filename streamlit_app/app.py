import streamlit as st
import sqlite3
import pandas as pd
import os
import re
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

from api.cricbuzz_api import (
    get_live_matches,
    get_recent_matches,
    get_upcoming_matches,
    get_top_player_stats,
    get_match_scorecard,
    api_configured
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "cricket.db")
QUERIES_PATH = os.path.join(BASE_DIR, "database", "sql", "25_queries.sql")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================================================
# DATABASE QUERY FUNCTION
# =========================================================

def run_sql(query, params=()):
    conn = get_connection()

    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


# =========================================================
# HEADER
# =========================================================

st.title("🏏 Cricbuzz LiveStats")
st.markdown(
    "### Cricket Data Analytics & Live Statistics Dashboard"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏏 Cricbuzz LiveStats")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🏏 Live Match",
        "👤 Top Player Stats",
        "📊 SQL Analytics",
        "✏️ CRUD Operations"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "🏠 Home":

    st.header("🏠 Welcome to Cricbuzz LiveStats")

    st.write(
        """
        Cricbuzz LiveStats is a cricket analytics application
        developed using Python, SQLite and Streamlit.

        The application provides cricket player information,
        match statistics, SQL-based analytics and CRUD operations.
        """
    )

    # -------------------------
    # DATABASE METRICS
    # -------------------------

    players_df = run_sql(
        "SELECT COUNT(*) AS total FROM players"
    )

    teams_df = run_sql(
        "SELECT COUNT(*) AS total FROM teams"
    )

    matches_df = run_sql(
        "SELECT COUNT(*) AS total FROM matches"
    )

    venues_df = run_sql(
        "SELECT COUNT(*) AS total FROM venues"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if not players_df.empty:
            st.metric(
                "👤 Total Players",
                players_df.iloc[0]["total"]
            )

    with col2:
        if not teams_df.empty:
            st.metric(
                "🏏 Total Teams",
                teams_df.iloc[0]["total"]
            )

    with col3:
        if not matches_df.empty:
            st.metric(
                "📅 Total Matches",
                matches_df.iloc[0]["total"]
            )

    with col4:
        if not venues_df.empty:
            st.metric(
                "🏟️ Total Venues",
                venues_df.iloc[0]["total"]
            )

    st.divider()

    st.subheader("📌 Project Modules")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            """
            **🏏 Live Match**

            View available cricket match information,
            teams, venues and match details.
            """
        )

    with c2:
        st.info(
            """
            **👤 Top Player Stats**

            Analyse player runs, wickets,
            strike rate and economy rate.
            """
        )

    with c3:
        st.info(
            """
            **📊 SQL Analytics**

            Execute the 25 analytical SQL queries
            included in the project.
            """
        )

    st.success(
        "Database connected successfully ✅"
    )


# =========================================================
# LIVE MATCH PAGE
# =========================================================

elif page == "🏏 Live Match":

    st.title("🏏 Live Cricket Matches")

    # Check whether Cricbuzz API key is configured
    if api_configured():

        st.info("Fetching live matches from Cricbuzz API...")

        result = get_live_matches()

        if result["success"]:

            data = result["data"]

            st.success("Live match data fetched successfully!")

            # Try to display common Cricbuzz match structures
            matches = []

            if isinstance(data, dict):

                # Common Cricbuzz response structure
                if "typeMatches" in data:
                    for match_type in data["typeMatches"]:

                        series_matches = match_type.get(
                            "seriesMatches", []
                        )

                        for series_item in series_matches:

                            series_ad_wrapper = series_item.get(
                                "seriesAdWrapper", {}
                            )

                            matches.extend(
                                series_ad_wrapper.get(
                                    "matches", []
                                )
                            )

                elif "matches" in data:
                    matches = data["matches"]

            if matches:

                st.subheader("🔴 Ongoing Matches")

                for item in matches:

                    match_info = item.get(
                        "matchInfo", {}
                    )

                    match_score = item.get(
                        "matchScore", {}
                    )

                    description = match_info.get(
                        "matchDesc",
                        "Cricket Match"
                    )

                    status = match_info.get(
                        "status",
                        "Status not available"
                    )

                    venue_info = match_info.get(
                        "venueInfo", {}
                    )

                    venue = venue_info.get(
                        "ground",
                        "Venue not available"
                    )

                    city = venue_info.get(
                        "city",
                        ""
                    )

                    st.markdown("---")

                    st.subheader(f"🏏 {description}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            "**Status:**",
                            status
                        )

                    with col2:
                        st.write(
                            "**Venue:**",
                            f"{venue}, {city}"
                        )

                    # Display team scores if available
                    if match_score:

                        for team_name, score_data in match_score.items():

                            if isinstance(score_data, dict):

                                runs = score_data.get(
                                    "teamScore",
                                    {}
                                ).get(
                                    "inngs1",
                                    {}
                                ).get(
                                    "runs"
                                )

                                wickets = score_data.get(
                                    "teamScore",
                                    {}
                                ).get(
                                    "inngs1",
                                    {}
                                ).get(
                                    "wickets"
                                )

                                overs = score_data.get(
                                    "teamScore",
                                    {}
                                ).get(
                                    "inngs1",
                                    {}
                                ).get(
                                    "overs"
                                )

                                if runs is not None:

                                    score_text = f"{runs}"

                                    if wickets is not None:
                                        score_text += f"/{wickets}"

                                    if overs is not None:
                                        score_text += f" ({overs} overs)"

                                    st.write(
                                        f"**{team_name}:** {score_text}"
                                    )

            else:

                st.warning(
                    "No live matches are currently available."
                )

        else:

            st.error(
                f"API Error: {result['error']}"
            )

    else:

        st.warning(
            "⚠️ Cricbuzz API key is not configured."
        )

        st.info(
            "Live API data will be available after "
            "adding the Cricbuzz API key."
        )

        st.subheader("📊 Available Database Matches")

        # Fallback to local database
        try:

            query = """
            SELECT
                m.match_id,
                m.description,
                m.match_type,
                t1.team_name AS team1,
                t2.team_name AS team2,
                m.match_date,
                v.venue_name,
                v.city,
                m.toss_decision,
                m.victory_margin,
                m.victory_type
            FROM matches m
            LEFT JOIN teams t1
                ON m.team1_id = t1.team_id
            LEFT JOIN teams t2
                ON m.team2_id = t2.team_id
            LEFT JOIN venues v
                ON m.venue_id = v.venue_id
            ORDER BY m.match_date DESC
            """

            df = run_sql(query)

            if not df.empty:
                st.dataframe(
                    df,
                    use_container_width=True
                )
            else:
                st.info(
                    "No matches found in the database."
                )

        except Exception as e:

            st.error(
                f"Database Error: {e}"
            )
            
        # -------------------------
        # TOP WICKET TAKERS
        # -------------------------
        try:
            stats = run_sql("""
                SELECT
                    p.full_name,
                    SUM(pp.runs) AS total_runs,
                    SUM(pp.wickets) AS total_wickets
                FROM player_performance pp
                JOIN players p
                    ON pp.player_id = p.player_id
                GROUP BY p.player_id, p.full_name
            """)

            if not stats.empty:
                top_wickets = (
                    stats.sort_values("total_wickets", ascending=False)
                    .head(10)
                )

                st.subheader("🏆 Top 10 Wicket Takers")
                st.bar_chart(
                    top_wickets.set_index("full_name")["total_wickets"]
                )
            else:
                st.warning("No player performance data available.")

        except Exception as e:
            st.error(f"Database Error: {e}")


# ============================================================
# SQL ANALYTICS PAGE
# ============================================================

elif page == "📊 SQL Analytics":
    st.header("📊 SQL Analytics")

    # -------------------------
    # READ SQL FILE
    # -------------------------

if not os.path.exists(QUERIES_PATH):

            st.error(
            "25_queries.sql file not found."
        )

else:

                with open(
            QUERIES_PATH,
            "r",
            encoding="utf-8"
        ) as file:

                     sql_content = file.read()

        # -------------------------------------------------
        # FIND QUESTIONS
        # -------------------------------------------------

pattern = r"(?:Question\s*)?(\d{1,2})[\.\):\-]\s*(.*?)(?=\n(?:Question\s*)?\d{1,2}[\.\):\-]|\Z)"

matches = re.findall(
            pattern,
            sql_content,
            flags=re.IGNORECASE | re.DOTALL
        )

        # -------------------------------------------------
        # FALLBACK PARSER
        # -------------------------------------------------

if len(matches) < 25:

            blocks = re.split(
                r"(?=Question\s*\d+|Q\d+|\n\d+[\.\)])",
                sql_content,
                flags=re.IGNORECASE
            )

            parsed = []

            for block in blocks:

                number_match = re.search(
                    r"(?:Question\s*|Q)?(\d{1,2})[\.\):\-]?",
                    block,
                    flags=re.IGNORECASE
                )

                if number_match:

                    number = number_match.group(1)

                    if 1 <= int(number) <= 25:

                        parsed.append(
                            (number, block.strip())
                        )

            matches = parsed

        # -------------------------------------------------
        # SQL QUERY EXTRACTION
        # -------------------------------------------------

query_data = {}

for number, block in matches:

            sql_match = re.search(
                r"(SELECT|WITH)\s+.*?(?=;|\Z)",
                block,
                flags=re.IGNORECASE | re.DOTALL
            )

            if sql_match:

                query_data[int(number)] = sql_match.group(0).strip()

        # -------------------------------------------------
        # QUERY SELECTOR
        # -------------------------------------------------

                available_questions = sorted(
            query_data.keys()
        )

if available_questions:

            selected_question = st.selectbox(
                "Select SQL Question",
                available_questions
            )

            selected_sql = query_data[
                selected_question
            ]

            st.subheader(
                f"SQL Query — Q{selected_question}"
            )

            st.code(
                selected_sql,
                language="sql"
            )

            if st.button(
                "▶️ Execute Query",
                type="primary"
            ):

                result = run_sql(
                    selected_sql
                )

                if not result.empty:

                    st.success(
                        "Query executed successfully ✅"
                    )

                    st.dataframe(
                        result,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "Query executed, but returned no rows."
                    )

            else:
             st.error(
                      "No SQL questions could be detected."
        )
            
# =========================================================
# CRUD OPERATIONS
# =========================================================

elif page == "✏️ CRUD Operations":

  st.header("✏️ CRUD Operations")
st.write(
        "Create, Read, Update and Delete player records."
    )

crud_operation = st.selectbox(
        "Select Operation",
        [
            "Create Player",
            "Read Players",
            "Update Player",
            "Delete Player"
        ]
    )

    # =====================================================
    # CREATE
    # =====================================================

if crud_operation == "Create Player":

        st.subheader("➕ Add New Player")

        full_name = st.text_input(
            "Full Name"
        )

        country = st.text_input(
            "Country"
        )

        playing_role = st.text_input(
            "Playing Role"
        )

        batting_style = st.text_input(
            "Batting Style"
        )

        bowling_style = st.text_input(
            "Bowling Style"
        )

        if st.button(
            "Add Player",
            type="primary"
        ):

            if full_name.strip() == "":

                st.error(
                    "Player name is required."
                )

            else:

                conn = get_connection()

                try:

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        INSERT INTO players
                        (
                            full_name,
                            country,
                            playing_role,
                            batting_style,
                            bowling_style
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            full_name,
                            country,
                            playing_role,
                            batting_style,
                            bowling_style
                        )
                    )

                    conn.commit()

                    st.success(
                        "Player added successfully ✅"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    conn.close()

    # =====================================================
    # READ
    # =====================================================

elif crud_operation == "Read Players":

        st.subheader("📋 All Players")

        players = run_sql(
            """
            SELECT
                player_id,
                full_name,
                country,
                playing_role,
                batting_style,
                bowling_style
            FROM players
            ORDER BY player_id
            """
        )

        st.dataframe(
            players,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # UPDATE
    # =====================================================

elif crud_operation == "Update Player":

        st.subheader("✏️ Update Player")

        players = run_sql(
            """
            SELECT player_id, full_name
            FROM players
            ORDER BY full_name
            """
        )

        if not players.empty:

            player_map = dict(
                zip(
                    players["full_name"],
                    players["player_id"]
                )
            )

            selected_name = st.selectbox(
                "Select Player",
                list(player_map.keys())
            )

            player_id = player_map[
                selected_name
            ]

            current = run_sql(
                """
                SELECT
                    full_name,
                    country,
                    playing_role,
                    batting_style,
                    bowling_style
                FROM players
                WHERE player_id = ?
                """,
                (player_id,)
            )

            if not current.empty:

                row = current.iloc[0]

                new_name = st.text_input(
                    "Full Name",
                    value=str(row["full_name"])
                )

                new_country = st.text_input(
                    "Country",
                    value=str(row["country"])
                )

                new_role = st.text_input(
                    "Playing Role",
                    value=str(row["playing_role"])
                )

                new_batting = st.text_input(
                    "Batting Style",
                    value=str(row["batting_style"])
                )

                new_bowling = st.text_input(
                    "Bowling Style",
                    value=str(row["bowling_style"])
                )

                if st.button(
                    "Update Player",
                    type="primary"
                ):

                    conn = get_connection()

                    try:

                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            UPDATE players
                            SET
                                full_name = ?,
                                country = ?,
                                playing_role = ?,
                                batting_style = ?,
                                bowling_style = ?
                            WHERE player_id = ?
                            """,
                            (
                                new_name,
                                new_country,
                                new_role,
                                new_batting,
                                new_bowling,
                                player_id
                            )
                        )

                        conn.commit()

                        st.success(
                            "Player updated successfully ✅"
                        )

                    except Exception as e:

                        st.error(
                            f"Error: {e}"
                        )

                    finally:

                        conn.close()

    # =====================================================
    # DELETE
    # =====================================================

elif crud_operation == "Delete Player":

        st.subheader("🗑️ Delete Player")

        players = run_sql(
            """
            SELECT player_id, full_name
            FROM players
            ORDER BY full_name
            """
        )

        if not players.empty:

            player_map = dict(
                zip(
                    players["full_name"],
                    players["player_id"]
                )
            )

            selected_name = st.selectbox(
                "Select Player to Delete",
                list(player_map.keys())
            )

            player_id = player_map[
                selected_name
            ]

            st.warning(
                f"You are about to delete: {selected_name}"
            )

            if st.button(
                "Delete Player",
                type="primary"
            ):

                conn = get_connection()

                try:

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM players
                        WHERE player_id = ?
                        """,
                        (player_id,)
                    )

                    conn.commit()

                    st.success(
                        "Player deleted successfully ✅"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )

                finally:

                    conn.close()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Cricbuzz LiveStats | Python • SQLite • Streamlit • SQL"
)