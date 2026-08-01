
def test_backend_getattr(module_name):
    proc = subprocess_run_helper(_test_module_getattr, module_name,
                                 timeout=120 if is_ci_environment() else 20)
    if 'SKIP: ' in proc.stdout:
        pytest.skip(proc.stdout.removeprefix('SKIP: '))
    print(proc.stdout)

