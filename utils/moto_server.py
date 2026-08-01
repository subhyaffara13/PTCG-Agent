
def moto_server(aws_credentials):
    # use service container for Linux on GitHub Actions
    if is_ci_environment() and not (
        is_platform_mac() or is_platform_arm() or is_platform_windows()
    ):
        yield "http://localhost:5000"
    else:
        moto_server = pytest.importorskip("moto.server")
        server = moto_server.ThreadedMotoServer(port=0)
        server.start()
        host, port = server.get_host_and_port()
        yield f"http://{host}:{port}"
        server.stop()

