
def basic_interactive_setup(
    autovisualize_arrays: bool = True,
    abbreviation_threshold: int | None = None,
):
  """Sets up IPython for interactive use with Treescope.

  This is a helper function that runs various setup steps:

    * Configures Treescope as the default IPython renderer.
    * Turns on interactive mode for Treescope's context managers.
    * Registers the `%%autovisualize` magic.
    * Registers the `%%with` magic.
    * If `autovisualize_arrays` is True, configures Treescope to automatically
      visualize arrays.
    * If `abbreviation_threshold` is not None, configures Treescope to
      abbreviate collapsed objects at the given depth.

  Args:
    autovisualize_arrays: Whether to automatically visualize arrays.
    abbreviation_threshold: If not None, configures Treescope to abbreviate
      collapsed objects at the given depth (recommended to set to 1 or 2).
  """
  register_as_default()
  register_autovisualize_magic()
  register_context_manager_magic()

  if autovisualize_arrays:
    autovisualize_lib.active_autovisualizer.set_globally(
        array_autovisualizer.ArrayAutovisualizer()
    )

  if abbreviation_threshold is not None:
    abbreviation_lib.abbreviation_threshold.set_globally(abbreviation_threshold)

