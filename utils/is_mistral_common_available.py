
def is_mistral_common_available() -> bool:
    return is_vision_available() and _is_package_available("mistral_common")[0]

