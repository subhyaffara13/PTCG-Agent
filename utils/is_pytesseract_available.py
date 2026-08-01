
def is_pytesseract_available() -> bool:
    return _is_package_available("pytesseract")[0] and is_vision_available()

