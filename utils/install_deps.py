import logging
import subprocess
import sys

def install_deps():
  """Installs required dependencies if not present."""
  deps_map = {'pytest': 'pytest', 'chex': 'chex', 'pyyaml': 'yaml'}
  to_install = []
  for pip_name, import_name in deps_map.items():
    try:
      __import__(import_name)
    except ImportError:
      to_install.append(pip_name)

  if to_install:
    logging.info('Installing dependencies: %s', ', '.join(to_install))
    try:
      subprocess.check_call(
          [sys.executable, '-m', 'pip', 'install'] + to_install
      )
    except subprocess.CalledProcessError as e:
      logging.error('Failed to install dependencies: %s', e)
      sys.exit(1)

