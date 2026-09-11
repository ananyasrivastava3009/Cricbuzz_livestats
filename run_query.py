import sqlite3
import re

DB_FILE = "database/cricket.db"
SQL_FILE = "database/sql/25_queries.sql"


def load_questions():
    with open(SQL_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    # QUESTION 1, QUESTION 2 ... QUESTION 25 खोजेगा
    pattern = r"(?i)QUESTION\s+(\d+)"
    matches = list(re.finditer(pattern, content))

    questions = {}

    for i, match in enumerate(matches):
        question_no = int(match.group(1))

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        sql = content[start:end].strip()

        # Comment/separator lines हटाना
        lines = []

        for line in sql.splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("--"):
                continue

            lines.append(line)

        sql = "\n".join(lines).strip()

        # सिर्फ valid SQL रखना
        if sql:
            questions[question_no] = sql

    return questions


def run_query():
    print("\n========================================")
    print("       CRICBUZZ SQL QUERY RUNNER")
    print("========================================\n")

    questions = load_questions()

    print("Questions detected:", sorted(questions.keys()))
    print("Total questions loaded:", len(questions))

    missing = [i for i in range(1, 26) if i not in questions]

    if missing:
        print("\nWARNING: These questions were not detected:")
        print(missing)

    if not questions:
        print("\nERROR: No SQL questions found.")
        return

    while True:

        user_input = input(
            "\nEnter question number (1-25) or 0 to exit: "
        ).strip()

        if user_input == "0":
            print("Exiting...")
            break

        if not user_input.isdigit():
            print("Please enter a valid number.")
            continue

        question_no = int(user_input)

        if question_no not in questions:
            print(
                f"Question {question_no} was not found in 25_queries.sql"
            )
            print("Available questions:", sorted(questions.keys()))
            continue

        sql = questions[question_no]

        print("\n========================================")
        print(f"          QUESTION {question_no}")
        print("========================================")
        print("\nSQL:")
        print(sql)

        connection = None

        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            cursor.execute(sql)
            results = cursor.fetchall()

            print("\nRESULT:")
            print("----------------------------------------")

            if cursor.description:
                columns = [column[0] for column in cursor.description]
                print(" | ".join(columns))
                print("----------------------------------------")

            if results:
                for row in results:
                    print(row)
            else:
                print("No records found.")

            print("----------------------------------------")
            print(f"Total records: {len(results)}")

        except Exception as error:
            print("\nERROR:")
            print(error)

        finally:
            if connection:
                connection.close()


if __name__ == "__main__":
    run_query()