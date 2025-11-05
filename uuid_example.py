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
    print()
    
    # UUID formats
    print("UUID Formats:")
    example_uuid = uuid.uuid4()
    print(f"Version: {example_uuid.version}")
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
    print()
    
    # UUID1 - Based on MAC address and timestamp
    print("UUID1 - MAC address and timestamp based:")
    uuid1_example = uuid.uuid1()
    print(f"UUID1: {uuid1_example}")
    print(f"Version: {uuid1_example.version}")
    print(f"Timestamp: {uuid1_example.time}")
    print()
    
    # UUID3 and UUID5 - Name-based (deterministic)
    print("UUID3 and UUID5 - Name-based (deterministic):")
    namespace = uuid.NAMESPACE_DNS
    name = "example.com"
    
    uuid3_1 = uuid.uuid3(namespace, name)
    uuid3_2 = uuid.uuid3(namespace, name)
    print(f"UUID3 (MD5): {uuid3_1}")
    print(f"UUID3 again: {uuid3_2}")
    print(f"Same name = same UUID: {uuid3_1 == uuid3_2}")
    
    uuid5_example = uuid.uuid5(namespace, name)
    print(f"UUID5 (SHA-1): {uuid5_example}")


if __name__ == "__main__":
    main()
