# app.py

import streamlit as st
import folium
import branca.colormap as cm
from streamlit_folium import st_folium
from src.spatial_logic import load_data, calculate_suitability

st.set_page_config(page_title="Berlin BESS Spatial Analysis", layout="wide", page_icon="🗺️")

st.title("🗺️ Berlin BESS Placement Optimizer")
st.markdown("Interactive GIS tool for optimal Battery Energy Storage System (BESS) placement for Peak Shaving.")

# --- Sidebar UI ---
st.sidebar.header("⚖️ MCDA Weights")
w_grid = st.sidebar.slider("Grid Congestion Weight", 0.0, 1.0, 0.5, 0.1)
w_land = st.sidebar.slider("Land Price Weight", 0.0, 1.0, 0.3, 0.1)
w_solar = st.sidebar.slider("Solar Potential Weight", 0.0, 1.0, 0.2, 0.1)

# جلوگیری از خطای تقسیم بر صفر و نرمال کردن وزن‌ها
total_weight = w_grid + w_land + w_solar
if total_weight > 0:
    w_grid, w_land, w_solar = w_grid/total_weight, w_land/total_weight, w_solar/total_weight
else:
    st.sidebar.error("حداقل یک وزن باید بزرگتر از صفر باشد.")

# --- Core Logic ---
# خواندن فایل ساخته شده در مرحله قبل
gdf = load_data("data/berlin_grid_data.geojson")
gdf_scored = calculate_suitability(gdf, w_grid, w_land, w_solar)
best_location = gdf_scored.iloc[0]

# --- Mapping ---
berlin_map = folium.Map(
    location=[52.5200, 13.4050], 
    zoom_start=11, 
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Esri'
)

colormap = cm.LinearColormap(
    colors=['red', 'yellow', 'green'],
    vmin=gdf_scored['suitability_score'].min(),
    vmax=gdf_scored['suitability_score'].max()
)
colormap.add_to(berlin_map)

# رسم زون‌ها روی نقشه
for _, row in gdf_scored.iterrows():
    geo_json = row['geometry'].__geo_interface__
    score = row['suitability_score']
    
    popup_text = (
        f"<b>Score:</b> {score:.2f}<br>"
        f"<b>Grid:</b> {row['grid_congestion']:.2f}<br>"
        f"<b>Land:</b> {row['land_price']:.0f} €/m²<br>"
        f"<b>Solar:</b> {row['solar_potential']:.0f} MWh"
    )
    
    folium.GeoJson(
        geo_json,
        style_function=lambda feature, color=colormap(score): {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        tooltip=popup_text
    ).add_to(berlin_map)

# علامت‌گذاری بهترین نقطه
best_centroid = best_location['geometry'].centroid
folium.Marker(
    location=[best_centroid.y, best_centroid.x],
    popup=f"🏆 Optimal 5MW BESS Location (Score: {best_location['suitability_score']:.2f})",
    icon=folium.Icon(color='blue', icon='star')
).add_to(berlin_map)

# --- Dashboard Layout ---
col1, col2 = st.columns([3, 1])

with col1:
    st_folium(berlin_map, width=800, height=500)

with col2:
    st.subheader("🏆 Top Location Stats")
    st.metric("Suitability Score", f"{best_location['suitability_score']:.2f}")
    st.metric("Grid Congestion", f"{best_location['grid_congestion']:.2f}")
    st.metric("Land Price (€/m²)", f"{best_location['land_price']:.0f}")
    st.metric("Solar Potential (MWh)", f"{best_location['solar_potential']:.0f}")

st.divider()
st.subheader("📊 Ranked Zones Dataframe")
st.dataframe(gdf_scored[['suitability_score', 'grid_congestion', 'land_price', 'solar_potential']].head(10), use_container_width=True)
