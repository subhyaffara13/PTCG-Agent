import pathlib
import time

def _torch_profile(req: _Request, resp: _Response) -> None:
    experimental_config = _ExperimentalConfig(
        profile_all_threads=True,
    )
    duration = float(req.get_param("duration"))
    with profile(record_shapes=True, experimental_config=experimental_config) as prof:
        time.sleep(duration)

    with tempfile.NamedTemporaryFile(prefix="torch_debug", suffix=".json") as f:
        prof.export_chrome_trace(f.name)
        resp.set_content(pathlib.Path(f.name).read_bytes(), "application/json")
        resp.set_status(200)

