"""CLI utilities for the backend.

Usage:
    python -m app.cli create-user <username> <password>
    python -m app.cli reset-password <username> <new_password>
"""

from __future__ import annotations

import sys

from app.database import SessionLocal, init_db
from app.models import User
from app.security import hash_password


def create_user(username: str, password: str) -> None:
    init_db()
    with SessionLocal() as db:
        if db.query(User).filter(User.username == username).first():
            print(f"User '{username}' already exists")
            sys.exit(1)
        user = User(username=username, password_hash=hash_password(password))
        db.add(user)
        db.commit()
        print(f"Created user '{username}' with id={user.id}")


def reset_password(username: str, password: str) -> None:
    init_db()
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            print(f"User '{username}' not found")
            sys.exit(1)
        user.password_hash = hash_password(password)
        db.add(user)
        db.commit()
        print(f"Password updated for user '{username}'")


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = argv[1]
    if command == "create-user" and len(argv) == 4:
        create_user(argv[2], argv[3])
    elif command == "reset-password" and len(argv) == 4:
        reset_password(argv[2], argv[3])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
