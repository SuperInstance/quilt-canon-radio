"""Generate MP3s for canon lore using quilt-tts (ElevenLabs)."""
import json
import sys
from pathlib import Path
from typing import Dict, List

# Add quilt-tts to path
sys.path.insert(0, "/workspace/repos/quilt-tts")

from quilt_tts.core import speak_lore

from .loader import load_canon


def _slug(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name)


def generate_all(canon_dir=None, output_dir: Path = None, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> List[Dict]:
    """Generate MP3 for every canon piece. Returns list of results."""
    if output_dir is None:
        output_dir = Path.home() / ".cache" / "quilt-canon-radio" / "mp3"
    output_dir.mkdir(parents=True, exist_ok=True)

    pieces = load_canon(canon_dir)
    results = []
    for p in pieces:
        out_path = output_dir / f"{_slug(p.name)}.mp3"
        text = p.title + ". " + (p.body[:4500] if p.body else "")
        result = speak_lore(text, voice_id=voice_id, output_path=str(out_path))
        result["name"] = p.name
        result["title"] = p.title
        result["path"] = str(out_path)
        results.append(result)
        # Quota check: if we hit quota, stop early
        if isinstance(result, dict) and "_error" in result:
            print(f"  ⚠ {p.name}: {result['_error'][:100]}")
            if "quota" in result.get("_error", "").lower() or "401" in result.get("_error", "") or "429" in result.get("_error", ""):
                print("  ✋ Quota hit — stopping generation early")
                break
    return results
