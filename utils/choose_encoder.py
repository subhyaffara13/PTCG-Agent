from typing import Callable, Tuple

def choose_encoder(accept_header: str) -> Tuple[Callable[[Collector], bytes], str]:
    # Python client library accepts a narrower range of content-types than
    # Prometheus does.
    accept_header = accept_header or ''
    escaping = openmetrics.UNDERSCORES
    for accepted in accept_header.split(','):
        if accepted.split(';')[0].strip() == 'application/openmetrics-text':
            toks = accepted.split(';')
            version = _get_version(toks)
            escaping = _get_escaping(toks)
            # Only return an escaping header if we have a good version and
            # mimetype.
            if not version:
                return (partial(openmetrics.generate_latest, escaping=openmetrics.UNDERSCORES, version="1.0.0"), openmetrics.CONTENT_TYPE_LATEST)
            if version and parse_version(version) >= (1, 0, 0):
                return (partial(openmetrics.generate_latest, escaping=escaping, version=version),
                        f'application/openmetrics-text; version={version}; charset=utf-8; escaping=' + str(escaping))
        elif accepted.split(';')[0].strip() == 'text/plain':
            toks = accepted.split(';')
            version = _get_version(toks)
            escaping = _get_escaping(toks)
            # Only return an escaping header if we have a good version and
            # mimetype.
            if version and parse_version(version) >= (1, 0, 0):
                return (partial(generate_latest, escaping=escaping),
                        CONTENT_TYPE_LATEST + '; escaping=' + str(escaping))
    return generate_latest, CONTENT_TYPE_PLAIN_0_0_4

