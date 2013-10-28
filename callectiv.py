import requests
import unittest

class CallectivTest(unittest.TestCase):



	def test_authentication(self):

		r = requests.post("http://callectiv.com/authentication")
		self.assertEqual(r.status_code, 404)

	def test_auth_with_wrong_method(self):
		r = requests.get("http://callectiv.com/authentication")
		self.assertEqual(r.status_code,404)
	

if __name__ == "__main__":
	unittest.main()








