import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.181/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def get():
    resp = requests.get(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070021", #
        auth=basicauth,
        headers=headers,
        verify=False
        )
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        return bool(json.dumps(response_json, indent=4))
    

def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070021",
            "description": "created loopback by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.21.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    
    check = get()
    if check == True:
        return "Cannot create: Interface loopback 65070021"
    else:
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070021", # Add
            data=json.dumps(yangConfig), # Add
            auth=basicauth, 
            headers=headers, # Add 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 65070021 is created successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot create: Interface loopback 65070021"


def delete():
    resp = requests.delete(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070021",
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070021 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 65070021"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070021",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        } 
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070021", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070021 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 65070021"


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070021",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.patch(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback65070021",
        data=json.dumps(yangConfig),
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070021 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 65070021"


def status():
    api_url_status = api_url + "/data/ietf-interfaces:interfaces-state/interface=Loopback65070021"

    resp = requests.get(
            api_url_status,
            auth=basicauth, 
            headers=headers, # Add
            verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
        interface_name = response_json["ietf-interfaces:interface"]["name"]
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if(admin_status == 'up' and oper_status == 'up' and interface_name == 'Loopback65070021'):
            return "Interface loopback 65070021 is enabled"
        elif(admin_status == 'down' and oper_status == 'down' and interface_name == 'Loopback65070021'):
            return "Interface loopback 65070021 is disabled"
        elif(interface_name != 'Loopback65070021'):
            return "No Interface loopback 65070021"
        
    else:
        return "No Interface loopback 65070021"
