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
    
    uuid3_dns = uuid.uuid3(uuid.NAMESPACE_DNS, "example.com")
    print(f"UUID3 for example.com: {uuid3_dns}")
    
    print("\nUsing NAMESPACE_URL:")
    uuid5_url = uuid.uuid5(uuid.NAMESPACE_URL, "https://example.com")
    print(f"UUID5 for https://example.com: {uuid5_url}")
    
    print("\nSame name, different namespace:")
    name = "test"
    uuid5_dns_test = uuid.uuid5(uuid.NAMESPACE_DNS, name)
    uuid5_url_test = uuid.uuid5(uuid.NAMESPACE_URL, name)
    print(f"DNS namespace: {uuid5_dns_test}")
    print(f"URL namespace: {uuid5_url_test}")
    print(f"Different: {uuid5_dns_test != uuid5_url_test}")


if __name__ == "__main__":
    main()

