
def render_label(label, inits={}):
    """Slightly more flexible way to render labels.

    >>> from sympy.physics.quantum.circuitplot import render_label
    >>> render_label('q0')
    '$\\\\left|q0\\\\right\\\\rangle$'
    >>> render_label('q0', {'q0':'0'})
    '$\\\\left|q0\\\\right\\\\rangle=\\\\left|0\\\\right\\\\rangle$'
    """
    init = inits.get(label)
    if init:
        return r'$\left|%s\right\rangle=\left|%s\right\rangle$' % (label, init)
    return r'$\left|%s\right\rangle$' % label

