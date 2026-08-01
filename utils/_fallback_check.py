
def _fallback_check():
    import IPython.core.interactiveshell as ipsh
    import matplotlib.pyplot
    ipsh.InteractiveShell.instance()
    matplotlib.pyplot.figure()

