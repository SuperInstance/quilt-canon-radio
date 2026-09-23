"""Test runner for quilt-canon-radio (no pytest dep)."""
import sys

sys.path.insert(0, "/workspace/repos/quilt-canon-radio")
sys.path.insert(0, "/workspace/repos/quilt-tts")

import json
from quilt_canon_radio.canary import canary
from quilt_canon_radio.player import build_playlist, save_playlist, load_playlist
from quilt_canon_radio.loader import load_canon
from quilt_canon_radio.generator import generate_all

results = []
failures = []


def test(name, func):
    try:
        func()
        results.append((name, "PASS"))
    except AssertionError as e:
        results.append((name, f"FAIL: {e}"))
        failures.append(name)
    except Exception as e:
        results.append((name, f"ERROR: {type(e).__name__}: {e}"))
        failures.append(name)


def t_canary():
    assert canary() == "0x24a555471370b18d"


def t_load_canon():
    pieces = load_canon()
    assert len(pieces) > 0


def t_build_playlist():
    fake = [
        {"name": "x", "title": "X", "path": "/tmp/x.mp3", "size_bytes": 1024, "lore_chars": 200, "voice_id": "abc"},
        {"name": "y", "title": "Y", "path": "/tmp/y.mp3", "_error": "quota"},
    ]
    pl = build_playlist(fake)
    assert pl["n_tracks"] == 1  # skips errors
    assert pl["items"][0]["name"] == "x"


def t_save_load_playlist(tmp):
    pl = {"version": "1", "n_tracks": 0, "items": []}
    save_playlist(pl, tmp / "pl.json")
    loaded = load_playlist(tmp / "pl.json")
    assert loaded == pl


def t_generate_graceful(tmp):
    """generate_all should handle missing ELEVENLABS_TOKEN gracefully."""
    import os
    saved = os.environ.pop("ELEVENLABS_TOKEN", None)
    try:
        results = generate_all(output_dir=tmp / "mp3", voice_id="21m00Tcm4TlvDq8ikWAM")
        # Without token, all should fail with _error but shouldn't crash
        for r in results:
            assert "_error" in r or "size_bytes" in r
    finally:
        if saved:
            os.environ["ELEVENLABS_TOKEN"] = saved


import tempfile
with tempfile.TemporaryDirectory() as td:
    tmp = __import__("pathlib").Path(td)

    test("test_canary", t_canary)
    test("test_load_canon", t_load_canon)
    test("test_build_playlist", t_build_playlist)
    test("test_save_load_playlist", lambda: t_save_load_playlist(tmp))
    test("test_generate_graceful", lambda: t_generate_graceful(tmp))

print("\n=== quilt-canon-radio test results ===")
for name, status in results:
    print(f"  {status:60} {name}")

print(f"\n{len(results) - len(failures)}/{len(results)} passed")
if failures:
    sys.exit(1)
