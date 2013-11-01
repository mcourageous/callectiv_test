import requests
import unittest
import json
from xml.etree import ElementTree as etree 
import StringIO
import validictory
import dateutil.parser as parser
import datetime

AUTH =  {"apikey":"6zUYjnpWPzkPfLmPhwaR", "secret":"29xxUQ7ySr"}
APPL_JSON = 'application/json'
APPL_XML = 'application/xml'
OK = 200
REFERENCE = "12345"
REFERENCE_1 = "67890"
REQUEST_BODY =  {"reference":REFERENCE,
				"contact":{"phone":"0207508668"},
				"message":"Callactiv Test"
				} 

REQUEST_BODY_1 =  {"reference":REFERENCE,
					"contact":{"phone":"0207508668"},
					"message":"Call Test"
				  } 

REQUEST_BODY_XML = """ <subject>
						<reference>12345</reference>
						<contact>
						<phone> 0207508668</phone>
						</contact>
						<message> Callactiv Test</message>
						</subject>
					"""

REQUEST_BODY_XML_1 =""" <subject>
						<reference>12345</reference>
						<contact>
						<phone> 0207508668</phone>
						</contact>
						<message> Call Test</message>
						</subject>
					"""
REQUEST_A = {
				"to": {
					"phone":"233207508668",
					"message": "Please deliver the goods at the mall"
				},
				"subjectReference": REFERENCE,
				"startDateTime":self.MakeConnectionTest.time(str(datetime.datetime.now()))
	
				}
REQUEST_B = 	{
				"from":{
						"phone":"233207508668",
						"message": "This is the place we call home"
						},
						"subjectReference":REFERENCE_1,
						"startDateTime":self.MakeConnectionTest.time(str(datetime.datetime.now()))

						}



class AuthenticationTest(unittest.TestCase):
	def setUp(self):
		self.uri = "http://api.callectiv.com/authentication"

	def test_get(self):
		""" Send an authentication request with a GET method"""
		headers = {'Content-Type':APPL_JSON}
		response = requests.get(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsNot(response.status_code, OK)

	def test_post_json_with_default_accept_header(self):
		headers = {'Content-Type':APPL_JSON}
		response = requests.post(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsValidXMLResponse(response)

	def test_post_json_with_xml_accept_header(self):
		headers = {'Content-Type':APPL_JSON, 'Accept':APPL_XML}
		response = requests.post(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsValidXMLResponse(response)


	def test_post_json_with_json_accept_header(self):
		headers = {'Content-Type':APPL_JSON, 'Accept':APPL_JSON}
		response = requests.post(self.uri, data=json.dumps(AUTH), headers=headers)
		self.assertIsValidJSONResponse(response)

	def assertIsValidXMLResponse(self, response):
		self.assertEqual(response.status_code, OK)
		root_xml = etree.fromstring(response.content)
		self.assertEqual(root_xml.tag, 'authorization')
		self.assertIsNotNone(root_xml.attrib.get('expiryTime', None))
		self.assertIsNotNone(root_xml.find('token'))

	def assertIsValidJSONResponse(self, response):
		self.assertEqual(response.status_code, OK)
		self.assertIsNotNone(response.json().get('token', None))
		self.assertIsNotNone(response.json().get('@expiryTime', None))


class CallectivTestCase(unittest.TestCase):
	def setUp(self):
		uri = 'http://api.callectiv.com/authentication'
		headers = {'Content-Type':APPL_JSON, 'Accept':APPL_JSON}
		response = requests.post(uri, data=json.dumps(AUTH), headers=headers)
		self.token = json.loads(response.content).get('token')


class RegisterSubjectTest(CallectivTestCase):
	
	def test_post_json_request(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Content-Type':APPL_JSON,'Authorization':self.token}

		response =requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_post_json_requset_without_content_type(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Authorization':self.token}
		response = requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertIsNot(response.status_code, OK)

	def test_post_json_without_auth(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Content-Type':APPL_JSON}
		response = requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_xml_request(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Content-Type':APPL_XML,'Authorization':self.token}
		response = requests.post(url, data=json.dumps(REQUEST_BODY_XML),headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_xml_request_without_content_type(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Authorization':self.token}
		response = requests.post(url, data=json.dumps(REQUEST_BODY_XML), headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_xml_without_auth(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Content-Type':APPL_XML}
		response = requests.post(url, data=json.dumps(REQUEST_BODY_XML), headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_json_with_request_body_1(self):
		url = "http://api.callectiv.com/subject"
		headers = {'Content-Type':APPL_JSON,'Authorization':self.token}
		response = requests.post(url, data=json.dumps(REQUEST_BODY_1), headers=headers)
		self.assertEqual(response.status_code, OK)






class GetSubjectDetailsTest(CallectivTestCase):
	def test_post(self):
		url = 'http://api.callectiv.com/subject/12345'
		headers = {'Authorization':self.token}
		response = requests.post(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)
		self.assertNotEqual(response.content, None)

	def test_get_default_response(self):
		url = 'http://api.callectiv.com/subject/12345'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		root_xml = etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertEqual(root_xml.tag, 'subject')
		self.assertIsNotNone(root_xml.find('creationDateTime'))
		self.assertIsNotNone(root_xml.find('message'))

	def test_get_json_response(self):
		url = 'http://api.callectiv.com/subject/12345'
		headers = {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.get(url, headers=headers)
		response_content = response.content
		json_response = json.loads(response_content)
		self.assertIsNotNone(json_response)
	

		self.assertIsNotNone(json_response)
		self.assertEqual(json_response.get('message'), u'Callactiv Test')
		self.assertEqual(json_response.get('reference'), '12345')
		self.assertEqual(json_response.get('contact')['phone'], '0207508668')

	def test_get_without_auth(self):
		url = 'http://api.callectiv.com/subject/12345'
		headers =  {'Accept':APPL_JSON}
		response = requests.get(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_get_without_subject_reference(self):
		url = 'http://api.callectiv.com/subject/'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		self.assertEqual(response.status_code, OK)



class GetConnectionsSubject(CallectivTestCase):
	def test_get_json_response(self):
		url = 'http://api.callectiv.com/subject/12345/connections'
		headers = {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.get(url, headers=headers)
		content = response.content
		json_response = json.loads(content)
		self.assertIsNotNone(json_response)

	def test_get_xml_response(self):
		url = 'http://api.callectiv.com/subject/12345/connections'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		root_xml = etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertEqual(root_xml.tag, 'connections')
		self.assertIsNotNone(root_xml.find('connections'))
		self.assertIsNotNone(root_xml.find('id'))
		self.assertIsNotNone(root_xml.find('subjectReference'))


class ChangeSubjectStatus(CallectivTestCase):
	def test_put_method_with_json(self):
		url = 'http://api.callectiv.com/subject/12345/status/enabled'
		headers = {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.put(url, headers=headers)
		content = response.content
		json_response = json.loads(content)
		self.assertEqual(response.status_code, OK)
		self.assertIsNotNone(json_response)
		self.assertEqual(json_response.get('reference'),'12345')
		self.assertEqual(json_response.get('contact')['phone'],'0207508668')
		self.assertIsNotNone(json_response.get('message'))
		self.assertIsNotNone(json_response.get('creationDateTime'))
		self.assertEqual(json_response.get('status'), 'enabled')


	def test_mehod_with_xml(self):
		url = 'http://api.callectiv.com/subject/12345/status/enabled'
		headers = {'Authorization':self.token, 'Accept':APPL_XML}
		response = requests.put(url, headers=headers)
		root_xml =etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertIsNotNone(root_xml.find('message'))
		self.assertIsNotNone(root_xml.find('reference'))
		self.assertIsNotNone(root_xml.find('contact'))
		self.assertIsNotNone(root_xml.find('creationDateTime'))

	def test_put_method_with_disabled_status(self):
		url =  'http://api.callectiv.com/subject/12345/status/disabled'
		headers =  {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.put(url, headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_put_without_auth(self):
		url = 'http://api.callectiv.com/subject/12345/status/disabled'
		headers = {'Accept':APPL_JSON}
		response = requests.put(url,headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_put_with_disabled_status(self):
		url = url = 'http://api.callectiv.com/subject/12345/status/disabled'
		headers =  {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.put(url, headers=headers)
		content = response.content
		json_response = json.loads(content)
		self.assertIsNotNone(json_response)
		self.assertEqual(json_response.get('status'), 'disabled')


class DeleteSubjectTest(CallectivTestCase):

	def test_delete_with_wrong_reference(self):
		url = 'http://api.callectiv.com/subject/000000'
		headers = {'Authorization':self.token}
		response = requests.delete(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_delete_with_reference(self):
		url = 'http://api.callectiv.com/subject/12345'
		headers = {'Authorization':self.token}	
		response = requests.delete(url, headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_delete_without_auth(self):
		url = 'http://api.callectiv.com/subject/1234'
		response = requests.delete(url)
		self.assertNotEqual(response.status_code, OK)

	def test_delete_without_subject(self):
		url =  'http://api.callectiv.com/subject/1234'
		headers =  {'Authorization':self.token}	
		response = requests.delete(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)


class MakeConnectionTest(CallectivTestCase):

	def test_connection(self):
		url = 'http://api.callectiv.com/connection'
		headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
		response = requests.post(url, headers=headers, data=json.loads(REQUEST_A))
		self.assertEqual(response.status_code, OK)
		


	def time(self, text):
		date = parser.parse(text)
		return date.isoformat()


if __name__ == "__main__":
	unittest.main()


