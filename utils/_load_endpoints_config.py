
def _load_endpoints_config() -> Dict:
    """Load the endpoints configuration from JSON file."""
    config_path = Path(__file__).parent / "endpoints.json"
    with open(config_path) as f:
        return json.load(f)


def _load_endpoints_config() -> Dict:
    """Load the endpoints configuration from JSON file."""
    config_path = Path(__file__).parent.parent.parent / "containers" / "endpoints.json"
    with open(config_path) as f:
        return json.load(f)


def _load_endpoints_config() -> Dict:
    """Load the endpoints configuration from JSON file."""
    config_path = Path(__file__).parent.parent.parent / "containers" / "endpoints.json"
    with open(config_path) as f:
        return json.load(f)

