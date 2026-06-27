import http.server
import socketserver
import json
import logging
import os

PORT = 9872
logger = logging.getLogger("status_server")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Status - %(message)s')

class StatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>Cluster Status</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
                    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                </style>
            </head>
            <body>
            <div class="card">
                <h1>Distributed Training Cluster Status</h1>
                <pre id="status">Loading...</pre>
            </div>
            <script>
                async function fetchStatus() {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.text();
                        document.getElementById('status').innerText = data;
                    } catch (e) {
                        document.getElementById('status').innerText = 'Error fetching status';
                    }
                }
                setInterval(fetchStatus, 2000);
                fetchStatus();
            </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            status_data = {"status": "running"}
            if os.path.exists("logs/iteration_result.json"):
                try:
                    with open("logs/iteration_result.json", "r") as f:
                        status_data["latest_iteration"] = json.load(f)
                except:
                    status_data["error"] = "Could not parse iteration_result.json"
            else:
                status_data["info"] = "No iteration_result.json found yet."
                
            self.wfile.write(json.dumps(status_data, indent=2).encode('utf-8'))
        else:
            self.send_error(404)

def start_status_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), StatusHandler) as httpd:
        logger.info(f"Serving HTTP status dashboard on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    start_status_server()
