
def instance_ip_grouping_key() -> Dict[str, Any]:
    """Grouping key with instance set to the IP Address of this host."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        if sys.platform == 'darwin':
            # This check is done this way only on MacOS devices
            # it is done this way because the localhost method does
            # not work.
            # This method was adapted from this StackOverflow answer:
            # https://stackoverflow.com/a/28950776
            s.connect(('10.255.255.255', 1))
        else:
            s.connect(('localhost', 0))

        return {'instance': s.getsockname()[0]}

