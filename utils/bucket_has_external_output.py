
def bucket_has_external_output(bucket: Bucket) -> bool:
    nodes_in_bucket = set()
    # we want to iterate in reverse order, but clumsi-luckily the bucket.nodes list was already created backwards
    # so we don't reverse it here
    for node in bucket.nodes:
        # assume node.op != output, since those are filtered in the original iteration
        nodes_in_bucket.add(node)
        for user in node.users:
            if user not in nodes_in_bucket:
                return True
    return False

