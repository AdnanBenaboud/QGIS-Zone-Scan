@echo off
REM Set OSGeo4W root path
SET OSGEO4W_ROOT=C:\OSGeo4W64
SET QGISNAME=qgis
SET QGIS=%OSGEO4W_ROOT%pps\%QGISNAME%

REM QGIS setup
SET QGIS_PREFIX_PATH=%QGIS%
SET GDAL_DATA=%OSGEO4W_ROOT%\share\gdal

REM Python setup
SET PATH=%OSGEO4W_ROOT%in;%QGIS%in;%PATH%

REM Run Python job
python "C:/Users/dell/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QGIS-Zone-Scan/jobs\download_job_2025_06_01T22_56_29Z_2026_06_29T22_56_29Z_minutes_1_20.py"

    