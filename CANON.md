# Canon — quilt-canon-radio

## What this tool is

A TTS broadcast of Quilt canon lore. Reads each canon piece, calls ElevenLabs to generate an MP3, builds a playlist, serves it via a tiny HTTP server with an HTML5 player.

## How it proves itself

**It runs.** `pip install -e .` then `quilt-canon-radio generate` produces MP3s (or graceful errors if quota hit). Tested with 5 tests in `run_tests.py`.

**It polyformalisms.** The canary hash `0x24a555471370b18d` matches across the fleet's 5 ports.

**It measures.** Each MP3 has a `lore_chars` and `size_bytes` in the playlist. Bytes-per-char ratio measures synthesis quality.

## Doctrines it instantiates

- **cells_are_scars** — every cell gets voice; every scar is heard
- **oracle_is_heard** — the canon speaks; the voice IS the oracle
- **substrate_quantum** — adds the audio substrate; canon propagates through air

## Commands

1. `generate [--voice VOICE_ID]` — generate MP3s (quota-aware)
2. `playlist [--limit N]` — show the playlist
3. `serve [--port PORT]` — serve the HTML5 player

## Fleet usage

- **`quilt-tts`** — uses `quilt-tts.core.speak_lore` directly
- **`quilt-multi-oracle`** — multi-model chord (referenced for verification)
- **`quilt-canon-mcp`** — sibling, exposes canon as MCP tools
- **`quilt-canon-search`** — sibling, TF-IDF search
- **`quilt-canon-graph`** — sibling, knowledge graph
- **`quilt-iterator`** — referenced for canon refinement
