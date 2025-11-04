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


if __name__ == "__main__":
    main()
