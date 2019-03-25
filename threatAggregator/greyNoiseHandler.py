#!/usr/bin/python3 -

import sendRequests

def greynoiseMain(scanIP=""):
	while 1:
		if (scanIP == ""):
			scanIP = input("\n[?] Please enter the IP you wish to scan : ")
		else:
			break

	print("\n [+] Greynoise data\n")
	
	greynoiseData = collectData(scanIP)
	showGreynoise(greynoiseData)

def collectData(scanIP):
	greynoiseData = sendRequests.sendPOSTrequest("http://api.greynoise.io:8888/v1/query/ip", {"ip":scanIP})
	return greynoiseData

def showGreynoise(data):
	if data["status"] == "ok":
		records = data["records"]
		print() 
		print("First Seen\tLast Updated\tConfidence\tName\n")
		try:
			for record in records:
				print(record["first_seen"].split("T")[0]+"\t", end="")
				print(record["last_updated"].split("T")[0]+"\t", end="")
				print(record["confidence"]+"\t\t", end="")
				print(record["name"]+"\n", end="")
		except Exception as e:
			print(e)
	else:
		print("[-] Greynoise api was unable to locate IP details")

if __name__ == "__main__":
	greynoiseMain()

'''
{
	"ip": "104.168.167.92", 
	"records": [
		{
			"category": "activity", 
			"confidence": "high", 
			"first_seen": "2019-02-27T14:24:13Z", 
			"intention": "", 
			"last_updated": "2019-03-01T12:24:11Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "NETIS_ROUTER_ADMIN_SCANNER_HIGH"
		}, 
		{
			"category": "activity", 
			"confidence": "high", 
			"first_seen": "2019-02-27T01:02:42Z", 
			"intention": "", 
			"last_updated": "2019-03-01T02:53:28Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "SSH_SCANNER_HIGH"
		}, 
		{
			"category": "activity", 
			"confidence": "low", 
			"first_seen": "2019-02-25T21:05:34Z", 
			"intention": "", 
			"last_updated": "2019-02-25T21:05:34Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "SSH_SCANNER_LOW"
		}, 
		{
			"category": "worm", 
			"confidence": "high", 
			"first_seen": "2019-02-25T21:05:34Z", 
			"intention": "malicious", 
			"last_updated": "2019-03-01T02:53:30Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "SSH_BRUTEFORCER"
		}, 
		{
			"category": "worm", 
			"confidence": "high", 
			"first_seen": "2019-02-25T14:00:40Z", 
			"intention": "malicious", 
			"last_updated": "2019-02-25T14:00:40Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "BELKIN_N750_WORM_CVE_2014_1635"
		}, 
		{
			"category": "tool", 
			"confidence": "high", 
			"first_seen": "2019-02-25T14:00:30Z", 
			"intention": "", 
			"last_updated": "2019-03-01T12:24:11Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "ZMAP_CLIENT"
		}, 
		{
			"category": "activity", 
			"confidence": "low", 
			"first_seen": "2019-02-25T14:00:30Z", 
			"intention": "", 
			"last_updated": "2019-02-25T14:00:30Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "Ethernet or modem", 
				"org": "IMS", 
				"os": "Linux 3.1-3.10", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "HTTP_ALT_SCANNER_LOW"
		}, 
		{
			"category": "tool", 
			"confidence": "high", 
			"first_seen": "2019-02-20T00:55:47Z", 
			"intention": "", 
			"last_updated": "2019-02-20T00:55:47Z", 
			"metadata": {
				"asn": "AS54290", 
				"datacenter": "", 
				"link": "", 
				"org": "IMS", 
				"os": "", 
				"rdns": "hwsrv-417530.hostwindsdns.com", 
				"rdns_parent": "hostwindsdns.com", 
				"tor": false
			}, 
			"name": "ZMAP_CLIENT"
		}
	], 
	"returned_count": 8, 
	"status": "ok"
}

'''