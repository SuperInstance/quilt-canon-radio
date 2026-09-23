"""CLI for quilt-canon-radio."""
import argparse
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from .generator import generate_all
from .player import build_playlist, save_playlist, load_playlist


PLAYLIST_PATH = Path.home() / ".cache" / "quilt-canon-radio" / "playlist.json"


def cmd_generate(args):
    print(f"Generating MP3s for canon lore...")
    results = generate_all(voice_id=args.voice)
    n_ok = sum(1 for r in results if isinstance(r, dict) and "_error" not in r)
    n_fail = len(results) - n_ok
    print(f"✓ {n_ok} succeeded, {n_fail} failed (quota or API errors)")
    playlist = build_playlist(results)
    save_playlist(playlist, PLAYLIST_PATH)
    print(f"✓ Playlist saved → {PLAYLIST_PATH} ({playlist['n_tracks']} tracks)")


def cmd_playlist(args):
    if not PLAYLIST_PATH.exists():
        print("No playlist yet. Run: quilt-canon-radio generate")
        return
    pl = load_playlist(PLAYLIST_PATH)
    print(f"Playlist: {pl['n_tracks']} tracks")
    for i, t in enumerate(pl["items"][:args.limit]):
        print(f"  {i+1:3d}. {t['title']} → {t['path']}")


def cmd_serve(args):
    """Serve the player + MP3s on a local HTTP server."""
    pl_path = Path(args.playlist)
    if not pl_path.exists():
        print(f"No playlist at {pl_path}. Run: quilt-canon-radio generate")
        return
    pl = load_playlist(pl_path)
    n = len(pl["items"])
    print(f"Serving {n} tracks on http://localhost:{args.port}/")
    print(f"Player: http://localhost:{args.port}/player/")
    print(f"Playlist: http://localhost:{args.port}/playlist.json")

    # Set up directory routing: /player/ → player dir, /mp3/ → mp3 dir, / → root
    base = Path(__file__).parent.parent  # /workspace/repos/quilt-canon-radio
    mp3_dir = pl_path.parent / "mp3"

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(base), **kw)

        def do_GET(self):
            # Map /mp3/.mp3 to ~/.cache/.../mp3/.mp3
            if self.path.startswith("/mp3/"):
                fname = self.path[5:]
                mp3_path = mp3_dir / fname
                if mp3_path.exists():
                    self.send_response(200)
                    self.send_header("Content-Type", "audio/mpeg")
                    self.send_header("Content-Length", str(mp3_path.stat().st_size))
                    self.end_headers()
                    self.wfile.write(mp3_path.read_bytes())
                    return
                else:
                    self.send_error(404, "MP3 not found")
                    return
            return super().do_GET()

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        httpd.serve_forever()


def main():
    p = argparse.ArgumentParser(description="quilt-canon-radio — TTS broadcast of canon lore")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_g = sub.add_parser("generate", help="Generate MP3s for canon pieces")
    p_g.add_argument("--voice", default="21m00Tcm4TlvDq8ikWAM")
    p_g.set_defaults(func=cmd_generate)

    p_pl = sub.add_parser("playlist", help="Show the playlist")
    p_pl.add_argument("--limit", type=int, default=20)
    p_pl.set_defaults(func=cmd_playlist)

    p_s = sub.add_parser("serve", help="Serve the player + MP3s")
    p_s.add_argument("--playlist", default=str(PLAYLIST_PATH))
    p_s.add_argument("--port", type=int, default=8765)
    p_s.set_defaults(func=cmd_serve)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
