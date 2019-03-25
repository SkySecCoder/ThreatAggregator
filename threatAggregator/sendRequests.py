import requests

def sendGETrequest(scanURL, myparams="", myheaders=""):
	if myheaders == "":
		myheaders = {"Content-Type":"application/json"}
	if "" == myparams:
		response = requests.get(url = scanURL, headers = myheaders)
	else:
		response = requests.get(url = scanURL, headers = myheaders, params=myparams)
	data = response.json()
	return data

def sendPOSTrequest(scanURL, mydata):
	response = requests.post(url = scanURL, data = mydata)
	data = response.json()
	return data
