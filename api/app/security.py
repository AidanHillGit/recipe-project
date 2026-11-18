from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return an Argon2 hash of a plain-text password."""
    # return the hasher's .hash() of password
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain-text password against a stored hash."""
    # return the hasher's .verify() of the two; check the docs for argument order
    return password_hasher.verify(password, password_hash)
