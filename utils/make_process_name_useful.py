
def make_process_name_useful():
  """Sets the process name to something better than 'python' if possible."""
  set_kernel_process_name(os.path.basename(sys.argv[0]))

