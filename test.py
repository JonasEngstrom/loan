import json
from urllib import request, error

# Base URL and endpoint
base_url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/PR/PR0101/PR0101A/KPItotM"

# JSON body equivalent to the R code
json_body = {
    "query": [
        {
            "code": "ContentsCode",
            "selection": {"filter": "item", "values": ["000004VU"]},
        }
    ],
    "response": {"format": "json"},
}

# Convert the body to a JSON-encoded string
json_data = json.dumps(json_body).encode("utf-8")

# Create the request
req = request.Request(
    base_url, data=json_data, headers={"Content-Type": "application/json"}
)

try:
    # Perform the request
    with request.urlopen(req) as response:
        # Read and decode the response
        response_data = response.read().decode("utf-8")
        # Parse JSON response
        parsed_response = json.loads(response_data)
        print(parsed_response)

except error.HTTPError as e:
    # Handle HTTP errors
    print(f"HTTPError: {e.code}, {e.reason}, {e.read().decode('utf-8')}")
except error.URLError as e:
    # Handle URL errors
    print(f"URLError: {e.reason}")
