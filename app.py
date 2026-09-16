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

# Research-informed, playfully scored city profiles for the Onlydevs meetup circuit.
# Axes: Lightning talks · Coffee strength · Late-night hacking · Wi‑Fi · Networking
CITIES: dict[str, dict] = {
    "Bangkok": {
        "color": "#00B4D8",
        "values": [90, 93, 86, 78, 88],
        "blurb": (
            "Only Devs still ends with open-mic five-minuters; BKK/hack keeps "
            "Thong Lo keyboards warm. Ari espresso hits hard—cafe Wi‑Fi is "
            "good until it isn't, so Hive fiber is the grown-up backup."
        ),
    },
    "Austin": {
        "color": "#F77F00",
        "values": [88, 78, 84, 92, 95],
        "blurb": (
            "SXSW lightning pitches and Capital Factory / Station nights until "
            "1am. Code & Coffee mornings, cold brew on tap, and a networking "
            "density that feels like BBQ line density."
        ),
    },
    "Berlin": {
        "color": "#E63946",
        "values": [93, 86, 96, 72, 78],
        "blurb": (
            "Hack and Tell's five-minute show-and-roast at c-base is sacred. "
            "OpenHack and Build Fridays run deep into the night; cafe Wi‑Fi "
            "still ghosts you between Altbau courtyards."
        ),
    },
    "Da Nang": {
        "color": "#FF6B35",
        "values": [70, 95, 72, 86, 74],
        "blurb": (
            "Cà phê sữa đá that could restart a laptop. Frontier Club, AI "
            "Tinkerers, and Monday Vibe & Coffee keep An Thuong shipping— "
            "intimate density, beach air, fiber that punches above the skyline."
        ),
    },
    "Lagos": {
        "color": "#F4A261",
        "values": [86, 65, 92, 48, 96],
        "blurb": (
            "GDG Lagos, DevFest, and 24-hour buildathons don't do half-speed. "
            "Yaba hubs sell fiber + generators as a lifestyle; outside them, "
            "bandwidth is a side quest and ambition is the ISP."
        ),
    },
    "Singapore": {
        "color": "#2A9D8F",
        "values": [84, 80, 58, 99, 82],
        "blurb": (
            "SingaDev lightning, AI Tinkerers demos, Hackapura daytime shipping. "
            "Kopi-o and third-wave both win; fiber is basically a utility. "
            "Late-night hacking lives in HackerspaceSG and the rare all-nighter."
        ),
    },
    "Toronto": {
        "color": "#6A994E",
        "values": [72, 88, 68, 88, 80],
        "blurb": (
            "Coffee & Code and Creeds cowork tables, TorontoJS TechTalks, "
            "Double Down build nights. Third-wave fuel is elite; true late-night "
            "laptop havens are rarer than a mild February."
        ),
    },
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

st.caption(
    "Chart library: [andfanilo/streamlit-echarts](https://github.com/andfanilo/streamlit-echarts)"
)
