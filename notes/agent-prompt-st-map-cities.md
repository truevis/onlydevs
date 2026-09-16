# Agent prompt: Onlydevs world map of radar cities (`st.map`)

Copy everything below the line into a Cursor agent (Composer / Auto). **Do not implement yet unless the user explicitly asks** — this file is the brief only.

---

## Goal

Add a **world map** to the Onlydevs Streamlit app that visualizes the same cities shown in the main City Radar spider chart in `app.py`, using Streamlit's built-in [`st.map`](https://docs.streamlit.io/develop/api-reference/charts/st.map).

Do **not** replace the radar chart. The map is an additional view that stays in sync with the city multiselect.

## Docs to follow

Primary API: https://docs.streamlit.io/develop/api-reference/charts/st.map

Key facts from the docs:

- `st.map` is a thin wrapper around `st.pydeck_chart` for a **scatterplot on a map** with auto-center / auto-zoom.
- Data must be anything `st.dataframe` accepts (prefer a `pandas.DataFrame`).
- Latitude / longitude columns default to names like `lat` / `latitude` and `lon` / `longitude`, or pass `latitude=` / `longitude=` explicitly.
- Optional: `color` (hex / RGBA / column), `size` (meters, or column), `zoom`, `width="stretch"`, `height` (default 500).
- Map tiles come from **Carto** by default; Mapbox/Carto API keys are only needed for advanced PyDeck usage — plain `st.map` should work without keys.
- Prefer `width="stretch"` over deprecated `use_container_width`.

## Cities already in `app.py` (`CITIES` dict)

Keep this list as the source of truth (names + hex colors already in the app):

| City | Approx. coordinates (use these unless you have better) | Existing color |
|------|----------------------------------------------------------|----------------|
| Bangkok | 13.7563, 100.5018 | `#00B4D8` |
| Austin | 30.2672, -97.7431 | `#F77F00` |
| Berlin | 52.5200, 13.4050 | `#E63946` |
| Da Nang | 16.0544, 108.2022 | `#FF6B35` |
| Lagos | 6.5244, 3.3792 | `#F4A261` |
| Singapore | 1.3521, 103.8198 | `#2A9D8F` |
| Toronto | 43.6532, -79.3832 | `#6A994E` |

Add a small structured mapping in code (e.g. `CITY_COORDS: dict[str, tuple[float, float]]`) next to `CITIES`, or embed `lat`/`lon` into each city dict — pick one approach and keep it DRY with the radar data.

## UX / layout requirements

1. Place the map **below the radar chart** and **above** the "Tonight at Only Devs Bangkok" promo section (or clearly separated with `st.divider()` / a bordered container).
2. Title something like **"Meetup circuit on the map"** with a one-line caption explaining pins = selected cities.
3. **Only plot cities currently selected** in the existing multiselect (`selected`). If none selected, show `st.info` and skip the map.
4. Pin **color** should match each city's radar color from `CITIES[name]["color"]`.
5. Pin **size** may encode vibe score (mean of the five radar values), scaled to a sensible meter range for world zoom (e.g. base size ~ 80_000–200_000 m so markers stay visible globally — tune so Bangkok and Toronto are both readable).
6. Let Streamlit auto-center / auto-zoom when possible; if the global spread looks too zoomed-out or too tight, set an explicit `zoom` (see OSM zoom levels) after a quick visual check.
7. Do not require Mapbox/Carto API keys for the default path.
8. Add `pandas` to `requirements.txt` if it is not already a direct dependency.

## Suggested implementation sketch

```python
import pandas as pd

# CITY_COORDS = {"Bangkok": (13.7563, 100.5018), ...}

if selected:
    rows = []
    for name in selected:
        lat, lon = CITY_COORDS[name]
        city = CITIES[name]
        vibe = sum(city["values"]) / len(city["values"])
        rows.append(
            {
                "city": name,
                "lat": lat,
                "lon": lon,
                "color": city["color"],
                "size": 50_000 + vibe * 2_000,  # tune
            }
        )
    map_df = pd.DataFrame(rows)
    st.subheader("Meetup circuit on the map")
    st.caption("Pins follow the cities selected above; size hints vibe score.")
    st.map(map_df, latitude="lat", longitude="lon", color="color", size="size", height=420, width="stretch")
```

Refine naming, copy, and sizing to match the app's existing tone.

## Out of scope (unless the user expands the ask)

- Replacing `st.map` with a custom full PyDeck layer stack
- Clustering, routes, or animation
- Editing talk promo images or radar scoring research in `notes/city-radar-research.md`
- Changing Streamlit Cloud secrets / adding Mapbox keys

## Acceptance criteria

- [ ] Selecting / deselecting cities updates the map markers.
- [ ] Marker colors match radar series colors.
- [ ] All seven cities can appear when selected; Da Nang is included.
- [ ] No new paid map API key required for the default `st.map` path.
- [ ] Radar chart and Bangkok meetup promo section still work unchanged in spirit.
- [ ] `requirements.txt` lists any new direct dependency (`pandas` if needed).
- [ ] Brief note in the PR/commit body pointing at this prompt file.

## Deliverable

Implement in `app.py` (+ `requirements.txt` if needed), run a quick local sanity check if possible, commit, and push to `main` **only when the user asks to implement**.
