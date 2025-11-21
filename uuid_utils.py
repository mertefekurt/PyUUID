import uuid
from typing import Optional


def is_valid_uuid(uuid_string: str) -> bool:
    if not isinstance(uuid_string, str):
        return False
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
    if not extension or not isinstance(extension, str):
        raise ValueError("extension must be a non-empty string")
    return f"file_{uuid.uuid4().hex[:8]}.{extension}"


def generate_short_id(length: int = 8) -> str:
    if not isinstance(length, int) or length < 1 or length > 32:
        raise ValueError("length must be an integer between 1 and 32")
    return uuid.uuid4().hex[:length]


def generate_transaction_id() -> str:
    return uuid.uuid4().hex.upper()


def generate_api_key() -> str:
    return uuid.uuid4().hex


def generate_namespace_uuid(namespace: str, name: str) -> uuid.UUID:
    if not isinstance(namespace, str) or not isinstance(name, str):
        raise ValueError("namespace and name must be strings")
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, namespace)
    return uuid.uuid5(namespace_uuid, name)


def uuid_from_string(uuid_string: str) -> Optional[uuid.UUID]:
    if not isinstance(uuid_string, str):
        return None
    try:
        return uuid.UUID(uuid_string)
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    test_uuid = generate_user_id()
    print("UUID Utils")
    print("-" * 40)
    print(f"User ID: {test_uuid}")
    print(f"Session Token: {generate_session_token()}")
    print(f"Filename: {generate_filename()}")
    print(f"Transaction ID: {generate_transaction_id()}")
    print(f"API Key: {generate_api_key()}")
    print(f"Short ID: {generate_short_id(12)}")
    print(f"Valid UUID check: {is_valid_uuid(str(test_uuid))}")
