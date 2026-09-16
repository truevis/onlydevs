"""Onlydevs meetup radar — Streamlit + streamlit-echarts spider chart demo."""

from __future__ import annotations

import streamlit as st
from streamlit_echarts import st_echarts

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

# Fictional but opinionated city profiles for the Onlydevs meetup circuit.
CITIES: dict[str, dict] = {
    "Bangkok": {
        "color": "#00B4D8",
        "values": [78, 92, 88, 70, 85],
        "blurb": "Street food fuel, midnight PRs, sticky humidity, sticky conversations.",
    },
    "Austin": {
        "color": "#F77F00",
        "values": [90, 75, 82, 88, 91],
        "blurb": "BBQ, live demos, and someone always shipping from a food-truck patio.",
    },
    "Berlin": {
        "color": "#E63946",
        "values": [85, 88, 95, 80, 72],
        "blurb": "Club-to-code pipelines. The after-meetup is the meetup.",
    },
    "Lagos": {
        "color": "#F4A261",
        "values": [88, 70, 90, 55, 94],
        "blurb": "High-voltage hustle. Bandwidth optional, ambition required.",
    },
    "Singapore": {
        "color": "#2A9D8F",
        "values": [82, 68, 60, 98, 80],
        "blurb": "Precision venues, flawless Wi‑Fi, talks that start on the minute.",
    },
    "Toronto": {
        "color": "#6A994E",
        "values": [75, 80, 70, 86, 78],
        "blurb": "Polite pull requests and maple-syrup standups in February.",
    },
}

st.title("Onlydevs City Radar")
st.caption(
    "A creative spider chart built with "
    "[streamlit-echarts](https://github.com/andfanilo/streamlit-echarts) — "
    "market-profile vibes, meetup energy instead of revenue."
)

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("Pick the circuit")
    selected = st.multiselect(
        "Cities to overlay",
        options=list(CITIES.keys()),
        default=["Bangkok", "Austin", "Berlin", "Singapore"],
        help="Toggle cities like legend chips on a market-profiles radar.",
    )
    fill = st.slider("Fill opacity", 0.05, 0.45, 0.18, 0.01)
    show_symbols = st.toggle("Show vertices", value=True)
    st.divider()
    if selected:
        st.markdown("**Spotlight**")
        for name in selected:
            city = CITIES[name]
            score = sum(city["values"]) / len(city["values"])
            st.markdown(
                f"<span style='color:{city['color']};font-weight:700'>{name}</span> "
                f"· vibe score **{score:.0f}**/100",
                unsafe_allow_html=True,
            )
            st.caption(city["blurb"])
    else:
        st.info("Select at least one city to draw the spider.")

with right:
    if not selected:
        st.empty()
    else:
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
                        "opacity": fill,
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
                "bottom": 0,
                "data": selected,
                "icon": "roundRect",
            },
            "radar": {
                "center": ["50%", "48%"],
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

st.divider()
st.markdown(
    "Run locally: `pip install -r requirements.txt && streamlit run app.py`  \n"
    "Chart library: [andfanilo/streamlit-echarts](https://github.com/andfanilo/streamlit-echarts)"
)
