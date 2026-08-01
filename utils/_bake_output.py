
def _bake_output(registry, accept_header, accept_encoding_header, params, disable_compression):
    """Bake output for metrics output."""
    # Choose the correct plain text format of the output.
    encoder, content_type = choose_encoder(accept_header)
    if 'name[]' in params:
        registry = registry.restricted_registry(params['name[]'])
    output = encoder(registry)
    headers = [('Content-Type', content_type)]
    # If gzip encoding required, gzip the output.
    if not disable_compression and gzip_accepted(accept_encoding_header):
        output = gzip.compress(output)
        headers.append(('Content-Encoding', 'gzip'))
    return '200 OK', headers, output

