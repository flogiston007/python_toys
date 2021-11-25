import urllib.request
import json
from urllib.error import HTTPError, URLError
import socket

# settings
servers = ['https://horizon.stellar.org/', 
'https://horizon-testnet.stellar.org/']

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

def getJsonData (server):
    try:
        msgPrint("curr", f"Connecting to sources: {server}")
        response = urllib.request.urlopen(server, timeout=5)
        element = parseJsonData(response)
        return element
    except HTTPError as error:
        msgPrint("err", f'Data not retrieved from URL: {server}')
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
        	msgPrint("err", f'socket timed out - URL {prod_server}')
        else:
        	msgPrint("err", 'some other error happened')

def parseJsonData (response):
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
    


if __name__ == "__main__":
    msgPrint('info', "Comparison between the prod version and the dev version")

    comparing_values = []
    for uri in servers:
    	msgPrint('info', f'Got URL: {uri}')
    	comparing_values.append(getJsonData(uri))
    	
    msgPrint('info', 'Checking for Identity\n')
    for i in range(len(comparing_values)-1):
    	# msgPrint('info', comparing_values[i])
    	if comparing_values[i] != comparing_values[i+1]:
    		msgPrint('err', "Found difference between servers!")
    		msgPrint('info', f"{comparing_values[i]}")
    		msgPrint('info', f"{comparing_values[i+1]}")
    	else:
	    	msgPrint('succ', "Difference between versions not found")
	    	msgPrint('info', f"{comparing_values[i]}")
	    	msgPrint('info', f"{comparing_values[i+1]}")
