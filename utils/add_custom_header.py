
def add_custom_header(headers):
    """Closure to capture the headers and add them."""

    def callback(request, **kwargs):
        """Actual callback function that Boto3 will call."""
        for header_name, header_value in headers.items():
            request.headers.add_header(header_name, header_value)

    return callback

