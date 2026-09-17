# Grok Bot features used today (Onlydevs lightning talk)

Short speaker notes for what this Grok Bot session actually did while building [onlydevs](https://github.com/truevis/onlydevs) / [onlydevs.streamlit.app](https://onlydevs.streamlit.app/).

## 1. Registered PC control (Alpha)

- Connected to the user’s Windows PC **Alpha** through local execution.
- Created `C:\GitHub\onlydevs`, initialized git, and pushed to **GitHub** (`truevis/onlydevs`) with `gh`.
- Installed Python deps and launched **Streamlit** locally for a first look.

## 2. Repo + coding loop

- Wrote the first **City Radar** Streamlit app (`app.py`) using **streamlit-echarts** spider charts.
- Iterated on UI (removed a non-working opacity control, widened city picker, bordered panels, top legend).
- Committed and pushed repeatedly so Streamlit Cloud could redeploy.

## 3. Box browser review (live app)

- Opened the hosted app in Grok Bot’s own browser.
- Captured screenshots of the live UI (radar, spotlight, footer) to spot issues like clipped city chips and a “run locally” footer.
- Those captures are the **v1** slides in this folder.

## 4. Research → data refresh

- When Cursor Cloud Agents were usage-blocked, fell back to **local Cursor Agent CLI on Alpha**.
- Researched meetup scenes for Bangkok, Austin, Berlin, Lagos, Singapore, Toronto, and **Da Nang**.
- Wrote findings to `notes/city-radar-research.md`, then refreshed radar scores/blurbs in `app.py` from that research.

## 5. Image generation for meetup promos

- Generated two **Instagram-style** talk posters with Grok Bot’s image tool.
- Dropped them under `assets/` and added a divider + “Tonight at Only Devs Bangkok” section at the bottom of the app.
- Delivered the same images in chat / raw GitHub URLs so they could be saved to a phone for Stories.

## 6. Agent briefs in the repo

- Authored a ready-to-paste agent prompt in `notes/agent-prompt-st-map-cities.md` for a future `st.map` world view of the radar cities — **without** changing the app yet.

## 7. Memory + continuity

- Remembered Alpha, the GitHub account, the live Streamlit URL, and the ongoing City Radar workflow across turns so the bot didn’t re-ask basics.

## 8. Delivery to the presenter

- Assembled this `slides/` folder: progression screenshots from the browser + this feature summary for the lightning talk.

---

## Suggested 60-second talk arc

1. **Ask** → “Build a spider-chart Streamlit demo and put it on my PC + GitHub.”
2. **Ship** → local run, then Streamlit Cloud.
3. **See** → bot opens the live app and screenshots what the audience sees.
4. **Improve** → research Da Nang + cities; regenerate scores; add tonight’s talk promos.
5. **Meta** → the bot is also writing the slide assets for *this* lightning talk.
