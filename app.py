import logging
import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Frontend configuration
CORS(app, resources={
    r"/api/*": {
        "origins": "http://44.222.70.48"
    }
})

# RDS configuration
db_config = {
    "host": "project-01.cwnesmmw84rg.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Admin&123",
    "database": "ProjectDB",
    "port": 3306,
    "connection_timeout": 10
}

@app.route("/api/students", methods=["GET"])
def get_students():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, username, email "
            "FROM students ORDER BY id"
        )
        students = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(students),
            "students": students
        })

    except mysql.connector.Error:
        app.logger.exception("Database error")
        return jsonify({
            "success": False,
            "message": "Unable to retrieve students records"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
