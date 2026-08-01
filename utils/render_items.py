
def render_items(eps):
    return '\n'.join(f'{ep.name} = {ep.value}' for ep in sorted(eps))

