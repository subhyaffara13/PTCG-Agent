
def service_span_name(data: "ServiceSpanData") -> str:
    """``"{service} {call_type}"`` e.g. ``"redis set"`` — service name alone when
    no call type is known, so identically-named calls stay distinguishable."""
    return f"{data.service_name} {data.call_type or ''}".strip()

