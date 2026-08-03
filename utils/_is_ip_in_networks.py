from typing import List, Optional

def _is_ip_in_networks(
    client_ip: Optional[str], networks: List[TrustedProxyNetwork]
) -> bool:
    if not client_ip or not networks:
        return False
    try:
        addr = ipaddress.ip_address(client_ip.strip())
    except ValueError:
        return False
    return any(addr in network for network in networks)

