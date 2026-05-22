# %%
# 
from pathlib import Path
from datetime import datetime

import folium
import gpxpy


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

GPX_FOLDER = Path("gpx_files")
FIGS_FOLDER = Path("figs")
FIGS_FOLDER.mkdir(exist_ok=True)

MAP_CENTER = [56.16, 10.20]
ZOOM_START = 8

# Year → color
YEAR_COLORS = {
    2024: "#00ff66",  # green
    2025: "#ccff00",  # yellow-green
    2026: "#ff1493",  # pink
    2024: "#ff8c00",  # orange
}


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def extract_date(filename: str) -> datetime:
    """
    Extract date from filenames like:
    2024-05-18_activity.gpx
    """
    date_str = filename.split("_")[0]
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_color(year: int) -> str:
    """
    Return a color for a given year.
    Falls back to white if the year is missing.
    """
    return YEAR_COLORS.get(year, "#ffffff")


def load_coordinates(gpx_path: Path):
    """
    Load all coordinate sequences from a GPX file.
    """
    with open(gpx_path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    for track in gpx.tracks:
        for segment in track.segments:
            coords = [
                (point.latitude, point.longitude)
                for point in segment.points
            ]

            if len(coords) >= 2:
                yield coords
# %%

# --------------------------------------------------
# LOAD FILES
# --------------------------------------------------

gpx_files = sorted(
    GPX_FOLDER.glob("*.gpx"),
    key=lambda p: extract_date(p.name)
)


# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

m = folium.Map(
    location=MAP_CENTER,
    zoom_start=ZOOM_START,
    tiles="CartoDB positron"
)

for gpx_file in gpx_files:

    date = extract_date(gpx_file.name)
    color = get_color(date.year)

    for coords in load_coordinates(gpx_file):

        folium.PolyLine(
            locations=coords,
            color=color,
            weight=2,
            opacity=0.5,
        ).add_to(m)


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

m
# %%

# save

m.save(FIGS_FOLDER / "rides_map.html")

# %%


# %%
