
def set_cache_dir(path) -> None:
  """Sets the persistent compilation cache directory.

  After calling this, jit-compiled functions are saved to `path`, so they
  do not need be recompiled if the process is restarted or otherwise run again.
  This also tells Jax where to look for compiled functions before compiling.

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

