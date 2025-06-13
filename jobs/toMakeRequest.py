from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# Your client credentials
client_id = 'sh-fe6c2430-e6d5-4e1d-b929-856798c5d2ad'
client_secret = 'ZeZVlTvJrEon65OnvPnaRGiFJ727V3Lu'



class SentinelDownloader:
    def __init__(self, client_id, client_secret, base_dir = "./data/"):   
        self.client_id = client_id
        self.client_secret = client_secret 

        # Create a session
        self.client = BackendApplicationClient(client_id=self.client_id)
        self.oauth = OAuth2Session(client=self.client)

        # Get token for the session
        self.token = self.oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                                client_secret=client_secret, include_client_id=True)
        
        self.url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        self.base_dir = base_dir


    def get_rgb(self, filename,time_start="2022-10-01T00:00:00Z",time_end="2022-10-31T00:00:00Z",cloud_coverage=20, size=(512, 512)):
        # The token can be used to make authenticated requests
        evalscript_RGB = """
        //VERSION=3
        function setup() {
        return {
            input: ["B02", "B03", "B04"],
            output: { bands: 3 },
        }
        }

        function evaluatePixel(sample) {
        return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
        }
        """


        request = {
            "input": {
                "bounds": {
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                    "bbox": [-5.981232, 35.586745, -5.647522, 35.812022],  
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": time_start,
                                "to": time_end,
                            },
                            "maxCloudCoverage": cloud_coverage,
                        },
                        "processing": {"harmonizeValues": "false"},
                    }
                ],
            },
            "output": {
                "width": size[0],
                "height": size[1],
                "responses": [
                    {
                        "identifier": "default",
                        "format": {"type": "image/tiff"},
                    }
                ],
            },
            "evalscript": evalscript_RGB,
        }


        response = self.oauth.post(self.url, json=request, headers={"Accept": "image/tiff"})
        print("Response code of the request is:",  response.status_code)
        with open(os.path.join(self.base_dir, filename), "wb") as f:
            f.write(response.content)
        print("Image saved to %s" % os.path.join(self.base_dir, filename))




    def get_raw(self, filename, time_start="2022-10-01T00:00:00Z",time_end="2022-10-31T00:00:00Z", cloud_coverage=20, size=(512, 512)):
        evalscript = """
        //VERSION=3
        function setup() {
        return {
            input: [
            {
                bands: [
                "B01",
                "B02",
                "B03",
                "B04",
                "B05",
                "B06",
                "B07",
                "B08",
                "B8A",
                "B09",
                "B11",
                "B12",
                ],
                units: "DN",
            },
            ],
            output: {
            id: "default",
            bands: 12,
            sampleType: SampleType.UINT16,
            },
        }
        }

        function evaluatePixel(sample) {
        return [
            sample.B01,
            sample.B02,
            sample.B03,
            sample.B04,
            sample.B05,
            sample.B06,
            sample.B07,
            sample.B08,
            sample.B8A,
            sample.B09,
            sample.B11,
            sample.B12,
        ]
        }
        """

        request = {
            "input": {
                "bounds": {
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                    "bbox": [-5.981232, 35.586745, -5.647522, 35.812022],  
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": time_start,
                                "to": time_end,
                            },
                            "maxCloudCoverage": cloud_coverage,
                        },
                        "processing": {"harmonizeValues": "false"},
                    }
                ],
            },
            "output": {
                "width": size[0],
                "height": size[1],
                "responses": [
                    {
                        "identifier": "default",
                        "format": {"type": "image/tiff"},
                    }
                ],
            },
            "evalscript": evalscript,
        }

        response = self.oauth.post(self.url, json=request)
        print("Response code of the request is:",  response.status_code)
        with open( os.path.join(self.base_dir, filename), "wb") as f:
            f.write(response.content)
        print("Image saved to %s" % os.path.join(self.base_dir, filename))


    def get_ndvi(self, filename, time_start="2022-10-01T00:00:00Z",time_end="2022-10-31T00:00:00Z",cloud_coverage=20, size=(512, 512)):
        # The token can be used to make authenticated requests
        evalscript = """
        //VERSION=3
        function setup() {
        return {
            input: [
            {
                bands: ["B04", "B08"],
                units: "REFLECTANCE",
            },
            ],
            output: {
            id: "default",
            bands: 1,
            sampleType: SampleType.FLOAT32,
            },
        }
        }

        function evaluatePixel(sample) {
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)
        return [ndvi]
        }
        """

        request = {
            "input": {
                "bounds": {
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                    "bbox": [-5.981232, 35.586745, -5.647522, 35.812022],  
                    
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": time_start,
                                "to": time_end,
                            },
                            "maxCloudCoverage": cloud_coverage,
                        },
                        "processing": {"harmonizeValues": "true"},
                    }
                ],
            },
            "output": {
                "width": 512,
                "height": 512,
                "responses": [
                    {
                        "identifier": "default",
                        "format": {"type": "image/tiff"},
                    }
                ],
            },
            "evalscript": evalscript,
        }

        response = self.oauth.post(self.url, json=request)

        print("Response code of the request is:",  response.status_code)
        with open( os.path.join(self.base_dir, filename), "wb") as f:
            f.write(response.content)
        print("Image saved to %s" % os.path.join(self.base_dir, filename))


def get_frequency_delta(unit, value):
    if unit == "years":
        return relativedelta(years=value)
    elif unit == "months":
        return relativedelta(months=value)
    elif unit == "weeks":
        return timedelta(weeks=value)
    elif unit == "days":
        return timedelta(days=value)
    elif unit == "hours":
        return timedelta(hours=value)
    elif unit == "minutes":
        return timedelta(minutes=value)
    elif unit == "secondes":
        return timedelta(seconds=value)
    else:
        raise ValueError("Invalid frequency unit")
    
def generate_jobs(start, end, step):
    current = start
    jobs = []
    while current < end:
        next_time = current + step
        if next_time > end:
            next_time = end
        jobs.append((current.isoformat(), next_time.isoformat()))
        current = next_time
    return jobs

def get_time_ranges(start, end, unit, value):
    step = get_frequency_delta(unit, value)
    return generate_jobs(start, end, step)


if __name__ == "__main__":
    SD = SentinelDownloader(client_id, client_secret)
    time_start = "2024-01-01T00:00:00Z"
    time_end = "2024-02-01T00:00:00Z"
    SD.get_rgb("RGB.tiff", time_start, time_end, cloud_coverage=10,size=(1024, 1024))
    SD.get_raw("Raw.tiff")
    SD.get_ndvi("NDVI.tiff")