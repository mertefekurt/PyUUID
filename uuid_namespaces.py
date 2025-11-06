import uuid


def main():
    print("UUID Namespaces")
    print("-" * 40)
    
    print("Standard Namespaces:")
    print(f"NAMESPACE_DNS: {uuid.NAMESPACE_DNS}")
    print(f"NAMESPACE_URL: {uuid.NAMESPACE_URL}")
    print(f"NAMESPACE_OID: {uuid.NAMESPACE_OID}")
    print(f"NAMESPACE_X500: {uuid.NAMESPACE_X500}")
    
    print("\nUsing NAMESPACE_DNS:")
    uuid5_dns = uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")
    print(f"UUID5 for example.com: {uuid5_dns}")
    
    print("\nUsing NAMESPACE_URL:")
    uuid5_url = uuid.uuid5(uuid.NAMESPACE_URL, "https://example.com")
    print(f"UUID5 for https://example.com: {uuid5_url}")


if __name__ == "__main__":
    main()

