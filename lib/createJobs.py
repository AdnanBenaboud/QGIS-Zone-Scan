import subprocess
import sys
import datetime


def parse_local_datetime(utc_string):
    dt = datetime.datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%SZ")
    local_dt = dt.astimezone()
    date_str = local_dt.strftime("%m/%d/%Y") 
    time_str = local_dt.strftime("%H:%M")  
    return date_str, time_str

def get_schedule(unit, value):
    unit = unit.lower()
    if unit == "minutes":
        if not (1 <= value <= 1439):
            raise ValueError("For MINUTE, MO must be 1 to 1439")
        return "MINUTE", value
    elif unit == "hours":
        if not (1 <= value <= 23):
            raise ValueError("For HOURLY, MO must be 1 to 23")
        return "HOURLY", value
    elif unit == "days":
        if not (1 <= value <= 365):
            raise ValueError("For DAILY, MO must be 1 to 365")
        return "DAILY", value
    elif unit == "weeks":
        total_days = 7 * value
        if not (1 <= total_days <= 365):
            raise ValueError("Weekly equivalent in days must be 1 to 365")
        return "DAILY", total_days
    elif unit == "months":
        total_days = 30 * value
        if not (1 <= total_days <= 365):
            raise ValueError("Monthly equivalent in days must be 1 to 365")
        return "DAILY", total_days
    else:
        raise ValueError(f"Unsupported schedule unit: {unit}")

    

def create_windows_task(task_name, time_str,time_end, bat_path, unit, value):
    unit = unit.lower()


    sc, mo = get_schedule(unit, value)
    
    start_date_str, start_time_str = parse_local_datetime(time_str)
    end_date_str, end_time_str = parse_local_datetime(time_end)

    cmd = [
        
        "schtasks",
        "/Create",
        "/SC", str(sc),
        "/MO", str(mo),
        "/TN", task_name,
        "/TR", f'wscript.exe {bat_path}',
        "/ST", start_time_str,
        "/SD", start_date_str,
        "/ED", end_date_str,
        "/F"
    ]
    print("Command to run: " + " ".join(cmd))
    subprocess.run(cmd, shell=True)
    print("Task created successfully.")





def write_download_script(job_id, client_id, client_secret, cloud_cov, out_dir, options):
    script = f"""import sys
from toMakeRequest import SentinelDownloader
import datetime



# Get today's date
today = datetime.date.today()
# make it ISO format
start_date = today.isoformat()
start_date = start_date + "T00:00:00Z"
end_date = (start_date.split("T")[0]) + "T23:55:28Z"

print(start_date)
print(end_date)


options = {options}

downloader = SentinelDownloader("{client_id}", "{client_secret}")
downloader.base_dir = r"{out_dir}"
name = "{job_id}"
name = name+"_"+datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")
if 'rgb' in options:
    downloader.get_rgb(f"rgb_{{name}}.tiff", start_date, end_date, {cloud_cov}, (512, 512))
if 'raw' in options:
    downloader.get_raw(f"raw_{{name}}.tiff", start_date, end_date, {cloud_cov}, (512, 512))
if 'ndvi' in options:
    downloader.get_ndvi(f"ndvi_{{name}}.tiff", start_date, end_date, {cloud_cov}, (512, 512))

"""
    filename = f"C:/Users/dell/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QGIS-Zone-Scan/jobs/download_job_{job_id}.py"
    with open(filename, "w") as f:
        f.write(script)

    # add bat file
    script_bat = f"""@echo off
REM Set OSGeo4W root path
SET OSGEO4W_ROOT=C:\OSGeo4W64
SET QGISNAME=qgis
SET QGIS=%OSGEO4W_ROOT%\apps\%QGISNAME%

REM QGIS setup
SET QGIS_PREFIX_PATH=%QGIS%
SET GDAL_DATA=%OSGEO4W_ROOT%\share\gdal

REM Python setup
SET PATH=%OSGEO4W_ROOT%\bin;%QGIS%\bin;%PATH%

REM Run Python job
python "{filename}"

    """
    filename_bat = f"C:/Users/dell/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QGIS-Zone-Scan/jobs/download_job_{job_id}.bat"
    with open(filename_bat, "w") as f:
        f.write(script_bat)

    # VBS script
    script_vbs = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:/Users/dell/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QGIS-Zone-Scan/jobs/download_job_{job_id}.bat", 1, True
    """

    filename_vbs = f"C:/Users/dell/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QGIS-Zone-Scan/jobs/download_job_{job_id}.vbs"
    with open(filename_vbs, "w") as f:
        f.write(script_vbs)

    return filename
