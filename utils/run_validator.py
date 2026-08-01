
def run_validator():
    """Run pytest to ensure we didn't break player logic."""
    logger.info("Validator Agent: Running pytest...")
    res = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
    if res.returncode == 0:
        logger.info("Validator Agent: All tests passed! Logic is intact.")
        return True
    else:
        logger.error("Validator Agent: Tests failed after mutation! Reverting...")
        return False

