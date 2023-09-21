import argparse
import json

TEMPLATE ='''export AZUREDNS_SUBSCRIPTIONID="<SUBSCRIPTIONID>"
export AZUREDNS_TENANTID="<TENANTID>"
export AZUREDNS_APPID="<APPID>"
export AZUREDNS_CLIENTSECRET="<CLIENTSECRET>"'''

def main(args):
    with open(args.config) as f:
        config = json.load(f)
        # validate config
        for k in ["subscriptionId","tenantId","appId","password"]:
            if k not in config:
                raise Exception(f"config file missing key: {k}")
    global TEMPLATE
    output = TEMPLATE.replace("<SUBSCRIPTIONID>", config["subscriptionId"]).replace("<TENANTID>", config["tenantId"]).replace("<APPID>", config["appId"]).replace("<CLIENTSECRET>", config["password"])
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config", help="The azure_config file to use", default="azure_config.json")
    args = parser.parse_args()
    main(args)