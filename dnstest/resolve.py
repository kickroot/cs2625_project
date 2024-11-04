import dns.resolver

def check_cname_exists(domain):
    try:
        # Query specifically for the CNAME record
        result = dns.resolver.resolve(domain, 'CNAME')
        return True if result else False
    except dns.resolver.NoAnswer:
        # No CNAME record exists
        return False
    except dns.resolver.NXDOMAIN:
        # Domain does not exist
        return False
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return False

# Usage
domain = 'dev-archive-orcas2222ound-net.s3.amazonaws.com'
cname_exists = check_cname_exists(domain)
print(f"CNAME exists: {cname_exists}")
