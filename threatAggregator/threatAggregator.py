#!/usr/bin/python3 -

import json
import argparse
import os
import getpass

import customEncMod
import bannerHandler
import greyNoiseHandler
import ipAPIHandler
import shodanHandler
import otxHandler
import sendRequests

# IP api : "http://ip-api.com/json/104.168.167.92"
# OTX api : "https://otx.alienvault.com/api/v1/indicators/IPv4/104.168.167.92/reputation"
#			"https://otx.alienvault.com/api/v1/indicators/IPv4/104.168.167.92/nids_list"
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
	if (str(args.addr) != "") and (str(args.addr) != " ") and (args.addr is not None):
		scanIP = str(args.addr)
	else:
		scanIP = "104.168.167.92"											# testing ip
	apiKey = ""												
	
	choice = input("\n\t\t[1] IP api\n\t\t[2] OTX api\n\t\t[3] Virustotal api\n\t\t[4] Greynoise api\n\t\t[5] Apility api\n\t\t[6] Shodan api\n\t\t[7] All api\n\n Choice : ")
	if choice == "1":
		ipAPIHandler.ipApiMain(scanIP)
	elif choice == "2":
		if keys == {}:
			keys = getAPIKeys(apiThatUseKey)
		otxHandler.otxMain(scanIP, keys["apiData"]["otx"])
	elif choice == "3":
		data = sendRequests.sendGETrequestWithParams("https://www.virustotal.com/vtapi/v2/ip-address/report", myparams={"apikey":apiKey, "ip":scanIP})
		print(json.dumps(data, sort_keys = True, indent = 4))
	elif choice == "4":
		greyNoiseHandler.greynoiseMain(scanIP)
	elif choice == "5":
		data = sendRequests.sendGETrequestWithoutParams("https://api.apility.net/v2.0/ip/"+scanIP)
	elif choice == "6":
		if keys == {}:
			keys = getAPIKeys(apiThatUseKey)
			print(keys)
		else:
			pass
		#sendRequests.sendGETrequestWithParams("https://api.shodan.io/shodan/host/"+scanIP, {"key":apiKey})
	elif choice == "7":
		# Getting keys
		if keys == {}:
			keys = getAPIKeys(apiThatUseKey)
		# Printing IP API
		ipAPIHandler.ipApiMain(scanIP)
		# Printing Greynoise
		greyNoiseHandler.greynoiseMain(scanIP)
		# Printing OTX
		otxHandler.otxMain(scanIP, keys["apiData"]["otx"])
	else:
		print("[-] What are you doing? -_-")

def getAPIKeys(apiThatUseKey):
	if "data" in os.listdir(os.path.abspath(__file__).strip(os.path.basename(__file__))+"../data/"):
		tempData = customEncMod.decryptmod()
	else:
		print("[-] Data file 'data' is not present in current directory\n[+] Creating data file\n")
		for key in apiThatUseKey:
			apiThatUseKey[key] = getpass.getpass("[?] Enter "+key+" apikey : ")
		customEncMod.createDataFile(apiThatUseKey)
		tempData = customEncMod.encryptmod()

	return tempData 

if __name__ == "__main__":
	main()