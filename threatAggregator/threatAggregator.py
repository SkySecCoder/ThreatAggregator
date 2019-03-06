#!/usr/bin/python3 -

import requests
import json
import argparse
import os
import getpass

import customEncMod
import bannerHandler
import greyNoiseHandler
import ipAPIHandler
import shodanHandler

# IP api : "http://ip-api.com/json/104.168.167.92"
# OTX api : "https://otx.alienvault.com/api/v1/indicators/IPv4/104.168.167.92/reputation"
# VIRUSTOTAL api : "https://www.virustotal.com/vtapi/v2/ip-address/report?apikey=<apiKey>&ip=104.168.167.92"
# GREYNOISE api : "http://api.greynoise.io:8888/v1/query/ip"
# APILITY api : "https://api.apility.net/v2.0/ip/"
# SHODAN api : "https://api.shodan.io/shodan/host/{ip}?key=<apiKey>"

def main():
	apiThatUseKey = {
		"shodan":"",
		"virustotal":"",
		"apility":"",
		"otx":""
	}

	keys = {}

	parser = argparse.ArgumentParser(description="Lookup IP address reputation")
	parser.add_argument("-a","--addr", dest="addr", type=str, help="IP Address to lookup")
	parser.add_argument("--no-banner",dest="banner",action="store_true", help="Don\"t print banner")
	args = parser.parse_args()

	print("[+] Welcome to Threat Aggregator")

	# bannerHandler.showBanner()
	# getAPIKeys()

	choice = ""
	scanIP = "104.168.167.92"
	'''scanIP = str(args.addr)'''
	apiKey = ""												
	
	choice = input("\n\t\t[1] IP api\n\t\t[2] OTX api\n\t\t[3] Virustotal api\n\t\t[4] Greynoise api\n\t\t[5] Apility api\n\t\t[6] Shodan api\n\t\t[7] All api\n\n Choice : ")
	if choice == "1":
		data = sendGETrequestWithoutParams("http://ip-api.com/json/"+scanIP)
		ipAPIHandler.showIpAPI(data)
	elif choice == "2":
		data = sendGETrequestWithoutParams("https://otx.alienvault.com/api/v1/indicators/IPv4/"+scanIP+"/reputation")
	elif choice == "3":
		sendGETrequestWitParams("https://www.virustotal.com/vtapi/v2/ip-address/report",{"apikey":apiKey, "ip":scanIP})
	elif choice == "4":
		data = sendPOSTrequest("http://api.greynoise.io:8888/v1/query/ip", {"ip":scanIP})
		greyNoiseHandler.showGreynoise(data)
	elif choice == "5":
		data = sendGETrequestWithoutParams("https://api.apility.net/v2.0/ip/"+scanIP)
	elif choice == "6":
		if keys != {}:
			getAPIKeys()
		else:
			pass
		sendGETrequestWitParams("https://api.shodan.io/shodan/host/"+scanIP, {"key":apiKey})
	elif choice == "7":
		# Printing IP API
		data = sendGETrequestWithoutParams("http://ip-api.com/json/"+scanIP)
		ipAPIHandler.showIpAPI(data)
		# Printing Greynoise
		data = sendPOSTrequest("http://api.greynoise.io:8888/v1/query/ip", {"ip":scanIP})
		greyNoiseHandler.showGreynoise(data)
	else:
		print("[-] What are you doing? -_-")

def getAPIKeys():
	if "data" in os.listdir(os.path.abspath(__file__).strip(os.path.basename(__file__))+"../data/"):
		pass
	else:
		print("[-] Data file 'data' is not present in current directory\n[+] Creating data file\n")
		for key in apiThatUseKey:
			apiThatUseKey[key] = getpass.getpass("[?] Enter "+key+" apikey : ")
		customEncMod.createDataFile(apiThatUseKey)

	tempData = customEncMod.encryptmod()
	return tempData 

def sendGETrequestWithoutParams(scanURL):
	response = requests.get(url = scanURL)
	tempdata = json.dumps(response.json())
	data = json.loads(tempdata)
	return data

def sendGETrequestWitParams(scanURL, myparams):
	response = requests.get(url = scanURL, params = myparams)
	tempdata = json.dumps(response.json())
	data = json.loads(tempdata)
	print(json.dumps(data, indent=4, sort_keys=True))

def sendPOSTrequest(scanURL, myparams):
	response = requests.post(url = scanURL, data = myparams)
	tempdata = json.dumps(response.json())
	data = json.loads(tempdata)
	return data

if __name__ == "__main__":
	main()