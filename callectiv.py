import requests
import unittest

class CallectivTest(unittest.TestCase):

	def test_authentication_with_wrong_method(self):
		""" Send an authentication request with a get method"""
		
		auth = {"apikey":"6zUYjnpWPzkPfLmPhwaR","secret":"29xxUQ7ySr"}
		self.request = requests.post("http://api.dev.callectiv.com",params=auth)
		self.assertEqual(self.request.status_code,404)

	def test_authentication(self):
		auth = {"apikey":"6zUYjnpWPzkPfLmPhwaR","secret":"29xxUQ7ySr"}
		self.request = requests.post("http://api.dev.callectiv.com",params=auth)
		self.assertEqual(self.request.status_code, 200)


	# def test_no_authentication(self):
	# 	"""Send a post request without authentication """

	# 	r = requests.post("http://callectiv.com/authentication")
	# 	self.assertEqual(r.status_code, 404)


	
if __name__ == "__main__":
	unittest.main()








