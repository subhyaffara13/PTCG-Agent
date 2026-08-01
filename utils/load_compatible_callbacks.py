
def load_compatible_callbacks() -> Dict:
    """
    Load the generic_api_compatible_callbacks.json file

    Returns:
        Dict: Dictionary of compatible callbacks configuration
    """
    try:
        json_path = os.path.join(
            os.path.dirname(__file__), "generic_api_compatible_callbacks.json"
        )
        with open(json_path, "r") as f:
            return json.load(f)
    except Exception as e:
        verbose_logger.warning(
            f"Error loading generic_api_compatible_callbacks.json: {str(e)}"
        )
        return {}

