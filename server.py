"""Dependency-free local development server."""
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
os.chdir(Path(__file__).parent)
class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', '3000'))
    print(f'Campaign Arena listening on port {port}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
