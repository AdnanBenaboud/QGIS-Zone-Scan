import sys

try:
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
except Exception:

    print("Installing the modules we neeed: oauthlib and requests_oauthlib..")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "oauthlib", "requests_oauthlib"])
    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session

    
from toMakeRequest import SentinelDownloader
import datetime



today = datetime.date.today()

start_date = (today - datetime.timedelta(weeks=2)).isoformat() + "T00:00:00Z"
end_date   = today.isoformat() + "T23:59:59Z"

print("Starting to download the new images... ")
print(start_date)
print(end_date)


options = ['rgb']

downloader = SentinelDownloader("sh-fe6c2430-e6d5-4e1d-b929-856798c5d2ad", "ZeZVlTvJrEon65OnvPnaRGiFJ727V3Lu")
downloader.base_dir = r"C:\Users\dell\Pictures"
name = "2025_06_01T22_56_29Z_2026_06_29T22_56_29Z_minutes_1_20"
name = name+"_"+datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")
if 'rgb' in options:
    downloader.get_rgb(f"rgb_{name}.tiff", start_date, end_date, 20, (512, 512))
if 'raw' in options:
    downloader.get_raw(f"raw_{name}.tiff", start_date, end_date, 20, (512, 512))
if 'ndvi' in options:
    downloader.get_ndvi(f"ndvi_{name}.tiff", start_date, end_date, 20, (512, 512))

