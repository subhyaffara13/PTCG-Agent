
def access_pypi():
    # Detect if tests are being run without connectivity
    if not os.environ.get('NETWORK_REQUIRED', False):  # pragma: nocover
        try:
            urlopen('https://pypi.org', timeout=1)
        except URLError:
            # No network, disable most of these tests
            return False

    return True

