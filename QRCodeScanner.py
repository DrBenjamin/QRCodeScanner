##### QRCodeScanner.py`
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
import io
import webbrowser
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
 
 
 
### Function: google_query = Perform SQL query on the Google Sheet
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl = 600)
def goolge_query(query):
    rows = conn_google.execute(query, headers = 1)
    rows = rows.fetchall()
    return rows
    


    
#### Main program
st.write('Python ' + platform.python_version() + ' and Streamlit ' + st.__version__)
### Synchronous local storage
## Main call to the api, returns a communication object
conn = injectWebsocketCode(hostPort = 'linode.liquidco.in', uid = getOrCreateUID())

# Set local variables
st.write('setting into localStorage')
ret = conn.setLocalStorageVal(key = 'k1', val = 'v1')
st.write('return: ' + ret)

# Get local variables
st.write('getting from localStorage')
ret = conn.getLocalStorageVal(key = 'k1')
st.write('return: ' + ret)
    

## Google Sheet
data_df = pd.DataFrame(columns = ['name', 'workshop'])
df = pd.DataFrame([['Test', 'Tester']], columns = ['name', 'workshop'])
data_df = pd.concat([data_df, df])
data_list = [['Ben', 'Python programming'], ['Benja', 'Python lecturing']]

client = pygsheets.authorize(service_file='google_credentials.json')

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
