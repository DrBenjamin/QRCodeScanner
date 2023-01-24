 ##### QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import webbrowser
from streamlit_qrcode_scanner import qrcode_scanner  




#### Streamlit initial setup
st.set_page_config(
  page_title = "QR Code Scanner",
  page_icon = "QRCode.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': st.secrets['custom']['menu_items_help'],
         'Report a bug': st.secrets['custom']['menu_items_bug'],
         'About': st.secrets['custom']['menu_items_about']
        }
) 




#### Initialization of session states
## QR Code session state
if ('qrcode' not in st.session_state):
  st.session_state['qrcode'] = False




#### Main program
## QR Code scanner (https needed)
with st.expander('QR Code scanner', expanded = False):
  st.subheader('QR Code scanner')
  if st.button('Scan QR Code?'):
    st.session_state['qrcode'] = True  
    
  if st.session_state['qrcode'] == True:
    qrcode = qrcode_scanner(key = 'qrcode_scanner')
    print(qrcode)
    if qrcode != None:
      webbrowser.open(qrcode)
      st.session_state['qrcode'] = False
      qrcode = None
      st.experimental_rerun()
