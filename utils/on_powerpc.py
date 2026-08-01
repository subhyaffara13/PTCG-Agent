
def on_powerpc():
    """ True if we are running on a Power PC platform."""
    return platform.processor() == 'powerpc' or \
           platform.machine().startswith('ppc')

