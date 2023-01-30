 ##### QRCodeScanner.py`
##### QR Code Scanner for HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/QRCodeScanner
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import io
import webbrowser
from streamlit_qrcode_scanner import qrcode_scanner
import qrcode




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
