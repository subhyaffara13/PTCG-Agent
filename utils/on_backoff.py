
def on_backoff(details):
    # The 'tries' key in the details dictionary contains the number of completed tries
    verbose_proxy_logger.debug("Backing off... this was attempt # %s", details["tries"])


def on_backoff(details):
    # The 'tries' key in the details dictionary contains the number of completed tries
    print_verbose(f"Backing off... this was attempt #{details['tries']}")

