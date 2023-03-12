##### `#️⃣_QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import io
import os
import shutil
import platform
import pandas as pd
import numpy as np
import pygsheets
from google_drive_downloader import GoogleDriveDownloader
from streamlit_qrcode_scanner import qrcode_scanner
import qrcode
from datetime import date




#### Streamlit initial setup
st.set_page_config(
    page_title = "QR Code Scanner",
    page_icon = "images/QRCode.png",
    layout = "centered",
    initial_sidebar_state = "expanded",
)




#### Initialization of session states
## QR Code session state
if ('qrcode' not in st.session_state):
    st.session_state['qrcode'] = False




#### Functions
### parse_national_id = Parsing National ID QR Code data to list
def parse_national_id(text):
    val = text.split('~')
    if len(val) == 12:
        if len(val[6].split(', ')) > 1:
            fname, mname = val[6].split(', ')
        else:
            fname = val[6]
            mname = ''
        lname = val[4]
        gender = str(val[8]).upper()
        raw_dob = val[9]
        nat_id = str(val[5])
        
        # Cleaning data format
        dateOfBirth = str(raw_dob).split(" ")
        day = dateOfBirth[0]
        year = dateOfBirth[2]
        month = dateOfBirth[1]
        month_var = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}
        num_month = month_var[month.upper()]
        birth_date = date(int(year), num_month, int(day))
        print_dob = day + "-" + month + "-" + year
        result = {"first_name": fname, "middle_name": mname, "last_name": lname, "gender": gender, "nation_id": nat_id, "dob": birth_date,
                  "printable_dob": print_dob}
        
        # Return result
        return result



### Function: generate_qrcode = QR Code generator
def generate_qrcode(data):
    # Encoding data using make() function
    image = qrcode.make(data)
    
    # Saving image as png in a buffer
    byteIO = io.BytesIO()
    image.save(byteIO, format = 'PNG')
    
    # Return qrcode
    return byteIO.getvalue()



### Function: load_data = Loading Google Sheet API credentials (non permanent)
def download_data():
    output = st.secrets['google']['credentials_file']
    gdd.download_file_from_google_drive(file_id = st.secrets['google']['credentials_file_id'], dest_path = './credentials.zip', unzip = True)



### Function: google_sheet_credentials = Getting Google Sheet API credentials
@st.experimental_singleton
def google_sheet_credentials():
    ## Google Sheet API authorization
    output = st.secrets['google']['credentials_file']
    GoogleDriveDownloader.download_file_from_google_drive(file_id = st.secrets['google']['credentials_file_id'], dest_path = './credentials.zip',
                                                          unzip = True)
    client = pygsheets.authorize(service_file = st.secrets['google']['credentials_file'])
    if os.path.exists("credentials.zip"):
        os.remove("credentials.zip")
    if os.path.exists("google_credentials.json"):
        os.remove("google_credentials.json")
    if os.path.exists("__MACOSX"):
        shutil.rmtree("__MACOSX")
    
    # Return client
    return client




#### Main program
### Google Sheet support
## Open the spreadsheet and the first sheet
# Getting credentials
client = google_sheet_credentials()

# Opening sheet
sh = client.open_by_key(st.secrets['google']['pin_spreadsheet_id'])
wks = sh.sheet1

## Read worksheet
pin_data = wks.get_as_df()
pin_data = pin_data.set_index('ID')



### Selectbox as menu
option = st.radio(label = "CHOOSE MODE 👇", options = ["Workshop", "Labor", "Secure Access", "Identify"], index = 3, key = "mode",
                  label_visibility = 'visible', disabled = False, horizontal = True)



### Workshop QR Code scanner
if option == 'Workshop':
    st.subheader('QR Code Scanner for Workshops')
    
    qrcode = qrcode_scanner(key = 'qrcode_scanner')
    if qrcode != None:
        text = parse_national_id(qrcode)
        st.write(text)
        # webbrowser.open(qrcode)


## Labor QR Code scanner
elif option == 'Labor':
    st.subheader('QR Code Scanner for Labor')
    
    qrcode = qrcode_scanner(key = 'qrcode_scanner')
    if qrcode != None:
        st.write(qrcode)
        # webbrowser.open(qrcode)



### Secure Access QR Code scanner
if option == 'Secure Access':
    st.subheader('QR Code Scanner for Secure Access')
    
    qrcode = qrcode_scanner(key = 'qrcode_scanner')
    if qrcode != None:
        st.write(qrcode)
        # webbrowser.open(qrcode)



### Identify QR Code generator
elif option == 'Identify':
    with st.form('QR Code Generator'):
        st.subheader('QR Code Generator')
        emp = st.text_input(label = 'Please enter an employee number')
        pin = st.text_input(label = 'Please enter the PIN')
        qrcode_image = None
        for i in range(len(pin_data)):
            if emp == str(pin_data.iloc[i]['Emp. No.']):
                if pin == str(pin_data.iloc[i]['PIN']):
                    qrcode_image = generate_qrcode('/?eno=' + emp + '&pin=' + pin)
                    break
        
        submitted = st.form_submit_button('Submit')
        if submitted:
            # Show QR Code
            if qrcode_image != None:
                st.image(qrcode_image)
            
            # Error message
            else:
                st.error(body = 'Wrong Emp. No. or PIN!', icon = "🚨")
