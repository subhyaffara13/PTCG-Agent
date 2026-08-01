
def _compress_payload(data: bytes, compression: CompressionType) -> Tuple[bytes, List[Tuple[str, str]]]:
    headers = [('Content-Type', CONTENT_TYPE_PLAIN_0_0_4)]
    if compression is None:
        return data, headers

    encoding = compression.lower()
    if encoding == 'gzip':
        headers.append(('Content-Encoding', 'gzip'))
        return gzip.compress(data), headers
    if encoding == 'snappy':
        if not SNAPPY_AVAILABLE:
            raise RuntimeError('Snappy compression requires the python-snappy package to be installed.')
        headers.append(('Content-Encoding', 'snappy'))
        compressor = snappy.StreamCompressor()
        compressed = compressor.compress(data)
        flush = getattr(compressor, 'flush', None)
        if callable(flush):
            compressed += flush()
        return compressed, headers
    raise ValueError(f"Unsupported compression type: {compression}")

