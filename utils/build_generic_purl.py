
def build_generic_purl(uri):
    """
    Return a PackageURL from `uri`, if `uri` is a parsable URL, or None

    `uri` is assumed to be a download URL, e.g. https://example.com/example.tar.gz
    """
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme and parsed_uri.netloc and parsed_uri.path:
        # Get file name from `uri`
        uri_path_segments = get_path_segments(uri)
        if uri_path_segments:
            file_name = uri_path_segments[-1]
            return PackageURL(type="generic", name=file_name, qualifiers={"download_url": uri})

