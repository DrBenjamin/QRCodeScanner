##### `#️⃣_QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
import os
import shutil
import platform
import pandas as pd
import numpy as np
import pygsheets
from google_drive_downloader import GoogleDriveDownloader as gdd
from streamlit_qrcode_scanner import qrcode_scanner
import qrcode




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

	
  
    
#### Main program
### Google Sheet support
with st.expander(label = 'Google Sheet support', expanded = False):
  ## Google Sheet API authorization
  output = st.secrets['google']['credentials_file']
  gdd.download_file_from_google_drive(file_id = st.secrets['google']['credentials_file_id'], dest_path = './credentials.zip', unzip = True)
  client = pygsheets.authorize(service_file = st.secrets['google']['credentials_file'])
  if os.path.exists("credentials.zip"):
    os.remove("credentials.zip")
  if os.path.exists("google_credentials.json"):
    os.remove("google_credentials.json")
  if os.path.exists("__MACOSX"):
    shutil.rmtree("__MACOSX")
    
    
  ## Open the spreadsheet and the first sheet
  sh = client.open_by_key(st.secrets['google']['spreadsheet_id'])
  wks = sh.sheet1
  
  
  ## Read worksheet
  data = wks.get_as_df()
  data = data.set_index('ID')
  st.write(data)
  
  
## Selectbox as menu
option = st.radio(label = "CHOOSE MODE 👇", options = ["Workshop", "Labor", "Secure Access", "Identify"], index = 1, key = "mode", label_visibility = 'visible', disabled = False, horizontal = True)


## Workshop QR Code scanner
if option == 'Workshop':
  st.subheader('QR Code Scanner for Workshops')

  qrcode = qrcode_scanner(key = 'qrcode_scanner')
  if qrcode != None:
    webbrowser.open(qrcode)
      

## Labor QR Code scanner
elif option == 'Labor':
  st.subheader('QR Code Scanner for Labor')

  qrcode = qrcode_scanner(key = 'qrcode_scanner')
  if qrcode != None:
    webbrowser.open(qrcode)      



## Secure Access QR Code scanner
if option == 'Secure Access':
  st.subheader('QR Code Scanner for Secure Access')

  qrcode = qrcode_scanner(key = 'qrcode_scanner')
  if qrcode != None:
    webbrowser.open(qrcode)
    
    
## Identify QR Code generator
elif option == 'Identify':
  st.subheader('QR Code Generator')
  url = st.text_input(label = 'Please enter an Url')
  emp =  st.text_input(label = 'Please enter an employee number')
  pin =  st.text_input(label = 'Please enter the PIN')
  if url != "":
    if url[len(url) - 1] == '/':
      url = url[:-1]
    qrcode_image = generate_qrcode(url + '/?eno=' + emp + '&pin=' + pin)
  else:
    qrcode_image = None
  if qrcode_image != None:
    st.image(qrcode_image)
