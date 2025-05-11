# -*- coding: utf-8 -*-
# pip install streamlit plotly pandas geopandas

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Indian States - Art & Culture", layout="wide")

# Load data
data = pd.read_csv("C:/Users/RahulBacche/Desktop/Culture HT/Indian art and culture.csv") 

# Load India states geojson (from GitHub or local)
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
    return gpd.read_file(url)

gdf = load_geojson()

#gdf.to_csv("C:/Users/RahulBacche/Desktop/Culture HT/gdf.csv")

# Merge geo data with your cultural data
data.columns = data.columns.str.strip()  # Strip any extra spaces
merged = gdf.merge(data, how="left", left_on="NAME_1", right_on="State")

#merged.to_csv("C:/Users/RahulBacche/Desktop/Culture HT/merged.csv")

# Draw the map using Plotly
fig = px.choropleth_mapbox(
    merged,
    geojson=merged.geometry.__geo_interface__,
    locations=merged.index,
    color_discrete_sequence=["#636EFA"],
    mapbox_style="carto-positron",
    zoom=3.8,
    center={"lat": 22.5937, "lon": 78.9629},
    hover_name="State",
    hover_data=["Art/Culture Form", "Description"],
    opacity=0.6,
)

fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

# Title
st.title("🎨 Indian States: Art & Culture Explorer")

# Display Map
st.plotly_chart(fig, use_container_width=True)

# Sidebar for selecting a state
selected_state = st.sidebar.selectbox("Select a State", sorted(data["State"].dropna()))


# Show art and culture info
state_data = data[data["State"] == selected_state]
if not state_data.empty:
    st.subheader(f"🎭 Art & Culture of {selected_state}")
    st.markdown(f"**Art Form:** {state_data.iloc[0]['Art and Culture Form']}")
    st.markdown(f"**Description:** {state_data.iloc[0]['Description']}")
