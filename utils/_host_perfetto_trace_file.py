
def _host_perfetto_trace_file(path: os.PathLike | str):
  # ui.perfetto.dev looks for files hosted on `127.0.0.1:9001`. We set up a
  # TCP server that is hosting the `perfetto_trace.json.gz` file.
  port = 9001
  orig_directory = pathlib.Path.cwd()
  directory, filename = os.path.split(path)
  try:
    os.chdir(directory)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', port), _PerfettoServer) as httpd:
      url = f"https://ui.perfetto.dev/#!/?url=http://127.0.0.1:{port}/{filename}"
      print(f"Open URL in browser: {url}")

      # Once ui.perfetto.dev acquires trace.json from this server we can close
      # it down.
      while httpd.__dict__.get('last_request') != '/' + filename:
        httpd.handle_request()
  finally:
    os.chdir(orig_directory)

