from typing import Optional, Union

def check_protocol_version(
    protocol: Optional[Union[str, int]], expected_version: int = 3
) -> bool:
    if protocol is None:
        protocol = DEFAULT_RESP_VERSION
    if isinstance(protocol, str):
        try:
            protocol = int(protocol)
        except ValueError:
            return False
    return protocol == expected_version

