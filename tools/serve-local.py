"""Run the storefront locally with the homepage at / (no dependencies)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class StorefrontHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/':
            self.path = '/Client/Public/Src/Pages/index.html'
        super().do_GET()

    def do_HEAD(self):
        if self.path.split('?')[0] == '/':
            self.path = '/Client/Public/Src/Pages/index.html'
        super().do_HEAD()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8000), partial(StorefrontHandler, directory=str(ROOT)))
    print('Dolce Vita: http://127.0.0.1:8000', flush=True)
    server.serve_forever()
