#!/usr/bin/python3 -

import sendRequests

# IP api : "http://ip-api.com/json/104.168.167.92"

def ipApiMain(scanIP=""):
	while 1:
		if (scanIP == ""):
			scanIP = input("\n[?] Please enter the IP you wish to scan : ")
		else:
			break

	print("\n [+] IP API data\n")
	
	ipApiData = collectData(scanIP)
	showIpAPI(ipApiData)

def collectData(scanIP):
	ipApiData = sendRequests.sendGETrequestWithoutParams("http://ip-api.com/json/"+scanIP)
	return ipApiData

def showIpAPI(data):
	print 
	try:
		if data["status"] != "fail":
			print("[+] Query : "+"\t\t\t"+data["query"])
			print("[+] Country : "+"\t\t\t"+data["country"]+"("+data["countryCode"]+")")
			print("[+] Region : "+"\t\t\t"+data["city"]+" "+data["regionName"]+"("+data["region"]+")"+", "+data["zip"])
			print("[+] Coordinates : "+"\t\t"+str(data["lat"])+","+str(data["lon"]))
			print("[+] Internet Service Provider : "+data["isp"])
			print("[+] Timezone : "+"\t\t\t"+data["timezone"])
			print("[+] Autonomous System : "+"\t"+data["as"])
			print("[+] Organisation : "+"\t\t"+data["org"])
		else:
			if data["message"] == "private range":
				print("\n[-] The IP "+str(data["query"])+" is a private range IP address\n")
			elif data["message"] == "reserved range":
				print("\n[-] The IP "+str(data["query"])+" is a reserved range IP address\n")
			else:
				print("\n[-] IP api message : "+str(data["message"])+"\n")
	except Exception as e:
		print(e)

if __name__ == "__main__":
	ipApiMain()

'''
{
	"as": "AS54290 Hostwinds LLC.", 
	"city": "Seattle", 
	"country": "United States", 
	"countryCode": "US", 
	"isp": "Hostwinds LLC.", 
	"lat": 47.4941, 
	"lon": -122.294, 
	"org": "Hostwinds LLC", 
	"query": "104.168.167.92", 
	"region": "WA", 
	"regionName": "Washington", 
	"status": "success", 
	"timezone": "America/Los_Angeles", 
	"zip": "98168"
}
'''