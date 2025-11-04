"""
Python UUID examples
UUID (Universally Unique Identifier) 
"""

import uuid


def main():
    print("Python UUID examples")
    print("-" * 40)
    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    
    print(f"UUID 1: {uuid1}")
    print(f"UUID 2: {uuid2}")
    print(f"Is unique? {uuid1 != uuid2}")
    print(f"Version: {example_uuid.version}")
    print()
    
    # UUID formats
    print("UUID Formats:")
    example_uuid = uuid.uuid4()
    print(f"String: {str(example_uuid)}")
    print(f"Hex: {example_uuid.hex}")
    print(f"Int: {example_uuid.int}")
    print(f"Bytes: {example_uuid.bytes}")
    print()
    
    # Create UUID from string
    print("Create UUID from string:")
    uuid_string = str(example_uuid)
    uuid_from_string = uuid.UUID(uuid_string)
    print(f"Original: {example_uuid}")
    print(f"From string: {uuid_from_string}")
    print(f"Are equal: {example_uuid == uuid_from_string}")


if __name__ == "__main__":
    main()
