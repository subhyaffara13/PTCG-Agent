
def get_in_flight_requests() -> int:
    """Module-level convenience wrapper used by the /health/backlog endpoint."""
    return InFlightRequestsMiddleware.get_count()

