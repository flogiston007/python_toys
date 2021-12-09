import urllib.request
import json
from urllib.error import HTTPError, URLError
import socket

# settings
server1 = "site1.org/"
server2 = "site.org/"
# comparing_key = "history_latest_ledger"
comparing_key = "core_version"

class bcolors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\33[101m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def msgPrint (type_msg, msg):
    if type_msg == 'err':
        print(bcolors.FAIL + "[ERROR] " + bcolors.ENDC + msg)
    elif type_msg == 'succ':
        print(bcolors.OKGREEN + "[SUCCESS] " + bcolors.ENDC + msg)
    elif type_msg == 'info':
        print(bcolors.OKCYAN + "[INFO] " + bcolors.ENDC + msg)
    elif type_msg == 'curr':
        print(bcolors.BOLD + "[---] " + bcolors.ENDC + msg)  
    elif type_msg == '':
        print('\n' + msg) 

def getJsonData (server):
    try:
        msgPrint("curr", f"Connecting to sources: {server}")
        response = urllib.request.urlopen(server, timeout=5)
        element = parseJsonData(response, server)
        return element
    except HTTPError as error:
        msgPrint("err", f'Data not retrieved from URL: {server}')
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
        	msgPrint("err", f'socket timed out - URL {server}')
        else:
        	msgPrint("err", 'some other error happened')

def parseJsonData (response, uri):
    try:
        data = json.loads(response.read())
        msgPrint('succ', f"Data from {uri} has been successfully retrieved")
        if comparing_key in data:
        	comparing_value = data[comparing_key]
        	return comparing_value
        else:
        	msgPrint('err', f"The data received from the {uri} does not contains the {comparing_key} key!")
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        msgPrint('err', f"Decoding JSON from {uri} has failed")
    
def getResultsOfComparing (serv1, serv2):
	value_from_json = []
	clean_val = []
	value_from_json.append(getJsonData(serv1))
	value_from_json.append(getJsonData(serv2))
	try:
		clean_val.append(value_from_json[0].split()[1])
		clean_val.append(value_from_json[1].split()[1])
		msgPrint("info", f'JSON strings by key {comparing_key} are splitted')
	except Exception:
		msgPrint("info", f'JSON strings by key {comparing_key} are not splitted')
		clean_val.append(value_from_json[0])
		clean_val.append(value_from_json[1])
	finally:
		t = compareTwoEntities(clean_val[0], clean_val[1])
		msgPrint('info', f'Compared values: \n{serv1} key: {clean_val[0]} \n{serv2} key: {clean_val[1]}')
		return t

def compareTwoEntities (val1, val2):
    	if val1 == val2:
    		return 1
    	else:
    		return 0


if __name__ == "__main__":
    msgPrint('info', "Comparison between the prod version and the dev version")

    if (getResultsOfComparing(server1, server2) == 0):
    	msgPrint("err", f'Found difference between versions!')
    else:
    	msgPrint("succ", f'Difference between versions not found')
