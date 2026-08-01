
def parse_semconv_opt_in(raw: Optional[str]) -> Set[OTELSemconvCategory]:
    """Parse the comma-separated OTEL_SEMCONV_STABILITY_OPT_IN value into the
    set of recognized categories. Unknown tokens are ignored per the spec."""
    if not raw:
        return set()
    return {
        _SEMCONV_CATEGORY_BY_VALUE[token]
        for token in (part.strip() for part in raw.split(","))
        if token in _SEMCONV_CATEGORY_BY_VALUE
    }

