
import uuid


def generate_user_id():

    return uuid.uuid4()


def generate_session_token():

    return uuid.uuid4().hex


def generate_filename(extension="txt"):

    return f"file_{uuid.uuid4().hex[:8]}.{extension}"


if __name__ == "__main__":
    print("UUID Utils")
    print("-" * 40)
    print(f"User ID: {generate_user_id()}")
    print(f"Session Token: {generate_session_token()}")
    print(f"Filename: {generate_filename()}")

