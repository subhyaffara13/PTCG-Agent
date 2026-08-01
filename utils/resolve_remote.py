
def resolve_remote(uri, handlers):
    """
    Resolve a remote ``uri``.

    .. note::

        urllib library is used to fetch requests from the remote ``uri``
        if handlers does notdefine otherwise.
    """
    scheme = urlparse.urlsplit(uri).scheme
    if scheme in handlers:
        result = handlers[scheme](uri)
    else:
        from urllib.request import urlopen

        req = urlopen(uri)
        encoding = req.info().get_content_charset() or 'utf-8'
        try:
            result = json.loads(req.read().decode(encoding),)
        except ValueError as exc:
            raise JsonSchemaDefinitionException('{} failed to decode: {}'.format(uri, exc))
        finally:
            req.close()
    return result

