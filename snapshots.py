"""Usage:
    prog.py <storage> <svm> <volume>

Arguments:
    <storage>  Storage name
    <svm>      SVM name
    <volume>   Volume name

"""


import base64
import requests
import json
import pandas as pd
from dateutil import parser
from docopt import docopt

# Disable warnings from requests library
requests.packages.urllib3.disable_warnings()


def conv_time(time):
    """
    Convert snapshot creation_time from ISO 8601 format to a formatted string.

    Args:
        time (str): Snapshot creation time in ISO 8601 format.

    Returns:
        str: Formatted string representing the snapshot creation time.
    """
    parsed_datetime = parser.isoparse(time)

    # Format the datetime object into the desired format
    formatted_datetime_str = parsed_datetime.strftime("%a %b %d %H:%M:%S %Y")

    return formatted_datetime_str


# Function to authenticate and get headers for API requests
def get_headers(username, password):
    """
    Generate authentication headers for API requests.

    Args:
        username (str): Username for authentication.
        password (str): Password for authentication.

    Returns:
        dict: Dictionary containing the authentication headers.
    """
    userpass = f"{username}:{password}"
    encoded_u = base64.b64encode(userpass.encode()).decode()
    return {"Authorization": f"Basic {encoded_u}"}

# Function to get all snapshots and their reclaimable space for a volume
def get_snapshots(storage, svm, volume, headers):
    """
    Retrieve information about snapshots for a given volume.

    Args:
        storage (str): Storage name.
        svm (str): SVM name.
        volume (str): Volume name.
        headers (dict): Authentication headers.

    Returns:
        dict: JSON response containing information about snapshots.
    """
    url = f"https://{storage}/api/storage/volumes/{volume}/snapshots?svm.name={svm}"
    try:
        response = requests.get(url, headers=headers, verify=False)

        # Extract UUIDs of snapshots
        for i in response.json()["records"]:
            snapshots.append([i['uuid']])

        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching snapshots: {e}")
        return None
    
def get_snapshot_data(storage, uuid, headers):
    """
    Retrieve information about each snapshot, including reclaimable space.

    Args:
        storage (str): Storage name.
        uuid (str): UUID of the volume.
        headers (dict): Authentication headers.

    Returns:
        list: List containing information about each snapshot.
    """
    for i in snapshots:
        url = f"https://{storage}/api/storage/volumes/{uuid}/snapshots/{i[0]}"
        url2 = f"https://{storage}/api/storage/volumes/{uuid}/snapshots/{i[0]}?fields=reclaimable_space"

        try:
            # Fetch snapshot data
            snapshot_info = requests.get(url, headers=headers, verify=False)
            # Fetch reclaimable space data
            space_info = requests.get(url2, headers=headers, verify=False)
            
            # Combine snapshot data with reclaimable space data
            combined_info = {**snapshot_info.json(), **space_info.json()}
             # Convert create_time if exists in combined_info
            if 'create_time' in combined_info:
                combined_info['create_time'] = conv_time(combined_info['create_time'])
            
            snapshot_data.append(combined_info)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching snapshots: {e}")
            return None

# Function to get volume UUID
def get_volume_uuid(storage, svm, volume, headers):
    """
    Retrieve the UUID of a volume.

    Args:
        storage (str): Storage name.
        svm (str): SVM name.
        volume (str): Volume name.
        headers (dict): Authentication headers.

    Returns:
        str: UUID of the volume.
    """
    url = f"https://{storage}/api/storage/volumes?svm.name={svm}&name={volume}"
    try:
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200 and response.json()["num_records"] != 0:
            return response.json()["records"][0]["uuid"]
        elif response.json()["num_records"] == 0:
            print(f"Volume does not have snapshot!")
            exit(0)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching volume UUID: {e}")
        return None


# Save JSON data to a JSON file
def save_to_json(data, filename):
    """
    Save JSON data to a file.

    Args:
        data (list): JSON data.
        filename (str): Name of the file to save the data to.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Save JSON data to a CSV file
def save_to_csv(data, filename):
    """
    Save JSON data to a CSV file.

    Args:
        data (list): JSON data.
        filename (str): Name of the CSV file to save the data to.
    """
    df = pd.json_normalize(data)  # Flatten JSON into a DataFrame
    df.to_csv(filename, index=False)

def main(args):
    """
    Main function to execute the program.

    Args:
        args (dict): Command-line arguments.
    """
    # Extract arguments
    storage = args['<storage>']
    svm = args['<svm>']
    volume = args['<volume>']
    
    # Prompt user for username and password
    username = "admin"
    password = "netapp1234"

    # Get authentication headers
    headers = get_headers(username, password)

    # Get volume UUID
    volume_uuid = get_volume_uuid(storage, svm, volume, headers)
    # Get snapshots uuid
    get_snapshots(storage, svm, volume_uuid, headers)
    # Get each snapshot data
    get_snapshot_data(storage, volume_uuid, headers)
    # Save data to JSON
    save_to_json(snapshot_data, 'output.json')
    # Save data to CSV
    save_to_csv(snapshot_data, 'output.csv')

if __name__ == "__main__":
    arguments = docopt(__doc__)
    snapshot_data = []  # List to store snapshot data
    snapshots = []      # List to store snapshot UUIDs
    main(arguments)
