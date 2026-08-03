import logging
import os

def _get_debugger_module_with_function(function_name):
  """Provides the `$PYTHONBREAKPOINT` module if it contains `function_name`.

  Falls back to `pdb` otherwise.

  Args:
    function_name: The name of the function required.

  Returns:
    A debugger module providing `function_name`.
  """
  python_breakpoint = os.getenv('PYTHONBREAKPOINT')
  # The special value '0' for `$PYTHONBREAKPOINT` means "do not use a debugger".
  # We don't respect it (if the user explicitly asks to debug) but shouldn't try
  # to import a module with this name.
  if python_breakpoint and python_breakpoint != '0':
    debugger_module_import = python_breakpoint.rsplit('.', 1)[0]
    try:
      debugger_module = importlib.import_module(debugger_module_import)
    except ImportError:
      logging.warning(
          (
              'Could not import $PYTHONBREAKPOINT debugger module %r, '
              'falling back to PDB'
          ),
          debugger_module_import,
      )
    else:
      if hasattr(debugger_module, function_name):
        return debugger_module
      logging.warning(
          '$PYTHONBREAKPOINT debugger %r has no function %r, '
          'falling back to PDB',
          debugger_module_import,
          function_name,
      )
  return pdb

