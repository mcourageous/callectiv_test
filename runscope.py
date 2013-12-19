import requests
import unittest
from requests_runscope import RunscopeAdapter
import json
from xml.etree import ElementTree as etree 


AUTH =  {"apikey":"xxxxxxxxxx", "secret":"xxxxxxxxxxx"}
APPL_JSON = 'application/json'
APPL_XML = 'application/xml'
OK = 200
REFERENCE = "12345"
REFERENCE_1 = "67890"


class Callectiv(unittest.TestCase):
	def setUp(self):
		self.uri = "https://api-callectiv-com/authentication-u453h6ad29k7.runscope.net"


	

	def test_get(self):
		""" Send an authentication request with a GET method"""
		headers = {'Content-Type':APPL_JSON}
		response = requests.get(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsNot(response.status_code, OK)

	def test_post_json_with_default_accept_header(self):
		headers = {'Content-Type':APPL_JSON}
		response = requests.post(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsValidXMLResponse(response)



	

	





if __name__ == "__main__":
	unittest.main()
