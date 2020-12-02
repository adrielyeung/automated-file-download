# automated-file-download
Automates downloading of files from web page with authentication using Python Selenium, with a Chrome driver, taking in year and month as input parameters.

All config (URL, username and password) are stored in file named ```Credentials.csv```. Structure of the file is uploaded. ```Pandas``` package is used to access the CSV file.

This helps to save a lot of time in manual operation if the downloading is done on a regular basis.

The ```FileDownload_Automation.py``` file contains the script which could be run to download files automatically. Some modifications are required:

1. Set default download path at ```download_path = '<default_download_path>'```
2. Set Chrome driver path at ```DRIVER_PATH = '<driver_path>'```
3. The HTML elements in ```find_element_by_xpath``` needs to be adapted to each website scraped. Please use the Developer tools of Chrome to search for the XPath of the required element.
