import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import geocoder
import plotly.express as px

# Initialize an empty DataFrame to store employee data
EMPLOYEE_DATA = pd.DataFrame(columns=['Employee ID', 'Check-in Time', 'Check-out Time'])

# Function to handle employee functionalities
def employ():
    st.subheader("Employee Dashboard")
    current_location = get_location() 

    # Check if the employee is within the specified coordinates
    # locattion coordinates for geo-fencing should be updated manually
    if current_location and current_location[0] == 12.954893 and current_location[1] == 80.24415:
        with st.form(key='employeeForm'):
            eid = st.text_input('Enter your Employee ID:')
            submit_button = st.form_submit_button('Submit')

        if submit_button and eid:
            st.write('Form submitted for Employee ID:', eid)
            check_in_button = st.button('Check-in')
            check_out_button = st.button('Check-out')

            if check_in_button:
                check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_entry = {'Employee ID': eid, 'Check-in Time': check_time, 'Check-out Time': ''}
                EMPLOYEE_DATA.loc[len(EMPLOYEE_DATA)] = new_entry
                st.success('Checked in successfully.')
            elif check_out_button:
                row = EMPLOYEE_DATA[(EMPLOYEE_DATA['Employee ID'] == eid) & (EMPLOYEE_DATA['Check-out Time'] == '')]
                if not row.empty:
                    check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    EMPLOYEE_DATA.loc[row.index[0], 'Check-out Time'] = check_time
                    st.success('Checked out successfully.')
                else:
                    st.error('You need to check-in first.')
    else:
        st.error('Please enter the company premises to mark attendance.')
    return EMPLOYEE_DATA

def get_location():
    """Fetches the user's current location using geocoder."""
    location = geocoder.ip('me').latlng
    if location:
        latitude, longitude = location[0], location[1]
        st.info(f"Current Location: Latitude {latitude}, Longitude {longitude}")

        # Displaying the user's location on a map
        fig = px.scatter_mapbox(data_frame=None, lat=[latitude], lon=[longitude], zoom=12)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)

        return latitude, longitude
    else:
        st.error("Failed to fetch current location.")
        return None

# Function to handle admin functionalities
def admin():
    st.subheader("Admin Functionalities")
    
    def download_link(df, filename):
        """Generates a link to download dataframe."""
        csv = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode('utf-8')
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download</a>'

    st.markdown("Click on the 'Download Data' button below to get all the data in CSV format.")
    st.markdown(download_link(EMPLOYEE_DATA, "EmployeeData.csv"), unsafe_allow_html=True)
    st.success("Time entries downloaded successfully.")

# Streamlit app title and login form
st.title('Techeze Time Management System')
st.header('Welcome back!')

tab1, tab2 = st.columns([1, 3])

with tab1:
    with st.form(key='login'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        login = st.form_submit_button("Login")

with tab2:
    if login:
        if not username or not password:
            st.warning("Please enter both Username and Password.")
        elif username == "admin" and password == "secret":
            st.success(f"User: {username} logged in successfully.")
            admin()
        elif username == "employee" and password == "techeze":
            st.success(f"User: {username} logged in successfully.")
            employ()
        else:
            st.error("Invalid Credentials. Please try again.")
    else:
        st.info('Please log in to access the dashboard.')

