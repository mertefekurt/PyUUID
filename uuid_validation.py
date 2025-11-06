
import uuid


def is_valid_uuid(uuid_string):

    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def main():
    print("UUID Validation")
    print("-" * 40)
    

    valid_uuids = [
        str(uuid.uuid4()),
        "550e8400-e29b-41d4-a716-446655440000"
    ]
    

    invalid_uuids = [
        "not-a-uuid",
        "12345",
        "550e8400-e29b-41d4"
    ]
    
    print("Valid UUIDs:")
    for u in valid_uuids:
        print(f"  {u}: {is_valid_uuid(u)}")
    
    print("\nInvalid UUIDs:")
    for u in invalid_uuids:
        print(f"  {u}: {is_valid_uuid(u)}")
    
    print("\nUUID Version Check:")
    test_uuid = uuid.uuid4()
    print(f"UUID: {test_uuid}")
    print(f"Version: {test_uuid.version}")
    
    print("\nValidate multiple formats:")
    formats = [
        str(test_uuid),
        test_uuid.hex,
        str(test_uuid.int)
    ]
    for fmt in formats:
        try:
            uuid_obj = uuid.UUID(fmt) if fmt != str(test_uuid.int) else None
            if uuid_obj:
                print(f"  {fmt[:30]}...: Valid")
        except:
            print(f"  {fmt[:30]}...: Invalid")


if __name__ == "__main__":
    main()

