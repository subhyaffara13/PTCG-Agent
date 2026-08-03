from typing import Any, List

def parse_trusted_proxy_ranges(
    configured_ranges: Any,
    *,
    setting_name: str = TRUSTED_PROXY_RANGES_KEY,
) -> List[TrustedProxyNetwork]:
    networks: List[TrustedProxyNetwork] = []
    for cidr in _normalize_cidr_ranges(configured_ranges, setting_name=setting_name):
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            verbose_proxy_logger.warning(
                "Invalid CIDR in %s: %s, skipping", setting_name, cidr
            )
    return networks

