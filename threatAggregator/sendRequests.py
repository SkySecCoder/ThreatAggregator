import requests

def sendGETrequestWithoutParams(scanURL):
	response = requests.get(url = scanURL)
	data = response.json()
	return data

def sendGETrequestWithParams(scanURL, myparams="", myheaders=""):
	if myheaders == "":
		myheaders = {"Content-Type":"application/json"}
	if "" == myparams:
		response = requests.get(url = scanURL, headers = myheaders)
	else:
		response = requests.get(url = scanURL, headers = myheaders, params=myparams)
	data = response.json()
	return data

def sendPOSTrequest(scanURL, mydata, myheaders=""):
	if myheaders == "":
		myheaders = {"Content-Type":"application/json"}
	response = requests.post(url = scanURL, headers=myheaders, data = mydata)
	data = response.json()
	return data