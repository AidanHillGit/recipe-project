from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return an Argon2 hash of a plain-text password."""
    # return the hasher's .hash() of password
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain-text password against a stored hash."""
    # return the hasher's .verify() of the two; check the docs for argument order
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    """Create a signed access token for a user that expires after the configured time"""
    lifetime = timedelta(minutes=settings.access_token_minutes)
    expires_at = datetime.now(timezone.utc) + lifetime

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256",
    )

    return token
