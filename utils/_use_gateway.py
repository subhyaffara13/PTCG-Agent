from typing import Any, Callable, Dict, List, Optional, Tuple

def _use_gateway(
        method: str,
        gateway: str,
        job: str,
        registry: Optional[Collector],
        grouping_key: Optional[Dict[str, Any]],
        timeout: Optional[float],
        handler: Callable,
        compression: CompressionType = None,
) -> None:
    gateway_url = urlparse(gateway)
    # See https://bugs.python.org/issue27657 for details on urlparse in py>=3.7.6.
    if not gateway_url.scheme or gateway_url.scheme not in ['http', 'https']:
        gateway = f'http://{gateway}'

    gateway = gateway.rstrip('/')
    url = '{}/metrics/{}/{}'.format(gateway, *_escape_grouping_key("job", job))

    if grouping_key is None:
        grouping_key = {}
    url += ''.join(
        '/{}/{}'.format(*_escape_grouping_key(str(k), str(v)))
        for k, v in sorted(grouping_key.items()))

    data = b''
    headers: List[Tuple[str, str]] = []
    if method != 'DELETE':
        if registry is None:
            registry = REGISTRY
        data = generate_latest(registry)
        data, headers = _compress_payload(data, compression)
    else:
        # DELETE requests still need Content-Type header per test expectations
        headers = [('Content-Type', CONTENT_TYPE_PLAIN_0_0_4)]
        if compression is not None:
            raise ValueError('Compression is not supported for DELETE requests.')

    handler(
        url=url, method=method, timeout=timeout,
        headers=headers, data=data,
    )()

