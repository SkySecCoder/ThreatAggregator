#!/usr/bin/python3 -

import json
import sendRequests
import getpass

# OTX api : "https://otx.alienvault.com/api/v1/indicators/IPv4/104.168.167.92/reputation"
#			"https://otx.alienvault.com/api/v1/indicators/IPv4/104.168.167.92/nids_list"

def otxMain(scanIP="", key=""):
	while 1:
		if (scanIP == ""):
			scanIP = input("\n[?] Please enter the IP you wish to scan : ")
		elif (key == ""):
			key = getpass.getpass("\n[?] Enter OTX apikey : ")
		elif (scanIP != "") and (key != ""):
			break

	print("\n [+] OTX data\n")

	reputationData = collectReputationData(scanIP)
	showOtxReputationData(reputationData)

	nidsData = collectNIDSData(scanIP, key)
	showOtxNidsData(nidsData)

def collectNIDSData(scanIP, key):
	nidsDataFromAPI = sendRequests.sendGETrequestWithParams("https://otx.alienvault.com/api/v1/indicators/IPv4/"+scanIP+"/nids_list", myheaders={"X-OTX-API-KEY": key})
	nidsData = []
	for nids in nidsDataFromAPI["results"]:
		data = sendRequests.sendGETrequestWithoutParams("https://otx.alienvault.com/api/v1/indicators/nids/"+str(nids)+"/general")
		nidsData.append(data)
	return nidsData

def collectReputationData(scanIP):
	reputationData = sendRequests.sendGETrequestWithoutParams("https://otx.alienvault.com/api/v1/indicators/IPv4/"+str(scanIP)+"/reputation")
	return reputationData

def showOtxNidsData(data):
	#print(json.dumps(data, sort_keys = True, indent = 4))
	print("[+] NIDS data")
	for item in data:
		print("\t"+item["base_indicator"]["indicator"], end ="\t\t")
		print(doPadding(item["name"]), end ="\t\t")
		print(item["category"], end ="\t\t")
		print(doPadding(item["name"]), end ="\t\t")
		print(doPadding(item["subcategory"]), end ="\t\t")
		try:
			print(doPadding(item["event_activity"]), end ="\t\t")
		except:
			pass
		try:
			print(doPadding(item["cve"]), end ="\t\t")
		except:
			pass
		print()
	print()

def showOtxReputationData(data):
	#print(json.dumps(data, sort_keys = True, indent = 4)) 
	print()
	print("[+] IP was first seen : \t"+data["reputation"]["first_seen"])
	print("[+] IP was last seen : \t\t"+data["reputation"]["last_seen"])
	print("[+] Threat Score of IP : \t"+str(data["reputation"]["threat_score"])+" out of 7")
	print("[+] Counts for various types of activities")
	for key in data["reputation"]["counts"]:
		print("\t"+str(key)+" : "+str(data["reputation"]["counts"][key]))

def doPadding(toBePadded):
	padding = "                         "
	if len(toBePadded) < 26:
		return (toBePadded+padding[0:(len(padding)-len(toBePadded))])
	else:
		return toBePadded

if __name__ == "__main__":
	otxMain()

'''
NIDS DATA
{
    "count": 2,
    "limit": 10,
    "next": null,
    "page": 1,
    "previous": null,
    "results": [
        "2001219",
        "2808717"
    ]
}
'''
'''
REPUTATION DATA
{
    "reputation": {
        "_id": {
            "$id": "5c6cc88503b04d06fc049e0c"
        },
        "activities": [
            {
                "data": [],
                "data_key": "104.168.167.92 hostile",
                "first_date": "2019-02-20T03:24:53",
                "last_date": "2019-03-05T10:16:50",
                "name": "Malicious Host",
                "source": "ciarmy",
                "status": 1
            }
        ],
        "address": "104.168.167.92",
        "allow_ping": "",
        "as": "54290",
        "city": "Seattle",
        "country": "US (United States)",
        "counts": {
            "Malicious Host": 1
        },
        "date_added": {
            "sec": 1550633093,
            "usec": 679000
        },
        "domains": [],
        "first_seen": "2019-02-20T03:24:53",
        "last_seen": "2019-03-05T10:16:50",
        "lat": 47.489101409912,
        "lon": -122.29080200195,
        "matched_bl": [
            "None"
        ],
        "matched_wl": [
            "None"
        ],
        "organization": "Hostwinds LLC.",
        "reputation_rel": "4",
        "reputation_rel_checked": 1,
        "reputation_val": "2",
        "reputation_val_checked": 1,
        "server_type": "",
        "state": 1,
        "status": 1,
        "threat_score": 2,
        "up": 1
    }
}
'''