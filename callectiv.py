import requests
import unittest

class CallectivTest(unittest.TestCase):

	def test_authentication(self):

		r = requests.post("http://callectiv.com/authentication")
		self.assertEqual(r.status_code, 404)

	def test_auth_method(self):
		pass

if __name__ == "__main__":
	unittest.main()








