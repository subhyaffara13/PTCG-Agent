
def _get_domain_info(info):
    domain_info = {"endpoints": info} if isinstance(info, tuple) else info
    typical = domain_info.pop("typical", None)
    return domain_info, typical

