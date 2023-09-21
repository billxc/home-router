import argparse
import datetime
import json
import os
import ssl
import shutil
import ipaddress

import urllib.parse
import urllib.request
import logging


class AzureConfig:
    def __init__(self, configDict):
        self.subscriptionId = configDict["subscriptionId"]
        self.appId = configDict["appId"]
        self.password = configDict["password"]
        self.resourceGroupName = configDict["resourceGroupName"]

CONFIG: AzureConfig = None

def init(args):
    init_logging(args)

    global CONFIG
    if CONFIG is not None:
        return

    if args.config is None:
        raise Exception("No config file specified")

    with open(args.config) as f:
        config = json.load(f)
        # validate config
        for k in ["subscriptionId","appId","password","resourceGroupName"]:
            if k not in config:
                raise Exception(f"config file missing key: {k}")
        CONFIG = AzureConfig(config)

def init_logging(args):
    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Set up logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(args.verbose and logging.DEBUG or logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if args.log is None:
        return
    
    log_file = args.log
    # create log file if not exists
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")

    # move log file if too big, new name: {log_file}-yyyy-mm-dd-hh-mm-ss
    if os.path.getsize(log_file) > 1024 * 1024: # 1MB
        new_name = log_file + datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
        shutil.move(log_file, new_name)

    file_handler = logging.FileHandler(args.log)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def main(args):
    logging.info("Starting update_azure_dns.py")
    logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_dns_record(args.domain,args.ip)


# separate the domain name and the zone name
# www.google.com -> www, google.com
def split_domain(domain):
    # No special handling for top domain or top level domains like co.uk
    # TODO: handle special top level domains like co.uk
    domain_parts = domain.split(".")
    recordSetName = domain_parts[0]
    zoneName = ".".join(domain_parts[1:])
    return recordSetName, zoneName
    

def update_dns_record(domain,new_ip):
    token = getBearerToken()
    [recordSetName, zoneName] = split_domain(domain)
    logging.info(f"Updating DNS record {recordSetName} in zone {zoneName} to {new_ip}")
    formatted_ip = ipaddress.ip_address(new_ip) # validate ip address
    if formatted_ip.version == 6:
        record_type = "AAAA" 
    else:
        record_type = "A"

    dns_service_url = f"https://management.azure.com/subscriptions/{CONFIG.subscriptionId}/resourceGroups/{CONFIG.resourceGroupName}/providers/Microsoft.Network/dnsZones/{zoneName}/{record_type}/{recordSetName}?api-version=2018-05-01"
    # Set the request body parameters
    if formatted_ip.version == 6:
      request_body = {
          "properties": {
              "TTL": 3600,
              "AAAARecords": [
                  {
                      "ipv6Address": formatted_ip.exploded
                  }
                  ]
          }
      }
    else:
      request_body = {
          "properties": {
              "TTL": 3600,
              "ARecords": [
                  {
                      "ipv4Address": new_ip
                  }
              ]
          }
      }
    # Set the request headers, including the authorization header with the bearer token

    # create headers with bearer token
    request_headers = {
        "Authorization": "Bearer " + token, # type: ignore
        "Content-Type": "application/json"
    }

    # Make the PUT request to update the DNS A record

    # Make a PUT request using urllib.request
    req = urllib.request.Request(dns_service_url, data=json.dumps(request_body).encode('utf-8'), headers=request_headers, method='PUT')
    response = urllib.request.urlopen(req)

    # Check the response status to see if the update was successful
    if response.status in [200, 201]:
        print("DNS record successfully updated.")
    else:
        print("Error updating DNS record. Status code: %d" %
              response.status_code)
        print(response.text)


def getBearerToken():
    client_id = CONFIG.appId
    client_secret = CONFIG.password

    # Set the Azure token endpoint URL
    token_endpoint_url = "https://login.microsoftonline.com/f3c77fb7-e702-435b-bfb4-37603d1714b1/oauth2/v2.0/token"

    # Set the request body parameters
    request_body = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scope=https://management.azure.com/.default"

    # Make a POST request to the Azure token endpoint to get the bearer token
    # response = requests.post(token_endpoint_url, data=request_body)


    # Disable SSL verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    data = request_body.encode('utf-8')
    req = urllib.request.Request(token_endpoint_url, data=data)
    response = urllib.request.urlopen(req,context=context)
    # Extract the bearer token from the response
    if response.status == 200:
        response_data = response.read().decode('utf-8')
        json_data = json.loads(response_data)
        bearer_token = json_data["access_token"]
        # print("Bearer token: %s" % bearer_token)
        return bearer_token
    else:
        print("Error getting bearer token. Status code: %d" %
              response.status_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="The domain to update" )
    parser.add_argument("ip", help="The ip value of the domain")
    parser.add_argument("-c","--config", help="The azure_config file to use", default="azure_config.json")
    parser.add_argument("-v","--verbose", help="Use log if flag is on", action="store_true")
    parser.add_argument("-l","--log", help="The log file to use", required=False)
    args = parser.parse_args()
    init(args)
    main(args)
