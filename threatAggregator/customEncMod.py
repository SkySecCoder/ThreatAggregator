#!/usr/bin/python3 -

import json
import platform
import os
import getpass
import crypt

def createDataFile(dictToEncrypt):									# [Accessible as external mod]
	data = {"encryptFlag" : 0, "apiData":dictToEncrypt}
	file = open("../data/data", "w")
	file.write(json.dumps(data, sort_keys=True, indent=4))
	file.close()

def encryptmod():													# [Accessible as external mod(must only be used in the begining when file not encrypted)] 
	# decData is a list whose "0" position contains 0(decryption failure) or 1(decryption successful). It's 1 position contains the decrypted data
	decData = [0]

	# Opening data file
	file = open("../data/data", "r")
	data = file.read()
	file.close()

	# Checking if initial encryption is required. SHOULD BE JSON
	try:
		jsonData = json.loads(data)
		# Checking to see if encryptFlag in json template is 0. If 0 then the json must be encrypted. If anything else program exit
		if jsonData["encryptFlag"] == 0:
			# Ask user if json has to be encrypted using choiceCounter
			choiceCounter = 0
			while choiceCounter == 0:
				choice = input("[?] It appears you would like to encrypt the data file.\n[?] Proceed?(y/n):")
				if (choice == "y" or choice == "Y"):
					encryptStart(1)
					choiceCounter = 1
					decData = decryptStart()
				elif (choice == "n" or choice == "N"):
					print("[-] Exiting program...")
					choiceCounter = 1
				else:
					print("Please choose a valid choice(y/n)")
		else:
			print("[*] It is mandatory for this script to encrypt your data file\n    Please set the 'encryptFlag' to 0")
			decData[0] = 0
	# 3 possibilities 1)json can be broken(not following template) 2) file is not following json format at all 3) file has already been encrypted.
	except Exception as e:
		with open("../data/data") as f:
			line = f.readline()
		# 3) file has already been encrypted
		if "[DATA ENCRYPTED]" in line:
			decData = decryptStart()
		# 1)json can be broken 2) file is not following json format at all
		else:
			print("[-] Your data file seems to be corrupted or is not following the required template")
			decData[0] = 0
	if decData[0] == 1:
		passDataToParentProgram = {}
		try:
			passDataToParentProgram = json.loads(decData[1])
		except:
			print("[-] Data was found to be corrupted. This may be because you entered the wrong password\n    or the data file has been modified.\n")
		return passDataToParentProgram
	else:
		return {}

def decryptmod():													# [Accessible as external mod]
	with open("../data/data") as f:
		line = f.readline()
	if "[DATA ENCRYPTED]" in line:
		decData = decryptStart()
		if decData[0] == 1:
			passDataToParentProgram = {}
			try:
				passDataToParentProgram = json.loads(decData[1])
			except:
				print("[-] Corrupted data has been recovered. This may be because you entered the wrong password\n    or the data file has been modified.\n")
			return passDataToParentProgram
		else:
			return "0"
	else:
		return encryptmod()

def encryptStart(initialEncrypt):
	# initialEncrypt is 1 if the data file has to be encrypted for the first time. This valuse will change in future versions of the program to accomodate change in credentials
	# Getting password from user which will hashed and the hash will be used as an AES key
	passwordSame = False
	while passwordSame == False:
		password = getpass.getpass("[?] Enter new password : ")
		temp = getpass.getpass("[?] Please retype the password to confirm : ")
		if temp == password:
			passwordSame = True
		else:
			print("\n[-] The retyped password does not match. Please try again.\n")
	initialSalt = generateInitialSalt(password)
	AESkey = generateAESKey(password, initialSalt)
	file = open("../data/data","r")
	data = file.read()
	jsonData = json.loads(data)
	# Switching encryptFlag from 0 to 1 which signifies that data file has been encrypted. This data is going to be encrypted then put into the data file
	jsonData["encryptFlag"] = 1
	file.close()
	file = open("../data/data", "w")
	file.write(json.dumps(jsonData, sort_keys=True, indent=4))
	file.close()
	if initialEncrypt == 1:
		# Initial Encrypting
		# Encrypting data file with AES key
		ossllocation = opensslLocation()
		enc = os.popen("echo '"+data+"' | "+ossllocation+" enc -nosalt -e -aes-256-cbc -base64 -pass pass:"+AESkey).read()
		file = open("../data/data","w")
		# Attaching "[DATA ENCRYPTED]" at the start of file to indicate that the file has been encrypted by this program
		file.write("[DATA ENCRYPTED]\n"+enc)
		file.close
		print("[+] Your encrypted data file has been created\n[+] Please remember your password, in order to access your data.")

def opensslLocation():
	location = ""
	choice = ''
	if platform.system() == "Darwin":
		# Check if brew is installed
		allDependenciesInstalled = False
		if "brew" in os.listdir("/usr/local/bin/"):
			if ("openssl" in os.listdir("/usr/local/Cellar/")):
				allDependenciesInstalled = True
			else:
				choice = input("[?] This program needs openssl to work. Install openssl? : ")
				if choice == 'Y' or choice == 'y':
					os.system("brew install openssl")
					allDependenciesInstalled = True
				else:
					print("[-] Exiting program")
					location = "[-] Error"
		else:
			print("[-] Brew is not installed")
			choice = input("[?] You must install brew for this program to work. Install brew? : ")
			if (choice == 'Y' or choice == 'y'):
				os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
				choice = input("[?] This program needs openssl to work. Install openssl? : ")
				if choice == 'Y' or choice == 'y':
					os.system("brew install openssl")
					allDependenciesInstalled = True
				else:
					print("[-] Exiting program")
					location = "[-] Error"
			else:
				print("[-] Exiting program")
				location = "[-] Error"
		if allDependenciesInstalled == True:
			location = "/usr/local/Cellar/openssl/"
			location = location + os.listdir(location)[0] + "/bin/openssl"
	elif platform.system() == "Linux":
		location = "/usr/bin/openssl"
	else:
		print("\n[-] This script currently does not support the OS that you are running")
		location = "[-] Error"
	if ("location" == "[-] Error"):
		return (0/0)
	else:
		return location 

def decryptStart():
	print("[+] Accessing encrypted data file")
	dec = []
	try:
		#Decrypting
		password = getpass.getpass("[?] Enter password : ")
		initialSalt = generateInitialSalt(password)
		AESkey = generateAESKey(password, initialSalt)
		file = open("../data/data","r")
		data = file.read()
		file.close()
		dec.append(1)
		ossllocation = opensslLocation()
		dec.append(os.popen("echo '"+data+"' | "+ossllocation+" enc -nosalt -d -aes-256-cbc -base64 -pass pass:"+AESkey).read())
		print("[+] Decryption completed")
		# Credential Recovery
		#print dec
		return dec
	except Exception as e:
		print("[-] Error occurred : "+str(e))
		dec[0] = 0
		return dec

def generateInitialSalt(password):
	# Generating initial salt for the hashes
	if len(password) > 8:
		salt = crypt.crypt(password, ("$6$"+password[(len(password)-8):len(password)]))
	else:
		salt = password[len(password)/2:len(password)]
		salt = salt+"vD7sMqYc"
		salt = salt[0:8]
		salt = crypt.crypt(password, ("$6$"+salt))
	salt = salt[12:20]
	return salt

def generateAESKey(password, salt):
	# Generating AES key by hashing the password 100 times
	key = ""
	i = 0
	while i < 101:
		i += 1
		genPassword = crypt.crypt(password,("$6$" + salt))
		password = genPassword[12:len(genPassword)]
		salt = password[0:8]
		if i == 100:
			key = password
	return key