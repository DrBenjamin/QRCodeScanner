# QRCodeScanner

[![GitHub][github_badge]][github_link]

## QR Code Scanner

This App handles the QR Codes created by the **EasyBadge ID Card Printer Software**. For development **[RStudio](https://www.rstudio.com/products/rstudio/download/#download)** is used. Install **[git](https://git-scm.com/download/win)** to use version control.

### Setup

Description of the installation and configuration to use the **QR Code Scanner**.

#### Installation and configuration of all needed Software

All Software which is used to run **QR Code Scaner** is **Open Source**. Please be aware of different licenses with varying policies.

##### Installation of Python, Streamlit and dependencies

Install **[Streamlit & Python](https://docs.streamlit.io/library/get-started/installation)** to run the source code locally. A virtual Python environment like **Anaconda** / **Miniconda** is highly recommend.

After that you need to install some *Python libraries*. To do so use the `requirements.txt` file with:

```cmd
pip install -r requirements.txt
```

#### Getting the QR Code Scanner source code

Clone the *repository* of **QRCodeScanner** with following command:

```cmd
git clone https://github.com/DrBenjamin/QRCodeScanner.git
```

##### Configuration of Streamlit config files

First make a directory `.streamlit`. After that create the file `.streamlit/config.toml`. Here you define the *theming* and some *Streamlit server behaviour* flags:

```python
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
```

Now create the file `.streamlit/secrets.toml` where you define some hidden configuration. Define the Google Sheets API settings:

```python
[google]
url = "" # URL to the Google spreadsheet
spreadsheet_id = "" # ID of the Google spreadsheet for workshop data
pin_spreadsheet_id = "" # ID of the Google spreadsheet for Emp. No. - PIN checking
credentials_file = "" # File name of the JSON document with Service Account
credentials_file_id = "" # ID of the Google spreadsheet for workshop data
```

##### Execute Streamlit

If you've installed all dependencies, configured the MySQL server and edited the Streamlit app config files (`config.toml` / `secrets.toml`) to your setup, you can run the app locally within the *Terminal* of RStudio or any other terminal with access to Python and the Python libraries (e.g. a virtual environment) with this command:

```cmd
streamlit run QRCodeScanner.py
```

This will open the **Web App** on the servers IP address(es) and the designated port.

#### Update Streamlit & dependencies

The Software and its dependencies will be updated regularly, so make sure to always run the newest versions to avoid security risks.

##### Update of Streamlit

To update to the latest version of the **Streamlit web app framework**, run the following command:

```cmd
pip install --upgrade streamlit
```

##### Update dependencies

To update all dependencies, use this command:

```cmd
pip install --upgrade -r requirements.txt
```

### Demo

[![Open in Streamlit Cloud][share_badge]][share_link]

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/DrBenjamin/QRCodeScanner

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://qrcodescanner.streamlit.app/
