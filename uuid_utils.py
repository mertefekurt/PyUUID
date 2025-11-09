import uuid
from typing import Optional


def is_valid_uuid(uuid_string: str) -> bool:
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False


def generate_user_id() -> uuid.UUID:
    return uuid.uuid4()


def generate_session_token() -> str:
    return uuid.uuid4().hex


def generate_filename(extension: str = "txt") -> str:
    return f"file_{uuid.uuid4().hex[:8]}.{extension}"


def generate_short_id(length: int = 8) -> str:
    if length < 1 or length > 32:
        raise ValueError("length must be between 1 and 32")
    return uuid.uuid4().hex[:length]


def generate_transaction_id() -> str:
    return uuid.uuid4().hex.upper()


def generate_api_key() -> str:
    return uuid.uuid4().hex


def uuid_from_string(uuid_string: str) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(uuid_string)
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    print("UUID Utils")
    print("-" * 40)
    print(f"User ID: {generate_user_id()}")
    print(f"Session Token: {generate_session_token()}")
    print(f"Filename: {generate_filename()}")
    print(f"Transaction ID: {generate_transaction_id()}")
    print(f"API Key: {generate_api_key()}")
    print(f"Short ID: {generate_short_id(12)}")
    print(f"Valid UUID check: {is_valid_uuid(str(generate_user_id()))}")
