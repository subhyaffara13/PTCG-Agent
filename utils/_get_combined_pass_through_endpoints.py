
def _get_combined_pass_through_endpoints(
    pass_through_endpoints: Union[List[Dict], List[PassThroughGenericEndpoint]],
    config_pass_through_endpoints: List[Dict],
):
    """Get combined pass-through endpoints from db + config"""
    return pass_through_endpoints + config_pass_through_endpoints

