import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random



long_lat_cities = pd.read_csv("2024 Trips.csv")

# Set up the page configuration
st.set_page_config(
    page_title="Marty and Brandees 2024 Trips",
    page_icon="🛫",
    #page_subtitle = 'Trips Wrapped',
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to mimic your theme settings
custom_theme = f"""
<style>
    /* Set the main background color */
    .stApp {{
        background-color: #acb7ae; /* Background color */
    }}

    /* Primary color for buttons and links */
    .stButton>button {{
        background-color: #9e8a77; /* Primary color */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #735c4a; /* Darker shade for hover */
        color: white;
    }}

    /* Secondary background color for containers and sidebar */
    .css-1d391kg {{
        background-color: #3a4660; /* Sidebar background color */
        color: white;
    }}

    /* Text colors */
    h1, h2, h3, h4, h5, h6 {{
        color: #9e8a77; /* Primary text color */
    }}
    p {{
        color: white; /* Standard text */
    }}
</style>
"""

# Inject the custom theme
st.markdown(custom_theme, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home",  "Locations", "Your Travel Wrapped","Fun Facts"])

# Home Page
if page == "Home":
    st.title("Marty and Brandees 2024 Trips 🛫")
    st.write(
        """
        ## Merry Christmas!! 

        You guys did a lot this year, and went to places all over the country. 
        Whether it was for track, Arizona visits, weddings, or JFK hot spots, you guys did it all. 
       
        It was really fun living with you guys for most of this year, and I don't think I will ever be able 
        to thank you! it was a lot of fun getting to see everywhere that you guys went too! 

        Chat GPT describes your travel vibe as: 

        *"Balanced Wanderlust": This year's travel embodies a perfect blend of adventure, relaxation, and cultural immersion. 
        It's about embracing the thrill of nature, the richness of history, and the joy of leisure, all while exploring both far-off destinations and nearby treasures.*
        
        Here is a dashboard to capture all of your adventures and travels of 2024! 

        Excited to see where youll go in 2025! 

        v.1.0

        """
    )

    
    col1, col2 = st.columns(2)

    with col1:
        st.image("IMG_FE91E5B33D1E-1.jpeg", caption="Hartford, CT", width=300)
    with col2: 
        st.image("IMG_2153.jpg", caption="Arches", width = 300)
## MAP VIEW 
elif page == "Locations":

    st.title("Oh The Places You Went!")

    # Initialize session state for controlling visibility of the table
    if "show_table" not in st.session_state:
        st.session_state.show_table = False

# Button to toggle the display of the table
    if st.button("List of Places You Went"):
        st.session_state.show_table = not st.session_state.show_table

        st.balloons()

# Display or hide the table based on the state
    if st.session_state.show_table:
        st.write("### List of Places You Visited in 2024")
        st.dataframe(long_lat_cities['City'], use_container_width=True)
    else:
        st.write("The table is currently hidden. Click the button to show it!")

    # Sample data with latitudes and longitudes of US cities
    us_cities = {
        "City": long_lat_cities["City"],
        "State": long_lat_cities["State"],
        "lat": long_lat_cities["Long"],
        "lon": long_lat_cities["Lat"]
    }
    st.write('## See it on a map!!')
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
        title="Map of the places"
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
    st.title('2024 Travel Wrapped')

    st.write("""
             ##### Theres a lot of stats to go along with your travels!

            Here are some fun metrics! 

              """)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("You went on", "20 trips", "🤗")
    with col2: 
        st.metric("You went to", "12 states", "🤭")

    with col3: 
        st.metric("You went to", "One other Country","🇨🇦")

    st.divider()
    
    col1, col2 = st.columns(2)

    travel_data = pd.DataFrame({
        "Mode of Transportation": ["Driving", "Flying", "Train"], 
        "Hours": [30.8, 46.9, 3]

    })

    travel_days = pd.DataFrame({
        "Day of Week": ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
        "Number of travels on this day" : [11, 3, 7, 6, 4, 8, 3]
    })

    travel_months = pd.DataFrame({
        "Month": ["January","February","March","April", "May","June","July","August","September","October","November","December"],
        "Number of Trips Taken":[2, 2, 2, 4, 1, 1, 2, 1, 2, 2, 1, 1]
    })

# Column 1: Pie Chart
    with col1:
        st.subheader("Travel Breakdown")

        #create a bar chart with plotly 
        fig1 = px.bar(travel_days, "Day of Week", "Number of travels on this day", title = "what day did you travel the most?")
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        #create another bar chart 

        fig2 = px.bar(travel_months, "Month","Number of Trips Taken", color= "Month", title = "What month did you travel the most?")
        st.plotly_chart(fig2,use_container_width=True)


        


    custom_box_style = """
    <div style="
        background-color: #808080; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); 
        text-align: center;">
        <h3 style="color: #333;">Key Metrics</h3>
        <p style="margin: 10px 0; font-size: 16px;"><b>Highest day of travel:</b> Sunday <span style="color: #ff6f61;">(11 days!)</span></p>
        <p style="margin: 10px 0; font-size: 16px;"><b>Highest month of travel:</b> April <span style="color: #ff6f61;">(4 trips!)</span></p>
        <p style="margin: 10px 0; font-size: 16px;"><b>Total Hours of Travel:</b> 173.92 hours</p>
        <p style="margin: 10px 0; font-size: 16px;"><b>That Means:</b> 7.246 days</p>
    </div>
    """

    # Column 2: Metric
    with col2:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown(custom_box_style, unsafe_allow_html=True)

            # Create a pie chart using Plotly
            fig = px.pie(travel_data, names="Mode of Transportation", values="Hours", title="How did you get places?")
            st.plotly_chart(fig, use_container_width=True)



    travel_metrics = {
    "Most Visited Place": {"name": "Tucson, AZ", "image": "tucson.jpeg", "value": "4 visits"},
    "Longest Flight": {"name": "Honolulu, HI", "image": "honolulu.jpeg", "value": "7.5 hours"},
    "Longest Drive": {"name": "Tucson, AZ", "image": "tucson.jpeg", "value": "12 hours"},
    "Place Stayed the Longest": {"name": "Hartford, CT + Burlington, VT + Montreal, Canada", "image": "longest_trip.jpeg", "value": "9 days"},
    "Total Days of Travel": {"name": "All Places", "image": "travel_days.jpeg", "value": "30 days"},
    "Total Hours of Travel": {"name": "All Flights", "image": "flying_hours.jpeg", "value": "40 hours"},
}
    
    st.divider()

     # Data for destinations and distances
    data = {
        "Destination": [
            "Anaheim, CA", "Tucson, AZ", "Boston / Cape Cod, MA", "Spearfish, SD", 
            "Pittsburgh, KS", "Orlando / Miami, FL", "Grand Junction, CO", 
            "Moab, UT / Grand Junction, CO", "Dallas, TX", "New York, NY", 
            "Orlando, FL", "Hartford, CT/Burlington, VT/Montreal", "Vail, CO", 
            "Honolulu / Kona, HI"
        ],
        "Distance (miles)": [
            1000, 850, 2000, 400, 550, 1700, 240, 340, 800, 1800, 1700, 1900, 120, 3400
        ]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Calculate metrics
    total_distance = df["Distance (miles)"].sum()
    average_distance = df["Distance (miles)"].mean()

    # Title
    st.write("### Your Travels in Distance!")

    # Metrics for total and average distance
    st.metric("Total Distance Traveled", f"{total_distance:,} miles")
    st.metric("Average Distance Per Trip", f"{average_distance:.2f} miles")

    # Divider
    st.divider()

    # Bar chart for distances
    st.subheader("📊 Distance to Each Destination")
    fig_bar = px.bar(
        df,
        x="Destination",
        y="Distance (miles)",
        title="Distance from Broomfield, CO to Each Destination",
        labels={"Distance (miles)": "Distance (miles)"},
        color="Distance (miles)",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Divider
    st.divider()

    # Interactive map with destinations
    st.subheader("🗺️ Map of Travel Destinations")
    map_fig = go.Figure()

    # Add Broomfield as the starting point
    map_fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=[-105.0905],  # Longitude for Broomfield, CO
        lat=[39.9205],    # Latitude for Broomfield, CO
        text=["Broomfield, CO"],
        mode='markers',
        marker=dict(size=10, color='red'),
        name="Broomfield, CO"
    ))

    # Add destinations
    destination_coords = {
        "Anaheim, CA": (-117.9145, 33.8353),
        "Tucson, AZ": (-110.9747, 32.2226),
        "Boston / Cape Cod, MA": (-70.3088, 41.805),
        "Spearfish, SD": (-103.8594, 44.4902),
        "Pittsburgh, KS": (-94.7049, 37.4109),
        "Orlando / Miami, FL": (-81.3792, 28.5383),
        "Grand Junction, CO": (-108.5506, 39.0639),
        "Moab, UT / Grand Junction, CO": (-109.5504, 38.5733),
        "Dallas, TX": (-96.7970, 32.7767),
        "New York, NY": (-74.0060, 40.7128),
        "Orlando, FL": (-81.3792, 28.5383),
        "Hartford, CT/Burlington, VT/Montreal": (-72.6851, 41.7637),
        "Vail, CO": (-106.3742, 39.6403),
        "Honolulu / Kona, HI": (-157.8583, 21.3069)
    }

    for place, coords in destination_coords.items():
        map_fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[coords[0]],
            lat=[coords[1]],
            text=[place],
            mode='markers',
            marker=dict(size=7, color='blue'),
            name=place
        ))

    # Draw arcs from Broomfield to each destination
    broomfield_coords = (-105.0905, 39.9205)
    for place, coords in destination_coords.items():
        map_fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[broomfield_coords[0], coords[0]],
            lat=[broomfield_coords[1], coords[1]],
            mode='lines',
            line=dict(width=1, color='blue'),
            name=f"Path to {place}"
        ))

    map_fig.update_layout(
        title="Travel Map from Broomfield, CO",
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type="albers usa"),
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)"
        )
    )
    st.plotly_chart(map_fig, use_container_width=True)

    # Divider
    st.divider()

    # Table of distances
    st.subheader("📋 Travel Distances Table")
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("The Awards!")     

    if "metrics_state" not in st.session_state:
        st.session_state.metrics_state = {key: False for key in travel_metrics.keys()}

    col1, col2, col3, col4 = st.columns(4)  # First row with 3 columns
   

    with col1:
        if st.button("Most Visited Place"):
            st.session_state.metrics_state["Most Visited Place"] = not st.session_state.metrics_state["Most Visited Place"]

        if st.session_state.metrics_state["Most Visited Place"]:
            st.metric("Most Visited Place", travel_metrics["Most Visited Place"]["value"])
            st.image(travel_metrics["Most Visited Place"]["image"], caption="Most Visited Place", use_column_width=True)

    with col2:
        if st.button("Longest Flight"):
            st.session_state.metrics_state["Longest Flight"] = not st.session_state.metrics_state["Longest Flight"]

        if st.session_state.metrics_state["Longest Flight"]:
            st.metric("Longest Flight", travel_metrics["Longest Flight"]["value"])
            st.image(travel_metrics["Longest Flight"]["image"], caption="Longest Flight", use_column_width=True)

    with col3:
        if st.button("Longest Drive"):
            st.session_state.metrics_state["Longest Drive"] = not st.session_state.metrics_state["Longest Drive"]

        if st.session_state.metrics_state["Longest Drive"]:
            st.metric("Longest Drive", travel_metrics["Longest Drive"]["value"])
            st.image(travel_metrics["Longest Drive"]["image"], caption="Longest Drive", use_column_width=True)

    # Second row of metrics
    with col4:
        if st.button("Place Stayed the Longest"):
            st.session_state.metrics_state["Place Stayed the Longest"] = not st.session_state.metrics_state["Place Stayed the Longest"]

        if st.session_state.metrics_state["Place Stayed the Longest"]:
            st.metric("Stayed the Longest", travel_metrics["Place Stayed the Longest"]["value"])
            st.image(travel_metrics["Place Stayed the Longest"]["image"], caption="Stayed the Longest", use_column_width=True)

# Sidebar navigation for page selection

## Fun Facts Stats
elif page == "Fun Facts":
    st.title('Fun Facts')


    # Fun facts about each destination
    fun_facts = {
    "Anaheim, CA": "🎢 Elvis Presley visited Disneyland in 1957 and even rode the Jungle Cruise! Walt Disney himself gave Elvis a private tour.",
    "Tucson, AZ": "🎥 Elvis Presley filmed *Stay Away, Joe* in Tucson in 1968. While in town, he reportedly loved visiting local diners for classic southwestern food.",
    "Boston / Cape Cod, MA": "🏖️ John F. Kennedy loved spending summers at Hyannis Port in Cape Cod, and the area now has a JFK Museum showcasing his life and legacy.",
    "Spearfish, SD": "🌌 Spearfish is famous for its stunning night skies and was one of the first places to advocate for 'dark sky' preservation.",
    "Pittsburgh, KS": "🎤 JFK delivered an inspirational campaign speech nearby in 1960, focusing on economic growth for small towns in Kansas.",
    "Orlando / Miami, FL": "🎶 Elvis Presley caused a frenzy in Miami during his 1956 Florida tour, with fans camping out to catch a glimpse of him before his sold-out concerts.",
    "Grand Junction, CO": "⛰️ Grand Junction is known as Colorado's wine country! The region produces award-winning wines thanks to its unique high-desert climate.",
    "Moab, UT / Grand Junction, CO": "🌄 Moab is a top filming location for Hollywood movies, including *Indiana Jones* and *Thelma & Louise*. JFK also dedicated Flaming Gorge Dam nearby.",
    "Dallas, TX": "📜 JFK’s final speech was in Fort Worth, but Dallas is also where Elvis Presley performed multiple sold-out shows in the 1950s.",
    "New York, NY": "🎤 Elvis Presley rocked Madison Square Garden in 1972, delivering one of his most iconic live performances.",
    "Orlando, FL": "🚀 The Kennedy Space Center near Orlando honors JFK’s vision for space exploration, making it a must-visit for space enthusiasts.",
    "Hartford, CT/Burlington, VT/Montreal": "📜 JFK visited Hartford in 1956, and the city is also home to Mark Twain’s historic house and museum.",
    "Vail, CO": "🎿 Vail is one of the largest ski resorts in the world and a favorite spot for celebrities. Elvis Presley was rumored to enjoy skiing nearby in Aspen!",
    "Honolulu / Kona, HI": "🌺 Elvis Presley’s *Blue Hawaii* (1961) was filmed on Oahu. Elvis loved Hawaii so much that he performed his famous *Aloha from Hawaii* concert here in 1973."
}
    # Title for the Streamlit app
    st.title("🎉 Fun Facts About Your Travel Destinations 🎤🚀")

    # Add a section to display a random fun fact
    st.subheader("✨ Click for a Random Fun Fact!")
    if st.button("🎲 Show Random Fun Fact"):
        random_place = random.choice(list(fun_facts.keys()))
        st.write(f"📍 **{random_place}**: {fun_facts[random_place]}")

    st.divider()

    # Add a cool grid-based display for all fun facts
    st.subheader("📍 Explore Fun Facts by Destination")
    cols = st.columns(3)  # Divide the display into three columns for a grid layout

    # Loop through the fun facts and display them in columns
    for idx, (place, fact) in enumerate(fun_facts.items()):
        col = cols[idx % 3]  # Distribute items across the three columns
        with col:
            if st.button(f"📍 {place}"):
                st.markdown(f"**{fact}**")
                st.success(f"You just learned about {place}! 🌟")

    ## two colum: showing stuff about JFK and Elvis and major figures and stuff 

