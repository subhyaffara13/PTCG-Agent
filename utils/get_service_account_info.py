
def get_service_account_info(request, service_account="default"):
    """Get information about a service account from the metadata server.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        service_account (str): The string 'default' or a service account email
            address. The determines which service account for which to acquire
            information.

    Returns:
        Mapping: The service account's information, for example::

            {
                'email': '...',
                'scopes': ['scope', ...],
                'aliases': ['default', '...']
            }

    Raises:
        google.auth.exceptions.TransportError: if an error occurred while
            retrieving metadata.
    """
    path = "instance/service-accounts/{0}/".format(service_account)
    # See https://cloud.google.com/compute/docs/metadata#aggcontents
    # for more on the use of 'recursive'.
    return get(request, path, params={"recursive": "true"})

