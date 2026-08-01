
def parse_cluster_info(response, **options):
    response = str_if_bytes(response)
    return dict(line.split(":") for line in response.splitlines() if line)

