import requests
import urllib3
import time

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# OAuth2 credentials
CLIENT_ID = "b94f8e82-9f22-426d-899f-d80fa9593cff"
CLIENT_SECRET = "otN~-73o8mh3pQZ3XVmO.4Ci-~"

# Base URL for the API
BASE_URL = "https://192.168.1.109/u-os-hub/api/v1/providers/u_os_sbm/variables"

# OAuth2 token endpoint
TOKEN_URL = "https://192.168.1.109/oauth2/token"  # Replace with the actual token endpoint

# List of variable IDs
VARIABLE_IDS = [
    "ur20_16di_p_1.process_data.channel_0.di",
    "ur20_16di_p_1.process_data.channel_1.di",
    "ur20_16di_p_1.process_data.channel_2.di",
    "ur20_16di_p_1.process_data.channel_3.di"
]

def get_access_token():
    """
    Sends a POST request to the OAuth2 token endpoint to obtain an access token.
    Uses client_secret_basic authentication.
    """
    try:
        # Prepare the payload for the token request
        payload = {
            "grant_type": "client_credentials"
        }

        # Encode the client_id and client_secret for Basic Authentication
        auth = (CLIENT_ID, CLIENT_SECRET)

        # Send the POST request to obtain the token (disable SSL verification)
        response = requests.post(TOKEN_URL, data=payload, auth=auth, verify=False)
        
        # Raise an exception if the request fails (e.g., 4xx or 5xx status code)
        response.raise_for_status()
        
        # Parse the JSON response and extract the access token
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise ValueError("Access token not found in the response.")
        
        print("Access token obtained successfully.")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining access token: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")
        return None

def fetch_data(variable_id, access_token):
    """
    Sends a GET request for the specified variable ID using the access token.
    """
    # Construct the full URL dynamically
    url = f"{BASE_URL}/{variable_id}"
    
    try:
        # Include the access token in the Authorization header
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Send the GET request (disable SSL verification)
        response = requests.get(url, headers=headers, verify=False)
        
        # Raise an exception if the request fails (e.g., 4xx or 5xx status code)
        response.raise_for_status()
        
        # Print the response content
        print(f"Response received for variable_id={variable_id}:")
        print(response.json())  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error fetching data for variable_id={variable_id}: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")

if __name__ == "__main__":
    # Obtain the access token
    access_token = get_access_token()
    
    # Exit if no access token is obtained
    if not access_token:
        print("Failed to obtain access token. Exiting...")
        exit(1)
    
    # Initialize a counter for tracking iterations
    request_counter = 0
    
    while True:
        # Increment the counter at the start of each iteration
        request_counter += 1
        
        # Print the current iteration count
        print(f"Fetching data for all variables... (Iteration #{request_counter})")
        
        # Fetch and print the data for each variable
        for variable_id in VARIABLE_IDS:
            fetch_data(variable_id, access_token)
        
        # Wait for 10 seconds before the next cycle
        print("Waiting for 10 seconds before the next cycle...\n")
        time.sleep(10)