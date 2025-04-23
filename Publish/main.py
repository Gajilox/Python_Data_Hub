import requests
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# OAuth2 credentials
CLIENT_ID = "b94f8e82-9f22-426d-899f-d80fa9593cff"
CLIENT_SECRET = "otN~-73o8mh3pQZ3XVmO.4Ci-~"

# Base URL for the API
BASE_URL = "https://192.168.1.109/u-os-hub/api/v1/providers"

# OAuth2 token endpoint
TOKEN_URL = "https://192.168.1.109/oauth2/token"  # Replace with the actual token endpoint

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

def write_variable(provider_id, variables, access_token):
    """
    Sends a POST request to update the specified variables.
    """
    # Construct the full URL dynamically
    url = f"{BASE_URL}/{provider_id}/variables"
    
    try:
        # Include the access token in the Authorization header
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
        
        # Send the POST request with the payload (disable SSL verification)
        response = requests.post(url, json=variables, headers=headers, verify=False)
        
        # Raise an exception if the request fails (e.g., 4xx or 5xx status code)
        response.raise_for_status()
        
        # Print the server response
        print("Variable write command was successfully sent.")
        print(f"Server response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error writing variables: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")

def main():
    # Obtain the access token
    access_token = get_access_token()
    
    # Exit if no access token is obtained
    if not access_token:
        print("Failed to obtain access token. Exiting...")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Write variables")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            # Get user inputs
            provider_id = input("Enter the provider ID (e.g., u_os_sbm): ")
            num_variables = int(input("How many variables do you want to update? "))
            
            variables = []
            for i in range(num_variables):
                key = input(f"Enter the key for variable #{i+1}: ")
                value = input(f"Enter the value for variable #{i+1} (True/False or numeric): ")
                
                # Convert value to boolean or numeric type if possible
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                
                variables.append({"key": key, "value": value})
            
            # Write the variables
            write_variable(provider_id, variables, access_token)
        
        elif choice == "2":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()