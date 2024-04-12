import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import geocoder
import plotly.express as px

#an empty DataFrame to store employee data
EMPLOYEE_DATA = pd.DataFrame(columns=['Employee ID', 'Check-in Time', 'Check-out Time'])

#employ functionalites
def employ():
    st.subheader("Employee Dashboard")
    current_location = location() 
    if current_location[0]== 12.954893 or current_location[1] == 80.24415:
  
        with st.form(key='employeeForm'):
            eid = st.text_input('Enter your Employee ID:')
            submitButton = st.form_submit_button('Submit')
            st.write('Form submitted:', submitButton)
            
        if current_location:
            st.write("Latitude:", current_location[0])
            st.write("Longitude:", current_location[1])
        if submitButton:
            st.write('Form submitted:', submitButton)
            check_in_button = st.button('Check-in')
            check_out_button = st.button('Check-out')
            st.write('Check-in button clicked:', check_in_button)
            st.write('Check-out button clicked:', check_out_button)
            if eid and (check_in_button or check_out_button):
                check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if check_in_button:
                    row = {'Employee ID': eid, 'Check-in Time': check_time, 'Check-out Time': ''}
                else:
                    row = EMPLOYEE_DATA[(EMPLOYEE_DATA['Employee ID'] == eid) & (EMPLOYEE_DATA['Check-out Time'] == '')]
                    if not row.empty:
                        EMPLOYEE_DATA.loc[row.index[0], 'Check-out Time'] = check_time
                        st.success('Checked out successfully.')
                    else:
                        st.error('You need to check-in first.')
                        return

                EMPLOYEE_DATA.loc[len(EMPLOYEE_DATA)] = row
                if check_in_button:
                    st.success('Checked in successfully.')
    else:
        st.error('Please enter into company permises to mark attendance')
    return EMPLOYEE_DATA


#12.954893215209236, 80.24415236932002 techeze latitude and longitude
def location():
    #fetching user current location using ipinfo

    location = geocoder.ip('me').latlng
    
    if location:
        latitude, longitude = location[0], location[1]
        st.info(f"Current Location: Latitude {latitude} , Longitude {longitude}")
        fig = px.scatter_mapbox(
        data_frame=None,
        lat=[latitude],
        lon=[longitude],
        zoom=12
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        # Display the plot
        st.plotly_chart(fig)

        
        return latitude, longitude
    else:
        st.error("Failed to fetch current location.")
        

#admin functions
def admin():
    st.subheader("Admin Functionalities")
    def download_link(df, filename):
        """Generates a link to download dataframe."""
        csv = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode('utf-8')
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download</a>'

    button = """Click on 'Download Data' Button below to get all the data in CSV format"""
    st.markdown(button, unsafe_allow_html=True)
    st.markdown(download_link(EMPLOYEE_DATA, "EmployeeData.csv"), unsafe_allow_html=True)
    st.success("Time entries downloaded successfully.")

st.title('Techeze Time management system')
st.header('Welcome back!')
tab1, tab2 = st.columns([1, 3])

#frontend
with tab1:
    with st.form(key='login'):
        username = st.text_input("Username")
        password = st.text_input("Password", value="", type='password')
        login = st.form_submit_button("Login")
    #print(username, password)
with tab2:
    if login:
        if not username or not password:
            st.warning("Please enter both Username and Password.")
        elif username == "admin" and password == "secret":
            with tab1:
                st.success(f" User: {username} Logged in successfully.")
            admin()
        elif username == "employee" and password == "techeze":
            with tab1:
                st.success(f" User: {username} Logged in successfully.")
            employ()
        else:
            st.error("Invalid Credentials. Please try again.")
        
    else:
        st.info('Please Login to access the dashboard.')
