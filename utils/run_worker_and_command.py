import os
import subprocess
import sys

def run_worker_and_command(command):
  """Worker Mode: Initializes JAX explicitly, then executes the target command."""

  coordinator_address = os.environ.get("JAX_COORDINATOR_ADDRESS")
  num_processes = os.environ.get("JAX_NUM_PROCESSES")
  process_id = os.environ.get("JAX_PROCESS_ID")

  if coordinator_address is None:
    raise ValueError(
        "Environment variables for JAX distributed not found. "
        "Did you use launch_multihost.py?"
    )

  # Explicit Initialization
  jax.distributed.initialize(
      coordinator_address=coordinator_address,
      num_processes=int(num_processes),
      process_id=int(process_id),
  )

  print(f"[Rank {process_id}] JAX Initialized. Executing: {' '.join(command)}")
  print(f"[Rank {process_id}] JAX devices: {jax.devices()}")

  # Clean up 'python' from the command if the user accidentally included it
  if command[0] == "python" or command[0] == "python3":
    command = command[1:]

  cmd_name = command[0]

  # Execute the requested script/tool inside this initialized process
  if cmd_name == "pytest":
    sys.exit(pytest.main(command[1:]))

  elif cmd_name.endswith(".py"):
    # Overwrite sys.argv so the target script sees its expected arguments
    sys.argv = command
    runpy.run_path(cmd_name, run_name="__main__")

  else:
    # Fallback for arbitrary shell commands
    sys.exit(subprocess.call(command))

