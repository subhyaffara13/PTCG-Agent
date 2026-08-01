
def _version_from_git_tree(base_version: str) -> str | None:
  try:
    root_directory = os.path.dirname(os.path.realpath(__file__))

    # Get date string from date of most recent git commit, and the abbreviated
    # hash of that commit.
    p = subprocess.Popen(["git", "show", "-s", "--format=%at-%h", "HEAD"],
                         cwd=root_directory,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = p.communicate()
    timestamp, commit_hash = stdout.decode().strip().split('-', 1)
    datestring = datetime.date.fromtimestamp(int(timestamp)).strftime("%Y%m%d")
    assert datestring.isnumeric()
    assert commit_hash.isalnum()
  except:
    return None
  else:
    version = f"{base_version}.dev{datestring}+{commit_hash}"
    suffix = os.environ.get("JAX_CUSTOM_VERSION_SUFFIX", None)
    if suffix:
      return version + "." + suffix
    return version


def _version_from_git_tree(base_version: str) -> str | None:
  try:
    root_directory = os.path.dirname(os.path.realpath(__file__))

    # Get date string from date of most recent git commit, and the abbreviated
    # hash of that commit.
    p = subprocess.Popen(["git", "show", "-s", "--format=%at-%h", "HEAD"],
                         cwd=root_directory,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = p.communicate()
    timestamp, commit_hash = stdout.decode().strip().split('-', 1)
    datestring = datetime.date.fromtimestamp(int(timestamp)).strftime("%Y%m%d")
    assert datestring.isnumeric()
    assert commit_hash.isalnum()
  except:
    return None
  else:
    version = f"{base_version}.dev{datestring}+{commit_hash}"
    suffix = os.environ.get("JAX_CUSTOM_VERSION_SUFFIX", None)
    if suffix:
      return version + "." + suffix
    return version

