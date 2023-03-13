import streamlit as st
import pandas as pd
from vega_datasets import data
import altair as alt

alt.data_transformers.disable_max_rows()

# Page Set Up 
st.title("SI 649 Altair Assignment 4")
st.write("Haley Johnson")

# Create tabs on visualization 
tab1, tab2, tab3, tab4 = st.tabs(['Question 1', 'Question 2', 'Question 3', 'Question 4'])

# Visualization 1
df = pd.read_csv('https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/airports.csv')
url = "https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/small-airports.json"
world = alt.topo_feature(url, feature = 'continent')

base = alt.Chart(world).mark_geoshape(
    fill = 'lightgray',
    stroke = 'white'
).project('mercator')

points = alt.Chart(df).mark_circle().transform_filter(
    alt.datum.type == 'small_airport'
).encode(
    latitude = alt.X('latitude_deg:Q'), 
    longitude = alt.Y('longitude_deg:Q'), 
    size = alt.value(10),
    color = alt.value('red'), 
    tooltip = alt.Tooltip('name:N')
)

ch1 = alt.layer(
    base, points
).properties(
    #width = 850, 
    height = 700, 
    title = 'Small airports in the world'
).configure_title(
    fontSize = 25
)

# Visualization 2
countries_url = data.world_110m.url
source = 'https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/population_prediction.csv'
world = alt.topo_feature(countries_url, feature = 'countries')

world_map = alt.Chart(world).mark_geoshape(
    fill = 'lightgray', 
    stroke = 'white'
).project(
    "naturalEarth1"
)

base = alt.Chart().mark_circle(
    fill = 'green', 
    stroke = 'white'
).encode(
    latitude = 'lat:Q',
    longitude = 'lon:Q', 
    size = alt.Size('population:Q', scale = alt.Scale(range = [0, 1500]), 
                    legend = alt.Legend(title = 'Population (millions)')), 
    tooltip = [alt.Tooltip('city:N', title = 'City'), alt.Tooltip('population:Q', title = 'Population')], 
    opacity = alt.value(0.75)
)

ch2 = alt.layer(world_map, base, data = source
).facet('year:N', 
        columns = 2
).properties(
    title = 'The 20 Most Populous Cities in the World by 2100'
).configure_title(
    fontSize = 15
)

# Visualization 3
states_url = data.us_10m.url
hurricane_data = pd.read_csv('https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/hurdat2.csv')

hurricane_data['year'] = pd.DatetimeIndex(hurricane_data['datetime']).year
continent_hurricanes = hurricane_data[~hurricane_data.index.isin([2, 15])]

states = alt.topo_feature(states_url, feature = 'states')

us = alt.Chart(states).transform_filter(
    (alt.datum.id != 2) & (alt.datum.id != 15)
).mark_geoshape(
    fill = 'white', 
    stroke = 'black', 
    strokeWidth = 1.5
).project('mercator')

lines = alt.Chart(continent_hurricanes).mark_line(
    stroke = 'blue', 
    strokeWidth = 1
).transform_filter(
    (alt.datum.year == 2017) 
).encode(
    latitude = 'latitude:Q', 
    longitude = 'longitude:Q'
)

ch3 = alt.layer(
    us, lines
).properties(
    width = 800, 
    height = 400, 
    title = 'Hurricane Trajectories in the Continental US, 2017'
).configure_title(
    fontSize = 20
)

# Visualization 4
state_map = data.us_10m.url
state_pop = data.population_engineers_hurricanes()[['state', 'id', 'population']]
states = alt.topo_feature(state_map, 'states')

hover_select = alt.selection_single(on = 'click', fields = ['state'])
opacity_condition = alt.condition(hover_select, alt.value(1.0), alt.value(0.25))

states_view = alt.Chart(states).add_selection(hover_select
).mark_geoshape().project(
    'albersUsa'
).transform_lookup(
    lookup = 'id', from_ = alt.LookupData(data = state_pop, key='id', fields=['state', 'population'])
).encode(
    color = alt.Color('population:Q'), 
    opacity = opacity_condition
)

states_bar = alt.Chart(state_pop).add_selection(hover_select).mark_bar(
).transform_window(
    rank = 'row_number()', 
    sort = [alt.SortField('population', order = 'descending')]
).transform_filter(
    (alt.datum.rank <= 15)
).encode(
    x = alt.X('population:Q', axis = alt.Axis(title = 'Population')), 
    y = alt.Y('state:N', sort = alt.EncodingSortField(field = 'population'), axis = alt.Axis(title = 'State')), 
    color = alt.Color('population:Q'), 
    opacity = opacity_condition
).properties(
    title = 'Top 15 states by population'
)

ch4 = alt.hconcat(states_view, states_bar)

# Add Visualizations to Page
with tab1: 
    st.altair_chart(ch1)
with tab2: 
    st.altair_chart(ch2)
with tab3:
    st.altair_chart(ch3)
with tab4:
    st.altair_chart(ch4)