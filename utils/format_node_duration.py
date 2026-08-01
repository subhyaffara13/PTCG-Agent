
def format_node_duration(seconds: float) -> str:
    """Format the given seconds in a human readable manner to show in the test progress."""
    # The formatting is designed to be compact and readable, with at most 7 characters
    # for durations below 100 hours.
    if seconds < 0.00001:
        return f" {seconds * 1000000:.3f}us"
    if seconds < 0.0001:
        return f" {seconds * 1000000:.2f}us"
    if seconds < 0.001:
        return f" {seconds * 1000000:.1f}us"
    if seconds < 0.01:
        return f" {seconds * 1000:.3f}ms"
    if seconds < 0.1:
        return f" {seconds * 1000:.2f}ms"
    if seconds < 1:
        return f" {seconds * 1000:.1f}ms"
    if seconds < 60:
        return f" {seconds:.3f}s"
    if seconds < 3600:
        return f" {seconds // 60:.0f}m {seconds % 60:.0f}s"
    return f" {seconds // 3600:.0f}h {(seconds % 3600) // 60:.0f}m"

