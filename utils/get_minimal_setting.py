
def get_minimal_setting() -> bool:
    """Ask the user if they want to use the minimal setting."""
    return validate_yes_no(
        "Do you want a minimal configuration without comments or default values?", "no"
    )

