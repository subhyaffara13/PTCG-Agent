
def parse_cluster_myshardid(resp, **options):
    """
    Parse CLUSTER MYSHARDID response.
    """
    return resp.decode("utf-8")

