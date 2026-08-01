
def get_distribution(dist: _DistributionT) -> _DistributionT: ...


def get_distribution(dist: _PkgReqType) -> Distribution: ...


def get_distribution(dist: Distribution | _PkgReqType) -> Distribution:
    """Return a current distribution object for a Requirement or string"""
    if isinstance(dist, str):
        dist = Requirement.parse(dist)
    if isinstance(dist, Requirement):
        dist = get_provider(dist)
    if not isinstance(dist, Distribution):
        raise TypeError("Expected str, Requirement, or Distribution", dist)
    return dist

