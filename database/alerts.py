import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "leakage_history.db"
)



def create_alert_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            alert_type TEXT,

            message TEXT,

            severity TEXT,

            probability REAL,

            timestamp TEXT

        )
        """
    )


    conn.commit()
    conn.close()



def save_alert(
    alert_type,
    message,
    severity,
    probability
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    # Last alert check

    cursor.execute(
        """
        SELECT 
            severity,
            probability
        FROM alerts
        ORDER BY id DESC
        LIMIT 1
        """
    )


    last_alert = cursor.fetchone()



    if last_alert:

        old_severity = last_alert[0]

        old_probability = float(
            last_alert[1]
        )


        # duplicate prevention

        if (

            old_severity == severity

            and abs(
                old_probability - probability
            ) < 5

        ):

            conn.close()

            return False



    cursor.execute(
        """
        INSERT INTO alerts
        (
            alert_type,
            message,
            severity,
            probability,
            timestamp
        )

        VALUES(?,?,?,?,?)

        """,

        (
            alert_type,

            message,

            severity,

            float(probability),

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )
    )


    conn.commit()

    conn.close()


    return True
def get_alerts():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            alert_type,
            message,
            severity,
            probability,
            timestamp

        FROM alerts

        ORDER BY id DESC
LIMIT 5
        """
    )


    rows = cursor.fetchall()


    conn.close()


    result = []


    for row in rows:

        result.append(

            {
                "alert_type": row[0],
                "message": row[1],
                "severity": row[2],
                "probability": row[3],
                "timestamp": row[4]
            }

        )


    return result