import requests
import unittest
import json

class CallectivTest(unittest.TestCase):

	def setUp(self):
		self.auth_url = "http://api.callectiv.com/authentication"
		self.auth =  {"apikey":"6zUYjnpWPzkPfLmPhwaR","secret":"29xxUQ7ySr"}
		self.headers = {'content-type': 'application/json'}




	def test_authentication_with_wrong_method(self):
		""" Send an authentication request with a get method"""

		self.request = requests.get(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 405)

	def test_authentication_with_post_method(self):
		self.request = requests.post(self.auth_url, data = json.dumps(self.auth), headers=self.headers)
		self.assertEqual(self.request.status_code, 200)
		self.assertEqual(self.request.headers["Content-Type"],"application/xml")
		self.assertTrue(self.request.headers.get["Content-Type"] =="application/xml")








	





	
if __name__ == "__main__":
	unittest.main()








