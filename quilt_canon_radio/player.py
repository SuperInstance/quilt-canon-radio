"""Build a playlist JSON from generated MP3 results."""
import json
from pathlib import Path
from typing import Dict, List


def build_playlist(generation_results: List[Dict]) -> Dict:
    """Build a playlist JSON. Skips failed generations gracefully."""
    items = []
    for r in generation_results:
        if isinstance(r, dict) and "_error" in r:
            continue  # skip failed
        items.append({
            "name": r.get("name", "unknown"),
            "title": r.get("title", ""),
            "path": r.get("path", ""),
            "size_bytes": r.get("size_bytes", 0),
            "lore_chars": r.get("lore_chars", 0),
            "voice_id": r.get("voice_id", ""),
        })
    return {
        "version": "1",
        "n_tracks": len(items),
        "items": items,
    }


def save_playlist(playlist: Dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(playlist, indent=1))


def load_playlist(path: Path) -> Dict:
    return json.loads(path.read_text())
