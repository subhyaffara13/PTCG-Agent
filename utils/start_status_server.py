
def start_status_server():
    import socketserver
    from distributed.status_server import PORT, StatusHandler, logger
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), StatusHandler) as httpd:
        logger.info(f"Serving HTTP status dashboard on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

