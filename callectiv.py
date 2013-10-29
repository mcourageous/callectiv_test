import requests
import unittest
import json

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
		self.assertFalse


	# def test_register_subject(self):
		
	# 	self.subject_body = {"reference":"12345",
	# 				"contact":{"phone":"0207508668"},
	# 				"message":"Callactiv Test"}t
	# 	self.request = requests.post(self.subject_url, data = json.dumps(self.subject_body),headers = self.headers)
	# 	self.assertIn("12345",self.request.content)

	def test_subject_details(self):
		self.url = "http://api.callectiv.com/subject"
		self.subject_body = {"reference":"12345",
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

		







	
		

		# self.content = self.request.json()
		# self.assertEqual(self.subject_body['reference'],"12345")
	















	





	
if __name__ == "__main__":
	unittest.main()








