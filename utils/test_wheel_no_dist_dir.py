import os

def test_wheel_no_dist_dir():
    project_name = 'nodistinfo'
    version = '1.0'
    wheel_name = f'{project_name}-{version}-py2.py3-none-any.whl'
    with tempdir() as source_dir:
        wheel_path = os.path.join(source_dir, wheel_name)
        # create an empty zip file
        zipfile.ZipFile(wheel_path, 'w').close()
        with tempdir() as install_dir:
            with pytest.raises(ValueError):
                _check_wheel_install(
                    wheel_path, install_dir, None, project_name, version, None
                )

