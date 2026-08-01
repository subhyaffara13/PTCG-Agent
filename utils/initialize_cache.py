
def initialize_cache(path) -> None:
  """This API is deprecated; use set_cache_dir instead.

  Set the path. To take effect, should be called prior to any calls to
  get_executable_and_time() and put_executable_and_time().

  For more information, see the :ref:`persistent compilation cache guide <persistent-compilation-cache>`.

  .. warning::
     The compilation cache is considered trusted. Do not share a compilation
     cache with users you do not trust. For example, if you put the compilation
     cache in a directory to which others may write, those users can trigger
     your JAX process to run arbitrary code. Sharing a compilation cache is
     equivalent to allowing anyone who can write to the cache directory to run
     code on your machine.
  """
  config.config.update("jax_compilation_cache_dir", path)

