"""
run_tests.py
Programmatic wrapper to execute pytest within the correct path context.
"""
import sys
import pytest

if __name__ == "__main__":
    sys.path.insert(0, ".")
    print("Running all pytest suites in tests/...")
    exit_code = pytest.main(["tests", "-v"])
    print(f"Test run completed with exit code: {exit_code}")
    sys.exit(exit_code)
