import uuid


def main():
    print("UUID Conversion")
    print("-" * 40)
    
    test_uuid = uuid.uuid4()
    
    print(f"Original UUID: {test_uuid}")
    print()
    
    print("String conversion:")
    uuid_str = str(test_uuid)
    print(f"String: {uuid_str}")
    uuid_from_str = uuid.UUID(uuid_str)
    print(f"Back to UUID: {uuid_from_str}")
    print()
    
    print("Hex conversion:")
    uuid_hex = test_uuid.hex
    print(f"Hex: {uuid_hex}")
    uuid_from_hex = uuid.UUID(uuid_hex)
    print(f"Back to UUID: {uuid_from_hex}")
    print()
    
    print("Int conversion:")
    uuid_int = test_uuid.int
    print(f"Int: {uuid_int}")
    uuid_from_int = uuid.UUID(int=uuid_int)
    print(f"Back to UUID: {uuid_from_int}")
    print()
    
    print("Bytes conversion:")
    uuid_bytes = test_uuid.bytes
    print(f"Bytes: {uuid_bytes}")
    uuid_from_bytes = uuid.UUID(bytes=uuid_bytes)
    print(f"Back to UUID: {uuid_from_bytes}")
    print()
    
    print("All conversions match:")
    print(f"Original == String: {test_uuid == uuid_from_str}")
    print(f"Original == Hex: {test_uuid == uuid_from_hex}")
    print(f"Original == Int: {test_uuid == uuid_from_int}")
    print(f"Original == Bytes: {test_uuid == uuid_from_bytes}")


if __name__ == "__main__":
    main()

