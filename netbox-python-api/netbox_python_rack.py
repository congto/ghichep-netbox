import os
import pynetbox
import requests
import re
import urllib3
import warnings
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import random


NetBox_URL = 'https://172.16.99.43/'
NetBox_Token = 'df3f38a9b679c0e99c78fa4cfea1c566f5b06ca2'

def netbox_connection_check(netboxurl, netboxtoken):
    try:
        warnings.simplefilter("ignore", InsecureRequestWarning)  
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            netboxurl,
            headers={"Authorization": f"Token {netboxtoken}"},
            timeout=20,
            verify=False  
        )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if response.status_code == 200:
            global nb
            nb = pynetbox.api(netboxurl, token=netboxtoken)
            nb.http_session.verify = False  
            print("Connection Check complete!")
        else:
            print(f"Connection Error: {response.status_code} - {response.reason}")
            return None
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: Can't verify SSL certificate. More: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Unable to reach NetBox. More: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: NetBox did not respond in time. More: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: An unknown error occurred. More: {e}")
    return None

def nb_rack_get():
    rackname = nb.dcim.racks.get(173)
    print(rackname)

def nb_rack_jounral():
    rackname = nb.extras.journal_entries.create(
        {
            "assigned_object_type": "dcim.rack",
            "assigned_object_id": 53,
            "kind": "info",
            "comments": "demo demo ttttttttttt",        
        }
    )

    journal_entry = {
        "assigned_object_type": "dcim.rack",
        "assigned_object_id": 53,
        "kind": "info",
        "comments": "This is a journal entry for the rack.",
    }

    created_journal_entry = nb.extras.journal_entries.create(journal_entry)

def main():
    try:
        print("Step 1: Checking NetBox connection...")
        netbox_connection_check(NetBox_URL, NetBox_Token)

        print("Step 2: Get rack...")
        nb_rack_get()
        nb_rack_jounral()
        
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
