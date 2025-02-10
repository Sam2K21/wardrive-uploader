# Wigle Wardrive Uploader ![icon](https://github.com/user-attachments/assets/7c1f720b-185c-4602-9b19-adf15737724f)

This is a Python script to allow for easy upload of wardrive data through Wigle's API using a GUI.

The script creates a file named "uploaded_files.txt" to track previously uploaded logs and "upload_log.txt" to log more detailed information about your uploads.

Accepts .log, .csv, .wiglecsv, and .kml files

How to use:

In your console from the script directory run "pip install -r requirements.txt"

1. Before running make sure to input your Wigle API info on lines 16 & 17.
   
   Line 16 variable labeled WIGLE_API_USER should be set to your API Name from your Wigle account.
   Line 17 variable labeled WIGLE_API_TOKEN should be set to your API Token from your Wigle account.

2. Make sure your SD card drive letter is correct in line 20.
   
   Line 20 variable labeled WATCH_DIRECTORY should be set to your SD card drive letter (e.g. G:\\)


