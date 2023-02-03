##### QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
import pandas as pd
from gsheetsdb import connect
import io
import webbrowser
from streamlit_qrcode_scanner import qrcode_scanner
import qrcode
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import service_account




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



### Function: write_to_gsheet = Perform writing SQL query on the Google Sheet
def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1
    
    
    
    
#### Main program
### Synchronous local storage
## Main call to the api, returns a communication object
#conn = injectWebsocketCode(hostPort = 'linode.liquidco.in', uid = getOrCreateUID())

# Set local variables
#st.write('setting into localStorage')
#ret = conn.setLocalStorageVal(key = 'k1', val = 'v1')
#st.write('return: ' + ret)

# Get local variables
#st.write('getting from localStorage')
#ret = conn.getLocalStorageVal(key = 'k1')
#st.write('return: ' + ret)

## Google Sheet
# Create a connection object.
conn_google = connect()

# Execute query
url = st.secrets['google']['url']
rows = goolge_query(f'SELECT * FROM "{url}"')
#rows = goolge_query(f'INSERT INTO "{url}"(name, workshop) VALUES ("Test", "Testing")')

# Print results.
for row in rows:
    st.write(row[0] + ' attends ' + row[1])
    

## Write to Google Sheet
data_df = pd.DataFrame(columns = ['name', 'workshop'])
df = pd.DataFrame([['Test', 'Tester']], columns = ['name', 'workshop'])
data_df = pd.concat([data_df, df])
#write_to_gsheet('orbital-anchor-376709-11c4a700451c.json', st.secrets['google']['spreadsheet_id'], 'QRCodeReader', data_df)
#credentials = service_account.Credentials.from_service_account_file(st.secrets['google']['credentials_file'])
credentials = service_account.ServiceAccountCredentials("qr-code-scanner-api@orbital-anchor-376709.iam.gserviceaccount.com", "108132249049824277061")
scoped_credentials = Credentials.from_authorized_user_file('google_credentials.json', 'https://www.googleapis.com/auth/spreadsheets.readonly')
#scoped_credentials = Credentials.with_scopes(['https://www.googleapis.com/auth/sqlservice.admin'])
# 'https://www.googleapis.com/auth/sqlservice.admin'
# 'https://www.googleapis.com/auth/spreadsheets.readonly'
# 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'

gc = gspread.Client(auth = scoped_credentials)
gc.session = AuthorizedSession(scoped_credentials)
sheet = gc.open_by_key(st.secrets['google']['spreadsheet_id'])
st.write(sheet.title)

    
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
