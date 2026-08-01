
def _read_url(url):
    with urlopen(url) as r:
        return r.read().decode(r.headers.get_content_charset("utf-8"))

