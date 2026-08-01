
def _socket_listener_loop(self):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(128)
        server_socket.settimeout(1.0)
    except Exception as e:
        logger.error(f"InferenceServer socket bind failed on port {self.port}: {e}")
        return
    while self._running:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(target=self._handle_socket_client, args=(conn,), daemon=True).start()
        except socket.timeout:
            continue
        except Exception:
            break
    server_socket.close()

