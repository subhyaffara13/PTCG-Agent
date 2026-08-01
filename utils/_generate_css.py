
def _generate_css(attrib):
    return "; ".join(f"{k}: {v}" for k, v in attrib.items())

