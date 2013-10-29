import requests
import unittest
import json
import xml.etree.ElementTree 
import StringIO
import validictory


class CallectivTest(unittest.TestCase):

	def setUp(self):
		self.auth_url = "http://api.callectiv.com/authentication"
		self.auth =  {"apikey":"6zUYjnpWPzkPfLmPhwaR","secret":"29xxUQ7ySr"}
		self.headers = {'content-type': 'application/json',"accept":"application/json"}
	
		self.access = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)

		self.token = json.loads((self.access.content)).get('token')

	def test_authentication_with_wrong_method(self):
		""" Send an authentication request with a get method"""

		self.request = requests.get(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 405)

	def test_authentication_with_post_method(self):
		
		self.request = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 200)
		self.assertEqual(self.request.headers["Content-Type"],"application/json")
		


	def test_subject_details(self):
		self.url = "http://api.callectiv.com/subject"
		self.reference = "12345"
		self.subject_body = {"reference":self.reference,
					"contact":{"phone":"0207508668"},
					"message":"Callactiv Test"} 

		headers = {"content-type":"application/json", "authorization":self.token}
		self.post = requests.post(self.url,data=json.dumps(self.subject_body),headers=headers)
		self.assertEqual(self.post.status_code, 200)
		
		header = headers.update({'accept':'application/json'})
		self.get =requests.get("http://api.callectiv.com/subject/12345", headers=headers)
		
		response = json.loads(self.get.content)
		self.assertEqual(response.get("message"), u"Callactiv Test")
		self.assertEqual(response.get("reference"),"12345")
		self.assertEqual(response.get("contact")["phone"], "0207508668")

	def test_subject_connections_default_accept_type(self):
		self.connection_url = "http://api.callectiv.com/subject/12345/connections"
		headers = {"content-type":"application/json","authorization":self.token}
		self.subject = requests.get(self.connection_url,headers=headers)
		self.assertEqual(xml.etree.ElementTree.fromstring(self.subject.content).tag,"connections")
	

	def test_subject_connection_with_json_accept_type(self):
		self.connection_url = "http://api.callectiv.com/subject/12345/connections"
		headers = {"content-type":"application/json","accept":"application/json","authorization":self.token}
		self.subject = requests.get(self.connection_url,headers=headers)
		output = json.loads(self.subject.content)
		expected_schema = {"type":"NoneType"}
		self.assertIsNot(None,output)

		# self.assertEqual(json.loads(self.subject.content),ValueError)
		# self.assertEqual(validictory.validate(output,expected_schema))

	def test_change_status_with_get_method(self):
		"""test status change with wrong method """

		self.status_url = "http://api.callectiv.com/subject/12345/status/enabled"
		headers = {"content-type":"application/json","accept":"application/json","authorization":self.token}
		self.send = requests.get(self.status_url,headers=headers)
		self.assertEqual(self.send.status_code, 405)
		self.assertFalse(self.send.status_code == requests.codes.ok)

	def test_change_status_with_disabled_status(self):
		self.put_url = "http://api.callectiv.com/subject/12345/status/disabled"
		headers = {"content-type":"application/json","accept":"application/json","authorization":self.token}
		self.put = requests.put(self.put_url,headers=headers)
		self.assertEqual(self.put.status_code, 409)
		self.assertIsNot(self.put.status_code, 200)
		print self.put.status_code




if __name__ == "__main__":
	unittest.main()








