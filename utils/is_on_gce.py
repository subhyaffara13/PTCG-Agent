
def is_on_gce(request):
    """Checks to see if the code runs on Google Compute Engine

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.

    Returns:
        bool: True if the code runs on Google Compute Engine, False otherwise.
    """
    if _NO_GCE_CHECK:
        return False

    if ping(request):
        return True

    if os.name == "nt":
        # TODO: implement GCE residency detection on Windows
        return False

    # Detect GCE residency on Linux
    return detect_gce_residency_linux()

