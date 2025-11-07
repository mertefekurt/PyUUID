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
    print(f"Node: {uuid1_test.node}")
    
    print(f"\nUUID3 Properties:")
    uuid3_test = uuid.uuid3(uuid.NAMESPACE_DNS, "test")
    print(f"UUID3: {uuid3_test}")
    print(f"Version: {uuid3_test.version}")
    print(f"Variant: {uuid3_test.variant}")
    
    print(f"\nUUID5 Properties:")
    uuid5_test = uuid.uuid5(uuid.NAMESPACE_DNS, "test")
    print(f"UUID5: {uuid5_test}")
    print(f"Version: {uuid5_test.version}")


if __name__ == "__main__":
    main()

