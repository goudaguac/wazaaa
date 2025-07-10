import streamlit as st
import geopandas as gpd
import pandas as pd

st.set_page_config(page_title="Hospitality Land Calculator", layout="wide")

st.title("🏨 Hospitality Land Calculator (URA Master Plan 2019)")

# -------------------------------
# 1. Load your GeoJSON / KML
# -------------------------------
# Example: load from local folder
geojson_file = "data/MP2019_UDG.geojson
"

try:
    gdf = gpd.read_file(geojson_file)
    st.success("✅ GeoJSON loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load GeoJSON: {e}")

# Show available columns
st.subheader("📍 Master Plan Data Preview")
st.write(gdf.head())

# -------------------------------
# 2. User selects site by planning area or plot name
# -------------------------------
selected_site = st.selectbox("Select Site", gdf['SITE_NAME'].unique())
site_row = gdf[gdf['SITE_NAME'] == selected_site].iloc[0]

# Extract site-specific info
site_area = site_row['SITE_AREA']  # e.g. in sqm, if available
plot_ratio = site_row['PLOT_RATIO']
height_limit = site_row['MAX_BUILDING_HEIGHT']

st.info(f"📌 Site Area: {site_area} sqm | Plot Ratio: {plot_ratio} | Height Limit: {height_limit} m")

# -------------------------------
# 3. Custom land specifics
# -------------------------------
st.subheader("✏️ Custom Inputs")

if site_area == 0 or pd.isnull(site_area):
    site_area = st.number_input("Land Area (sqm)", min_value=0.0, value=1000.0)

efficiency_factor = st.slider("Efficiency Factor (NFA as % of GFA)", min_value=0.6, max_value=0.95, value=0.8)

avg_room_size = st.slider("Average Room Size (sqm)", min_value=20, max_value=30, value=23)

# -------------------------------
# 4. Compute GFA, NFA, Max Levels, Max Rooms
# -------------------------------
gfa = site_area * plot_ratio
nfa = gfa * efficiency_factor

# Estimate storey height (assume avg 3.5m per floor)
storey_height = 3.5
max_levels = min(int(height_limit // storey_height), int(plot_ratio * 2))  # Basic limit: site-specific or plot ratio

max_rooms = int(nfa / avg_room_size)

# -------------------------------
# 5. Show Results
# -------------------------------
st.subheader("📊 Estimated Outputs")

col1, col2 = st.columns(2)

with col1:
    st.metric("Gross Floor Area (GFA)", f"{gfa:,.2f} sqm")
    st.metric("Net Floor Area (NFA)", f"{nfa:,.2f} sqm")

with col2:
    st.metric("Max Levels Allowed", max_levels)
    st.metric("Estimated Max Rooms", max_rooms)

# -------------------------------
# 6. Map Preview (Optional)
# -------------------------------
st.subheader("🗺️ Site Geometry")
st.map(gdf[gdf['SITE_NAME'] == selected_site])

# -------------------------------
# 7. Downloadable Report (Optional)
# -------------------------------
st.download_button(
    label="Download Calculation Summary",
    data=f"""
Site: {selected_site}
Land Area: {site_area} sqm
Plot Ratio: {plot_ratio}
Height Limit: {height_limit} m
Efficiency Factor: {efficiency_factor}
Avg Room Size: {avg_room_size} sqm

Gross Floor Area: {gfa:.2f} sqm
Net Floor Area: {nfa:.2f} sqm
Max Levels: {max_levels}
Estimated Max Rooms: {max_rooms}
    """,
    file_name="site_calculation.txt",
)



