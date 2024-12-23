import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import numpy as np



long_lat_cities = pd.read_csv("2024 Trips.csv")

# Set up the page configuration
st.set_page_config(
    page_title="Marty and Brandees 2024 Trips",
    page_icon="🛫",
    #page_subtitle = 'Trips Wrapped',
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Your Travel Wrapped", "Map view", "Flight Stats", "Fun Facts", "Photos"])

# Home Page
if page == "Home":
    st.title("Marty and Brandees 2024 Trips 🛫")
    st.write(
        """
        ## Merry Christmas!! 

        """
    )

    

    st.image("/Users/emilygalvin/VS Code/2024_project/IMG_FE91E5B33D1E-1.jpeg", caption="Placeholder Image for Home Page", width=300)

## MAP VIEW 
elif page == "Map view":

    st.title("Map view")

    st.button("Click here to see list of places you went!")

    # Sample data with latitudes and longitudes of US cities
    us_cities = {
        "City": long_lat_cities["City"],
        "State": long_lat_cities["State"],
        "lat": long_lat_cities["Long"],
        "lon": long_lat_cities["Lat"]
    }

    # Create DataFrame with a time dimension (e.g., days, months)
    time_steps = 10
    time_df = pd.DataFrame({
        "time": np.tile(range(1, time_steps + 1), len(us_cities['City'])),
        "City": np.repeat(us_cities['City'], time_steps),
        "lat": np.repeat(us_cities['lat'], time_steps),
        "lon": np.repeat(us_cities['lon'], time_steps)
    })

    # Add random offset to the latitudes and longitudes to simulate movement
    time_df['lat'] += np.random.randn(len(time_df)) * 0.001
    time_df['lon'] += np.random.randn(len(time_df)) * 0.001

    # Create the figure using go.Scattermapbox
    fig = go.Figure(
        go.Scattermapbox(
            mode="markers",  # 'markers' will plot points
            lat=time_df['lat'],
            lon=time_df['lon'],
            text=time_df['City'],
            marker=dict(size=10),
            name="City Positions"
        )
    )

    # Create frames for animation
    frames = []
    for time_step in range(1, time_steps + 1):
        frame_data = time_df[time_df['time'] == time_step]
        frame = go.Frame(
            data=[go.Scattermapbox(
                mode="markers", 
                lat=frame_data['lat'],
                lon=frame_data['lon'],
                text=frame_data['City'],
                marker=dict(size=10),
                name=f"Step {time_step}"
            )],
            name=f"Frame {time_step}"
        )
        frames.append(frame)

    # Set up the layout with animation options
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 39.9205, "lon": -105.0867},
        updatemenus=[dict(
            type="buttons",
            x=0.1,
            xanchor="right",
            y=0,
            yanchor="top",
            buttons=[dict(
                args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                label="Play",
                method="animate"
            )]
        )],
        height=600,
        title="Animated Map of US Cities"
    )

    fig.update_traces(
        marker = dict(
            color="blue"

        )
    )

    # Add the frames to the figure
    fig.frames = frames

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)



## QUICK FACTS 
elif page == "Your Travel Wrapped":
    st.title('Quick Facts')

    ###add in the blocks stuff 


## Flight Stats
elif page == "Flight Stats":
    st.title('Flight Stats')

    ### add in stuff about southwest and flight times and a bar chart? Something?

## Fun Facts Stats
elif page == "Fun Facts":
    st.title('Fun Facts')

    ## two colum: showing stuff about JFK and Elvis and major figures and stuff 

## Photos
elif page == "Photos":
    st.title('Photos')