
def disable_created_metrics():
    """Disable exporting _created metrics on counters, histograms, and summaries."""
    global _use_created
    _use_created = False

