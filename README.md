# snapshot.py

## Description

`snapshot.py` is a Python script designed to retrieve information about snapshots from a storage system using its API. It authenticates with the API using provided credentials, retrieves information about snapshots for a specified volume, and saves the snapshot data to JSON and CSV files.

## Usage

```sh
python snapshot.py <storage> <svm> <volume>
```
## Arguments
- `<storage>`: Name of the storage system.
- `<svm>`: Name of the Storage Virtual Machine (SVM).
- `<volume>`: Name of the volume.
## Dependencies
* base64
* requests
* json
* pandas
* dateutil.parser
* docopt
* Functionality
* conv_time(time):

## Functionality

1. conv_time(time):
    * Converts the snapshot creation time from ISO 8601 format to a formatted string.

2. get_headers(username, password):
    * Generates authentication headers for API requests.

3. get_snapshots(storage, svm, volume, headers):
    * Retrieves information about snapshots for a specified volume.
4. get_snapshot_data(storage, uuid, headers):

    * Retrieves detailed information about each snapshot, including reclaimable space.
5. get_volume_uuid(storage, svm, volume, headers):

    * Retrieves the UUID of a volume.
6. save_to_json(data, filename):

    * Saves JSON data to a file.
7. save_to_csv(data, filename):

    * Saves JSON data to a CSV file.
8. main(args):

    * Main function to execute the program. Parses command-line arguments, retrieves snapshot data, and saves it to JSON and CSV files.

# Usage Example

```sh
python prog.py storage1 svm1 volume1
```

This command retrieves snapshot data for the volume "volume1" in the SVM "svm1" of the storage system "storage1", and saves the data to JSON and CSV files.

Note: Ensure to replace "storage1", "svm1", and "volume1" with the actual names of your storage system, SVM, and volume, respectively.

# Author
    anon0313