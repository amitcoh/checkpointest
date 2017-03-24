import requests
import json

requests.packages.urllib3.disable_warnings()

CP_API = "https://10.10.13.60:443/web_api/"
USERNAME = "admin"
PASSWORD = "Password1"


def GetSessionId():
	apiCall = "login"
	url = CP_API + apiCall
	body = {"user":USERNAME, "password":PASSWORD}
	headers = {"content-type": "application/json"}
	response = requests.post(url, json=body, headers=headers, verify=False)
	
	return response.json()["sid"]
	
def Publish(sessionId):
	willPublish = raw_input("Yould you like to publish changes? [Y/N]: ")
	if willPublish.lower() == "y":
		apiCall = "publish"
		url = CP_API + apiCall
		body = {}
		headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
		response = requests.post(url, json=body, headers=headers, verify=False)
		if response.json()["task-id"]:
			print "Published!"

def ShowPackages(sessionId):
	apiCall = "show-packages"
	url = CP_API + apiCall
	body = {}
	headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
	response = requests.post(url, json=body, headers=headers, verify=False)
	numOfPkgs = int(response.json()["total"])
	pkgsList = []
	for i in xrange(numOfPkgs):
		pkgsList.append(response.json()["packages"][i]["name"])
	return pkgsList

def AddNetwork(sessionId):
	anotherOne = "y"
	while anotherOne.lower() == "y":
		apiCall = "add-network"
		url = CP_API + apiCall
		netName = raw_input("Please enter object name: ")
		while netName[0].lower() != "s":
			print "Network name must start with 's'"
			netName = raw_input("Please enter object name: ")
		netAddress = raw_input("Please enter network address: ")
		maskLength = int(raw_input("Please enter mask length: "))
		body = {"name":netName, "subnet":netAddress, "mask-length":maskLength}
		headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
		response = requests.post(url, json=body, headers=headers, verify=False)
		if str(response) == "<Response [200]>":
			print "OK!"
		anotherOne = raw_input("Would you like to add another network? [Y/N]: ")
	
def ShowNetworks(sessionId):
	apiCall = "show-networks"
	url = CP_API + apiCall
	body = {}
	headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
	response = requests.post(url, json=body, headers=headers, verify=False)
	for item in response.json()["objects"]:
		#print item
		if item["domain"]["domain-type"].lower() != "data domain":
			#print "NICHT"
			print "Network name:", item["name"], "Network Address:", item["subnet4"] + "/" + str(item["mask-length4"]), "uid:", item["uid"]

def ShowRuleBase(sessionId):
	apiCall = "show-access-rulebase"
	url = CP_API + apiCall
	body = {"name":"Network"}
	headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
	response = requests.post(url, json=body, headers=headers, verify=False)
	for item in response.json()["rulebase"]:
		print "uid:", item["uid"], "\tRule #:", item["rule-number"], "\tName:", item["name"]
		
			
def addRule(sessionId):
	apiCall = "add-access-rule"
	url = CP_API + apiCall
	ruleName = raw_input("Please enter a rule name: ")
	flag = True
	while flag:
		action = raw_input("Would you like to Accept [A] or Drop [D]? ").lower()
		if action == 'a':
			action = "Accept"
			flag = False
		elif action == 'd':
			action = "Drop"
			flag = False
		else:
			print "Wrong Input!"
	'''srcList = []
	src = raw_input("Please enter a source IP address: (Enter '1' to finish)")
	while src != 1:
		srcList.append(src)
		src = raw_input("Please enter a source IP address: (Enter '1' to finish)")'''
	body = {"layer":"Network", "position":"top", "name":ruleName, "action":action }
	headers = {"content-type": "application/json", "X-chkp-sid":sessionId}
	response = requests.post(url, json=body, headers=headers, verify=False)
	print response.text

def ListSize (aList):
	count = 0
	for i in aList:
		count += 1
	return count

def CheckIpAddress (ipAddr):
	count = 0
	for byte in ipAddr.split('.'):
		if byte != '':
			if -1 < int(byte) < 255:
				count += 1
		if ListSize(ipAddr.split('.')) == 5 and ipAddr.split('.')[4] == '':
			return False
	return count == 4
	
def MakeIpList():
	ipAddr = raw_input("Please enter an IP address (end with '-1'): ")
	ipAddrList = []
	while ipAddr != "-1":
		#print ipAddr.split('.')
		while not CheckIpAddress(ipAddr) and ipAddr != "-1":
			print "Wrong input!"
			ipAddr = raw_input("Please enter an IP address (end with '-1'): ")
		ipAddrList.append(ipAddr)
		ipAddr = raw_input("Please enter an IP address (end with '-1'): ")
	return ipAddrList
	
sessionId = GetSessionId()
'''
pkgsList = ShowPackages(sessionId)
print pkgsList
if (raw_input("Would you like to add a network rule? [Y/N]:").lower() == "y"):
	addRule(sessionId)


AddNetwork(sessionId)
Publish(sessionId)
'''
print "\n\nNetwork List:"
ShowNetworks(sessionId)
print "\n\nRulebase List:"
ShowRuleBase(sessionId)

print "\n\n", MakeIpList()