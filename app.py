import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Hospitality Land Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏨 Hospitality Land-to-Rooms Calculator")

# Layout: 2 columns
left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("Input Parameters")
    land_area = st.number_input("Land Area (sqm)", value=1000)
    plot_ratio = st.number_input("Plot Ratio", value=3.0)
    gross_floor_area = land_area * plot_ratio
    st.write(f"Estimated Gross Floor Area (GFA): {gross_floor_area:.2f} sqm")

    efficiency_factor = st.slider(
        "Efficiency Factor (percentage of GFA usable for rooms)",
        min_value=50, max_value=100, value=80
    )

    usable_area = gross_floor_area * (efficiency_factor / 100)
    st.write(f"Usable Area for Rooms: {usable_area:.2f} sqm")

    avg_room_size = st.slider(
        "Average Room Size (sqm)",
        min_value=20, max_value=50, value=25
    )

    if st.button("🔍 Calculate Maximum Rooms"):
        max_rooms = int(usable_area // avg_room_size)
        st.session_state['max_rooms'] = max_rooms
        st.session_state['usable_area'] = usable_area
        st.session_state['gross_floor_area'] = gross_floor_area

with right_col:
    st.header("Calculation Results")
    if 'max_rooms' in st.session_state:
        st.success(f"✅ Estimated Maximum Rooms: {st.session_state['max_rooms']}")
        st.write(f"- Gross Floor Area (GFA): {st.session_state['gross_floor_area']:.2f} sqm")
        st.write(f"- Usable Area: {st.session_state['usable_area']:.2f} sqm")
        st.write(f"- Avg. Room Size: {avg_room_size} sqm")

    else:
        st.info("Enter your land details and click **Calculate** to see results!")

    st.markdown("---")
    st.write("📐 **Space for future diagrams and visuals!**")

