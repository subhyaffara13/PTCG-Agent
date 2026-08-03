from typing import Callable

def make_wsgi_app(registry: Collector = REGISTRY, disable_compression: bool = False) -> Callable:
    """Create a WSGI app which serves the metrics from a registry."""

    def prometheus_app(environ, start_response):
        # Prepare parameters
        accept_header = environ.get('HTTP_ACCEPT')
        accept_encoding_header = environ.get('HTTP_ACCEPT_ENCODING')
        params = parse_qs(environ.get('QUERY_STRING', ''))
        method = environ['REQUEST_METHOD']

        if method == 'OPTIONS':
            status = '200 OK'
            headers = [('Allow', 'OPTIONS,GET')]
            output = b''
        elif method != 'GET':
            status = '405 Method Not Allowed'
            headers = [('Allow', 'OPTIONS,GET')]
            output = '# HTTP {}: {}; use OPTIONS or GET\n'.format(status, method).encode()
        elif environ['PATH_INFO'] == '/favicon.ico':
            # Serve empty response for browsers
            status = '200 OK'
            headers = []
            output = b''
        else:
            # Note: For backwards compatibility, the URI path for GET is not
            # constrained to the documented /metrics, but any path is allowed.
            # Bake output
            status, headers, output = _bake_output(registry, accept_header, accept_encoding_header, params, disable_compression)
        # Return output
        start_response(status, headers)
        return [output]

    return prometheus_app

