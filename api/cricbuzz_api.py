import os
import requests


# =========================================================
# CRICBUZZ API CONFIGURATION
# =========================================================

BASE_URL = os.getenv(
    "CRICBUZZ_BASE_URL",
    "https://cricbuzz-cricket.p.rapidapi.com"
)

API_KEY = os.getenv("CRICBUZZ_API_KEY", "")

API_HOST = os.getenv(
    "CRICBUZZ_API_HOST",
    "cricbuzz-cricket.p.rapidapi.com"
)


# =========================================================
# COMMON HEADERS
# =========================================================

def get_headers():
    """
    Return headers required for Cricbuzz RapidAPI.
    """

    return {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }


# =========================================================
# COMMON API REQUEST FUNCTION
# =========================================================

def make_request(endpoint):
    """
    Send GET request to Cricbuzz API.
    """

    if not API_KEY:
        return {
            "success": False,
            "error": "Cricbuzz API key is not configured."
        }

    url = f"{BASE_URL}{endpoint}"

    try:

        response = requests.get(
            url,
            headers=get_headers(),
            timeout=15
        )

        response.raise_for_status()

        return {
            "success": True,
            "data": response.json()
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "API request timed out."
        }

    except requests.exceptions.HTTPError as e:

        return {
            "success": False,
            "error": f"HTTP Error: {e}"
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"API Request Error: {e}"
        }

    except ValueError:

        return {
            "success": False,
            "error": "Invalid JSON response received from API."
        }


# =========================================================
# LIVE MATCHES
# =========================================================

def get_live_matches():
    """
    Fetch currently live cricket matches.
    """

    return make_request(
        "/matches/v1/live"
    )


# =========================================================
# RECENT MATCHES
# =========================================================

def get_recent_matches():
    """
    Fetch recent cricket matches.
    """

    return make_request(
        "/matches/v1/recent"
    )


# =========================================================
# UPCOMING MATCHES
# =========================================================

def get_upcoming_matches():
    """
    Fetch upcoming cricket matches.
    """

    return make_request(
        "/matches/v1/upcoming"
    )


# =========================================================
# TOP PLAYER STATS
# =========================================================

def get_top_player_stats():
    """
    Fetch top player statistics.
    """

    return make_request(
        "/stats/v1/topstats"
    )


# =========================================================
# SERIES LIST
# =========================================================

def get_series_list():
    """
    Fetch cricket series information.
    """

    return make_request(
        "/series/v1/series"
    )


# =========================================================
# SERIES DETAILS
# =========================================================

def get_series_details(series_id):
    """
    Fetch details of a particular cricket series.
    """

    return make_request(
        f"/series/v1/{series_id}"
    )


# =========================================================
# MATCH SCORECARD
# =========================================================

def get_match_scorecard(match_id):
    """
    Fetch detailed scorecard of a match.
    """

    return make_request(
        f"/mcenter/v1/{match_id}"
    )


# =========================================================
# PLAYER DETAILS
# =========================================================

def get_player_details(player_id):
    """
    Fetch details of a particular player.
    """

    return make_request(
        f"/players/v1/{player_id}"
    )


# =========================================================
# API STATUS
# =========================================================

def api_configured():
    """
    Check whether API key is available.
    """

    return bool(API_KEY)


# =========================================================
# TEST API CONNECTION
# =========================================================

if __name__ == "__main__":

    print("====================================")
    print("      CRICBUZZ API CONNECTION")
    print("====================================")

    if not api_configured():

        print("❌ API key not configured.")
        print("Please configure CRICBUZZ_API_KEY.")

    else:

        print("API key found.")
        print("Testing live matches...")

        result = get_live_matches()

        if result["success"]:

            print("✅ API connection successful!")

            data = result["data"]

            print(
                "Response received successfully."
            )

            print(
                f"Response type: {type(data).__name__}"
            )

        else:

            print("❌ API connection failed.")
            print(
                f"Error: {result['error']}"
            )