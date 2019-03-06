#!/usr/bin/python3 -

def showIpAPI(data):
	print 
	
	try:
		print("[+] Query : "+"\t\t\t"+data["query"])
		print("[+] Country : "+"\t\t\t"+data["country"]+"("+data["countryCode"]+")")
		print("[+] Region : "+"\t\t\t"+data["city"]+" "+data["regionName"]+"("+data["region"]+")"+", "+data["zip"])
		print("[+] Coordinates : "+"\t\t"+str(data["lat"])+","+str(data["lon"]))
		print("[+] Internet Service Provider : "+data["isp"])
		print("[+] Timezone : "+"\t\t\t"+data["timezone"])
		print("[+] Autonomous System : "+"\t"+data["as"])
		print("[+] Organisation : "+"\t\t"+data["org"])
	except Exception as e:
		print(e)

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