##### `#️⃣_QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
import platform
import pandas as pd
import pygsheets
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
    


    
#### Main program
## Google Sheet support
with st.expander(label = 'Google Sheet support', expanded = False):
	st.write('Python ' + platform.python_version() + ' and Streamlit ' + st.__version__)
	st.write(st.secrets['google']['url'])
	data_list = [['Benjamin', 'Python programming'], ['Stefan', 'Projectmanagement'], ['Thoko', 'Leadership'], ['Hope', 'PHP programming'], ['Nick', 'Java programming']]
	
	client = pygsheets.authorize(service_file = 'google_credentials.json')
	
	# Open the spreadsheet and the first sheet
	sh = client.open_by_key(st.secrets['google']['spreadsheet_id'])
	
	wks = sh.sheet1
	
	# Read Sheet
	data = wks.get_as_df()
	st.write(data)
	
	# Update a single cell.
	wks.update_value('A1', "name")
	
	# Update the worksheet with the numpy array values. Beginning at cell 'A2'.
	wks.update_values('A2', data_list)
	

	## Synchronious local storage## Main call to the api, returns a communication object
	#conn = injectWebsocketCode(hostPort = 'linode.liquidco.in', uid = getOrCreateUID())

	# Set local variables
	#st.write('setting into localStorage')
	#ret = conn.setLocalStorageVal(key = 'k1', val = 'v1')
	#st.write('return: ' + ret)
	
	# Get local variables
	#st.write('getting from localStorage')
	#ret = conn.getLocalStorageVal(key = 'k1')
	#st.write('return: ' + ret)
	
    
## Selectbox as menu
option = st.radio(label = "CHOOSE MODE 👇", options = ["QR Code Scanner", "QR Code Generator"], index = 1, key = "mode", label_visibility = 'visible', disabled = False, horizontal = True)


## QR Code scanner (https needed)
if option == 'QR Code Scanner':
  st.subheader('QR Code Scanner')

  qrcode = qrcode_scanner(key = 'qrcode_scanner')
  if qrcode != None:
    webbrowser.open(qrcode)
      
      
## QR Code generator
elif option == 'QR Code Generator':
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
