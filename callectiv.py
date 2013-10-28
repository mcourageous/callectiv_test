import requests
import unittest
import json

class CallectivTest(unittest.TestCase):

	def setUp(self):
		self.auth_url = "http://api.callectiv.com/authentication"
		self.auth =  {"apikey":"6zUYjnpWPzkPfLmPhwaR","secret":"29xxUQ7ySr"}
		self.headers = {'content-type': 'application/json'}
		self.subject_url = "http://api.callectiv.com/subject"




	def test_authentication_with_wrong_method(self):
		""" Send an authentication request with a get method"""

		self.request = requests.get(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 405)

	def test_authentication_with_post_method(self):
		self.request = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 200)
		self.assertEqual(self.request.headers["Content-Type"],"application/xml")
		self.assertFalse


	# def test_register_subject(self):
		
	# 	self.subject_body = {"reference":"12345",
	# 				"contact":{"phone":"0207508668"},
	# 				"message":"Callactiv Test"}
	# 	self.request = requests.post(self.subject_url, data = json.dumps(self.subject_body),headers = self.headers)
	# 	self.assertIn("12345",self.request.content)

	def test_subject_details(self):

		self.url = "http://api.callectiv.com/subject/12345"
		self.subject_body = {"reference":"12345",
					"contact":{"phone":"0207508668"},
					"message":"Callactiv Test"}
		self.post = requests.post(self.url, data = json.dumps(self.subject_body),headers = self.headers)

		self.get = requests.get("http://api.callectiv.com/subject/12345")
		print self.post
		print self.get


		# self.content = self.request.json()
		# self.assertEqual(self.subject_body['reference'],"12345")
	















	





	
if __name__ == "__main__":
	unittest.main()








