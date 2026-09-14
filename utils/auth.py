import sqlite3
import hashlib
import secrets
from pathlib import Path


DB_PATH = Path("data/users.db")


def init_auth_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    salt, stored_hash = stored_password.split("$")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return secrets.compare_digest(
        password_hash,
        stored_hash
    )


def create_user(email, password):
    try:
        conn = sqlite3.connect(DB_PATH)

        conn.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (
                email.lower().strip(),
                hash_password(password)
            )
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        return False


def authenticate_user(email, password):
    conn = sqlite3.connect(DB_PATH)

    user = conn.execute(
        """
        SELECT id, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (email.lower().strip(),)
    ).fetchone()

    conn.close()

    if user and verify_password(password, user[2]):
        return {
            "id": user[0],
            "email": user[1]
        }

    return None