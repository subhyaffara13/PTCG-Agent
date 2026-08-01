
def install_threadsafe_warning_handlers():
  # Hook the showwarning method. The warnings module explicitly notes that
  # this is a function that users may replace.
  warnings.showwarning = _showwarning

  # Set the warnings module to always display warnings. We hook into it by
  # overriding the "showwarning" method, so it's important that all warnings
  # are "shown" by the usual mechanism.
  warnings.simplefilter("always")

