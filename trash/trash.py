'''
				  _.,-----/=\-----,._
				 (__ ~~~"""""""~~~ __)
				  | ~~~"""""""""~~~ |
				  | |  ; ,   , ;  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  | |  | |   | |  | |
				  |. \_| |   | |_/ .|
				   `-,.__ ~~~ __.,-'
				         ~~~~~
			888                          888      
			888                          888      
			888                          888      
			888888888d888 8888b. .d8888b 88888b.  
			888   888P"      "88b88K     888 "88b 
			888   888    .d888888"Y8888b.888  888 
			Y88b. 888    888  888     X88888  888 
			 "Y888888    "Y888888 88888P'888  888 
'''
'''
import urllib2
#import requests

# GET response = urllib2.urlopen("https://www.virustotal.com/vtapi/v2/url/report")
#response = urllib2.urlopen("https://www.virustotal.com/vtapi/v2/ip-address/report?apikey=<apiKey>&ip=104.168.167.92").read()

# POST
#params = urllib.urlencode({'ip'  : '104.168.167.92'})
#response = urllib2.urlopen(url='http://api.greynoise.io:8888/v1/query/', data=params).read()

response = urllib2.urlopen("https://www.virustotal.com/vtapi/v2/url/report")

print response.code
data = response.read()
print str(data)
'''