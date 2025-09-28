searchcars_url = os.getenv(
    'searchcars_url',
    default="http://localhost:3050/")

def searchcars_request(endpoint, **kwargs):
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params+key + "=" + value + "&"

    request_url = searchcars_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")
    finally:
        print("GET request call complete!")