
def _dist_matches_req(egg_dist, req):
    return (
        packaging.utils.canonicalize_name(egg_dist.name)
        == packaging.utils.canonicalize_name(req.name)
        and egg_dist.version in req.specifier
    )

