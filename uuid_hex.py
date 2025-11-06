import uuid


def main():
    print("UUID Hex Operations")
    print("-" * 40)
    
    test_uuid = uuid.uuid4()
    
    print(f"UUID: {test_uuid}")
    print(f"Hex: {test_uuid.hex}")
    print(f"Hex length: {len(test_uuid.hex)}")
    
    hex_string = test_uuid.hex
    uuid_from_hex = uuid.UUID(hex_string)
    
    print(f"\nFrom hex string: {hex_string}")
    print(f"Reconstructed UUID: {uuid_from_hex}")
    print(f"Match: {test_uuid == uuid_from_hex}")
    
    print(f"\nFirst 8 chars: {test_uuid.hex[:8]}")
    print(f"Last 8 chars: {test_uuid.hex[-8:]}")


if __name__ == "__main__":
    main()

