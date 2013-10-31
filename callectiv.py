import requests
import unittest
import json
import xml.etree.ElementTree 
import StringIO
import validictory
import dateutil.parser as parser
import datetime


class CallectivTest(unittest.TestCase):


	def time(self, text):
		date = parser.parse(text)
		return date.isoformat()

	def setUp(self):

		self.auth_url = "http://api.callectiv.com/authentication"
		self.auth =  {"apikey":"6zUYjnpWPzkPfLmPhwaR", "secret":"29xxUQ7ySr"}
		self.headers = {"content-type": "application/json", "Accept":"application/json"}
		self.access = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.token = json.loads((self.access.content)).get('token')

	def test_authentication_with_wrong_method(self):
		""" Send an authentication request with a get method"""
		request = requests.get(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertIsNot(request.status_code, 200)

	def test_authentication_with_post_method(self):
		
		request = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(request.status_code, 200)
		
	def test_subject_details(self):

		url = "http://api.callectiv.com/subject"
		reference = "12345"
		request_body = {"reference":reference,
					"contact":{"phone":"0207508668"},
					"message":"Callactiv Test"} 

		headers = {"Content-Type":"application/json", "Authorization":self.token}
		request = requests.post(url, data=json.dumps(request_body), headers=headers)
		self.assertEqual(request.status_code, 200)
		response =requests.get("http://api.callectiv.com/subject/12345", headers=headers)
		json_response = json.loads(response.get.content)
		self.assertEqual(json_response.get("message"), u"Callactiv Test")
		self.assertEqual(json_response.get("reference"), "12345")
		self.assertEqual(json_response.get("contact")["phone"], "0207508668")
		
	def test_connections_default_accept_type(self):

		url = "http://api.callectiv.com/subject/12345/connections"
		headers = {"Content-Type":"application/xml", "Authorization":self.token}
		subject = requests.get(url, headers=headers)
		self.assertEqual(subject.status_code, 200)
		self.assertEqual(xml.etree.ElementTree.fromstring(subject.content).tag, "connections")

	def test_connections_with_json_accept_type(self):

		url = "http://api.callectiv.com/subject/12345/connections"
		headers = {"Content-Type":"application/json", "Authorization":self.token}
		response = requests.get(url, headers=headers)
		self.assertEqual(response.status_code, 200)
		self.assertIsNotNone(response.content)
		output = json.loads(response.content)
		self.assertIsNotNone(output)
		
	def test_change_status_with_get_method(self):
		"""test status change with wrong method """

		url = "http://api.callectiv.com/subject/12345/status/enabled"
		headers = {"content-type":"application/json","accept":"application/json","authorization":self.token}
		response = requests.get(url, headers=headers)
		self.assertNotEqual(response.status_code, 200)

	def test_change_status_with_disabled_status(self):
		url = "http://api.callectiv.com/subject/12345/status/disabled"
		headers = {"content-type":"application/json","accept":"application/json","authorization":self.token}
		response = requests.put(url,headers=headers)
		self.assertEqual(response.status_code, 200)
		response_1 = requests.put(url,headers=headers)
		self.assertIsNot(response_1.status_code, 200)




	def test_delete_subject_with_reference(self):
		""" check status code"""
		url = "http://api.callectiv.com/subject/12345"
		headers = {"Authorization":self.token}
		delete =requests.delete(url, headers= headers)
		self.assertEqual(delete.status_code, 200)
		
	def test_delete_subject_with_wrong_reference(self):
		"""check status code"""
		url = "http://api.callectiv.com/subject/2347"
		delete = requests.delete(url, headers=self.headers)
		self.assertIsNot(delete.status_code, 200)



	def test_make_connections(self):
		url = "http://api.callectiv.com/connection"
		headers = {"Content-Type":"application/json","Authorization":self.token}
		tim = self.time(str(datetime.datetime.now()))
		request_a = {
					"from":{
						"phone":"23327508668",
						"message":"Hello world"
					},
					"subjectReference":"12345",
					"startDateTime": tim}

		request_b = {
					"to":{
						"phone":"23320755555",
						"message":"How are you"
					},
					"subjectReference":"12345",
					"startDateTime":tim
					}
		request_a = requests.post(url, headers=headers, data=request_a)
		request_b = requests.post(url, headers=headers, data=request_b)
		self.assertEqual(request_a.status_code, 200)
		self.assertEqual(request_b.status_code, 200)

	# def test_get_connection_details(self):
	# 	"""check the response body and assert if its equal to what was sent in the post request"""
	# 	self.detail_url = "http://api.callectiv.com/connection/{connectionId}"

	# 	pass

	# def get_connection_status(self)







if __name__ == "__main__":
	unittest.main()








		# self.connection_request ={"from":{
		# 							"phone":"233207508668",
		# 							"message":"Hello world"
		# 							},
		# 						"subjectReference":"12345","startDateTime": self.time("Wed, 30 Oct 2013 10:50:05 +0000")}
