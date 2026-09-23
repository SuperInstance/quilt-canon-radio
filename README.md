# quilt-canon-radio

**Continuous TTS broadcast of Quilt canon lore via ElevenLabs.**

## Quick start

```bash
pip install -e .

# Set your ElevenLabs API key
export ELEVENLABS_TOKEN=...

# Generate MP3s for canon lore (quota-aware)
quilt-canon-radio generate --voice 21m00Tcm4TlvDq8ikWAM

# Show playlist
quilt-canon-radio playlist

# Serve the HTML5 player
quilt-canon-radio serve --port 8765
# Open http://localhost:8765/player/
```

## How it works

1. **Read** canon lore from `canon_writings/*.md`
2. **Speak** each piece via `quilt-tts` (ElevenLabs `eleven_turbo_v2_5`)
3. **Save** MP3s to `~/.cache/quilt-canon-radio/mp3/`
4. **Build** `playlist.json` with metadata
5. **Serve** via a tiny Python HTTP server with HTML5 player

The HTML player auto-plays canon in order. Click "next" to skip, click queue items to jump. Gradient progress bar; mobile-friendly.

## Quota handling

ElevenLabs free tier has limits. `generate`:
- Catches quota errors gracefully
- Stops early when quota hits
- Skips failed tracks in the playlist

## Fleet integration

- **`quilt-tts`** — uses `quilt-tts.core.speak_lore` directly
- **`quilt-multi-oracle`** — multi-model chord (referenced for canon verification)
- **`quilt-canon-mcp`** — exposes canon as MCP tools (sibling)
- **`quilt-canon-search`** — TF-IDF search (sibling)
- **`quilt-canon-graph`** — knowledge graph (sibling)
- **`quilt-iterator`** — referenced for canon refinement

## The 5 bedrock doctrines

1. `cells_are_scars` — every cell records an attempted entry
2. `witness_log_is_prediction` — the log IS the prediction
3. `canon_gate_is_chord` — canon passes when multiple agents agree
4. `oracle_is_heard` — JEV probes canon with multi-model consensus
5. `substrate_quantum` — the substrate is the walker; canon is substrate-aware

## Polyformalism canary

```bash
python -m quilt_canon_radio.canary
# → 0x24a555471370b18d
```

## License

MIT
