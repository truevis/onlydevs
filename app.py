"""Onlydevs meetup radar — Streamlit + streamlit-echarts spider chart demo."""

from __future__ import annotations

import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_echarts import st_echarts


def _hex_to_rgba(hex_color: str, alpha: int = 200) -> list[int]:
    """Convert #RRGGBB to an RGBA list for pydeck layers."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return [r, g, b, alpha]

st.set_page_config(
    page_title="Onlydevs · City Radar",
    page_icon="🕸️",
    layout="wide",
)

# Axes inspired by classic market-profile radars, remixed for meetup energy.
INDICATORS = [
    {"name": "Lightning talks", "max": 100},
    {"name": "Coffee strength", "max": 100},
    {"name": "Late-night hacking", "max": 100},
    {"name": "Wi‑Fi reliability", "max": 100},
    {"name": "Networking density", "max": 100},
]

# Research-informed, playfully scored city profiles for the Onlydevs meetup circuit.
# Axes: Lightning talks · Coffee strength · Late-night hacking · Wi‑Fi · Networking
CITIES: dict[str, dict] = {
    "Bangkok": {
        "color": "#00B4D8",
        "values": [92, 90, 84, 82, 88],
        "blurb": (
            "Only Devs still ends with capped five-minute lightnings; BKK/hack "
            "keeps Thong Lo keyboards warm. Ari espresso hits hard—cafe Wi‑Fi "
            "is good until it isn't, so Hive fiber is the grown-up backup."
        ),
    },
    "Austin": {
        "color": "#F77F00",
        "values": [86, 80, 82, 94, 96],
        "blurb": (
            "SXSW pitches and Capital Factory mini-hacks stack the calendar. "
            "Code & Coffee mornings, cold brew on tap, and a networking density "
            "that feels like BBQ line density."
        ),
    },
    "Berlin": {
        "color": "#E63946",
        "values": [96, 88, 97, 70, 80],
        "blurb": (
            "Hack and Tell's five-minute show-and-roast at c-base is sacred. "
            "Hackerspace nights run deep; cafe Wi‑Fi still ghosts you between "
            "Altbau courtyards."
        ),
    },
    "Da Nang": {
        "color": "#FF6B35",
        "values": [72, 97, 78, 88, 76],
        "blurb": (
            "Cà phê sữa đá that could restart a laptop. Frontier Club and AI "
            "Tinkerers keep An Thuong shipping—intimate density, beach air, "
            "and fiber that punches above the skyline."
        ),
    },
    "Lagos": {
        "color": "#F4A261",
        "values": [88, 62, 94, 52, 97],
        "blurb": (
            "GDG Lagos, DevFest, and hub buildathons don't do half-speed. "
            "Yaba sells fiber + generators as a lifestyle; outside them, "
            "bandwidth is a side quest and ambition is the ISP."
        ),
    },
    "Singapore": {
        "color": "#2A9D8F",
        "values": [86, 82, 55, 99, 84],
        "blurb": (
            "AI Tinkerers demos and Hackware show-and-tells; Hackapura ships "
            "by day. Kopi-o and third-wave both win; fiber is basically a "
            "utility. Late nights live at HackerspaceSG."
        ),
    },
    "Toronto": {
        "color": "#6A994E",
        "values": [78, 92, 72, 90, 82],
        "blurb": (
            "Coffee & Code at Creeds, TorontoJS TechTalks, Double Down "
            "co-hacking. Third-wave fuel is elite; true overnight laptop "
            "havens are rarer than a mild February."
        ),
    },
}

# Approximate city centers for the meetup-circuit map (lat, lon).
CITY_COORDS: dict[str, tuple[float, float]] = {
    "Bangkok": (13.7563, 100.5018),
    "Austin": (30.2672, -97.7431),
    "Berlin": (52.5200, 13.4050),
    "Da Nang": (16.0544, 108.2022),
    "Lagos": (6.5244, 3.3792),
    "Singapore": (1.3521, 103.8198),
    "Toronto": (43.6532, -79.3832),
}

st.title("Onlydevs City Radar")
st.caption(
    "A creative spider chart built with "
    "[streamlit-echarts](https://github.com/andfanilo/streamlit-echarts) — "
    "market-profile vibes, meetup energy instead of revenue."
)

with st.container(border=True):
    st.subheader("Pick the circuit")
    selected = st.multiselect(
        "Cities to overlay",
        options=list(CITIES.keys()),
        default=["Bangkok", "Austin", "Berlin", "Da Nang", "Singapore"],
        help="Toggle cities like legend chips on a market-profiles radar.",
    )
    show_symbols = st.toggle("Show vertices", value=True)

if selected:
    with st.container(border=True):
        st.markdown("**Spotlight**")
        cols = st.columns(min(len(selected), 4))
        for i, name in enumerate(selected):
            city = CITIES[name]
            score = sum(city["values"]) / len(city["values"])
            with cols[i % len(cols)]:
                st.markdown(
                    f"<span style='color:{city['color']};font-weight:700'>{name}</span> "
                    f"· vibe score **{score:.0f}**/100",
                    unsafe_allow_html=True,
                )
                st.caption(city["blurb"])
else:
    st.info("Select at least one city to draw the spider.")

if selected:
    series_data = []
    for name in selected:
        city = CITIES[name]
        series_data.append(
            {
                "name": name,
                "value": city["values"],
                "symbol": "circle" if show_symbols else "none",
                "symbolSize": 8,
                "lineStyle": {"width": 2, "color": city["color"]},
                "itemStyle": {"color": city["color"]},
                "areaStyle": {
                    "color": city["color"],
                    "opacity": 0.18,
                },
            }
        )

    options = {
        "color": [CITIES[n]["color"] for n in selected],
        "tooltip": {
            "trigger": "item",
            "confine": True,
        },
        "legend": {
            "top": 0,
            "data": selected,
            "icon": "roundRect",
        },
        "radar": {
            "center": ["50%", "55%"],
            "radius": "62%",
            "indicator": INDICATORS,
            "splitNumber": 4,
            "axisName": {
                "color": "#334155",
                "fontSize": 13,
                "fontWeight": 600,
            },
            "splitLine": {"lineStyle": {"color": "#CBD5E1"}},
            "splitArea": {
                "show": True,
                "areaStyle": {
                    "color": ["#F8FAFC", "#F1F5F9", "#E2E8F0", "#F8FAFC"]
                },
            },
            "axisLine": {"lineStyle": {"color": "#94A3B8"}},
        },
        "series": [
            {
                "type": "radar",
                "emphasis": {"lineStyle": {"width": 3}},
                "data": series_data,
            }
        ],
    }

    st_echarts(options=options, height="560px", key="onlydevs_radar")

# --- Meetup circuit map (selected cities only) ---
st.divider()
st.subheader("Meetup circuit on the map")
st.caption("Click a pin to inspect that city's vibe stats.")
if selected:
    map_rows = []
    for name in selected:
        lat, lon = CITY_COORDS[name]
        city = CITIES[name]
        values = city["values"]
        vibe = sum(values) / len(values)
        map_rows.append(
            {
                "city": name,
                "lat": lat,
                "lon": lon,
                "color": _hex_to_rgba(city["color"]),
                "size": 50_000 + vibe * 2_000,
                "vibe": round(vibe),
                "lightning": values[0],
                "coffee": values[1],
                "hacking": values[2],
                "wifi": values[3],
                "networking": values[4],
                "blurb": city["blurb"],
            }
        )
    map_df = pd.DataFrame(map_rows)

    event = st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=float(map_df["lat"].mean()),
                longitude=float(map_df["lon"].mean()),
                zoom=1.2,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=map_df,
                    id="meetup-cities",
                    get_position="[lon, lat]",
                    get_fill_color="color",
                    get_radius="size",
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            tooltip={
                "html": (
                    "<b>{city}</b><br/>"
                    "Vibe: {vibe}/100<br/>"
                    "Lightning: {lightning} · Coffee: {coffee}<br/>"
                    "Hacking: {hacking} · Wi‑Fi: {wifi}<br/>"
                    "Networking: {networking}"
                ),
                "style": {"backgroundColor": "#0f172a", "color": "white"},
            },
        ),
        height=420,
        width="stretch",
        on_select="rerun",
        selection_mode="single-object",
        key="meetup_circuit_map",
    )

    selected_objects = event.selection.get("objects", {}).get("meetup-cities", [])
    if selected_objects:
        picked = selected_objects[0]
        city_name = picked["city"]
        city = CITIES[city_name]
        score = sum(city["values"]) / len(city["values"])
        axis_names = [ind["name"] for ind in INDICATORS]
        stats = " · ".join(
            f"{axis}: **{value}**"
            for axis, value in zip(axis_names, city["values"], strict=True)
        )
        with st.container(border=True):
            st.markdown(
                f"<span style='color:{city['color']};font-weight:700;font-size:1.15rem'>"
                f"{city_name}</span> · vibe score **{score:.0f}**/100",
                unsafe_allow_html=True,
            )
            st.markdown(stats)
            st.caption(city["blurb"])
    else:
        st.caption("Select a city pin on the map to see its full stats.")
else:
    st.info("Select at least one city to place pins on the map.")

st.caption(
    "Chart library: [andfanilo/streamlit-echarts](https://github.com/andfanilo/streamlit-echarts)"
)
