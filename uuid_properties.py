import uuid


def main():
    print("UUID Properties")
    print("-" * 40)
    
    test_uuid = uuid.uuid4()
    
    print(f"UUID: {test_uuid}")
    print(f"Version: {test_uuid.version}")
    print(f"Variant: {test_uuid.variant}")
    print(f"Hex: {test_uuid.hex}")
    print(f"Int: {test_uuid.int}")
    print(f"Bytes length: {len(test_uuid.bytes)}")
    
    uuid1_test = uuid.uuid1()
    print(f"\nUUID1: {uuid1_test}")
    print(f"Timestamp: {uuid1_test.time}")
    print(f"Clock sequence: {uuid1_test.clock_seq}")


if __name__ == "__main__":
    main()

