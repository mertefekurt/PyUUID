
import uuid


def main():
    print("UUID Comparison")
    print("-" * 40)
    
    uuid_a = uuid.uuid4()
    uuid_b = uuid.uuid4()
    uuid_c = uuid.UUID(str(uuid_a))
    
    print(f"UUID A: {uuid_a}")
    print(f"UUID B: {uuid_b}")
    print(f"UUID C (from A): {uuid_c}")
    print()
    
    print("Comparisons:")
    print(f"A == B: {uuid_a == uuid_b}")
    print(f"A == C: {uuid_a == uuid_c}")
    print(f"A != B: {uuid_a != uuid_b}")
    
    uuid_from_hex = uuid.UUID(uuid_a.hex)
    print(f"UUID from hex: {uuid_from_hex}")
    print(f"A == hex UUID: {uuid_a == uuid_from_hex}")


if __name__ == "__main__":
    main()

