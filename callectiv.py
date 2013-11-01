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

REQUEST_BODY_XML_1 =  """ <subject>
						<reference>12345</reference>
						<contact>
						<phone> 0207508668</phone>
						</contact>
						<message> Call Test</message>
						</subject>
					"""


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
		self.assertIsNotNone(root_xml.find('connection'))
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
		self.assertIsNotNone(root_xml.find(''))

		






	


	
		

























		

		# headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
		# request = requests.post(url, data=json.dumps(request_body), headers=headers)
		# self.assertEqual(request.status_code, OK)
		# response =requests.get("http://api.callectiv.com/subject/12345", headers=headers)
		# json_response = json.loads(response.content)
		# self.assertEqual(json_response.get("message"), u"Callactiv Test")
		# self.assertEqual(json_response.get("reference"), "12345")
		# self.assertEqual(json_response.get("contact")["phone"], "0207508668")
		

# class GetConnectionsForSubjectTests(CallectivTestCase):
# 	def test_connections_default_accept_type(self):

# 		url = "http://api.callectiv.com/subject/12345/connections"
# 		headers = {'Content-Type':"application/xml", 'Authorization':self.token}
# 		subject = requests.get(url, headers=headers)
# 		self.assertEqual(subject.status_code, OK)
# 		self.assertEqual(etree.fromstring(subject.content).tag, "connections")

	# def test_connections_with_json_accept_type(self):

	# 	url = "http://api.callectiv.com/subject/12345/connections"
	# 	headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
	# 	response = requests.get(url, headers=headers)
	# 	self.assertEqual(response.status_code, OK)
	# 	self.assertIsNotNone(response.content)
	# 	output = json.loads(response.content)
	# 	self.assertIsNotNone(output)
		
	# def test_change_status_with_get_method(self):
	# 	"""test status change with wrong method """

	# 	url = "http://api.callectiv.com/subject/12345/status/enabled"
	# 	headers = {'Content-Type':APPL_JSON,"accept":APPL_JSON,'authorization':self.token}
	# 	response = requests.get(url, headers=headers)
	# 	self.assertNotEqual(response.status_code, OK)

	# def test_change_status_with_disabled_status(self):
	# 	url = "http://api.callectiv.com/subject/12345/status/disabled"
	# 	headers = {'Content-Type':APPL_JSON,"accept":APPL_JSON,'authorization':self.token}
	# 	response = requests.put(url,headers=headers)
	# 	self.assertEqual(response.status_code, OK)
	# 	response = requests.put(url,headers=headers)
	# 	self.assertIsNot(response.status_code, OK)




	# def test_delete_subject_with_reference(self):
	# 	""" check status code"""
	# 	url = "http://api.callectiv.com/subject/12345"
	# 	headers = {'Authorization':self.token}
	# 	delete =requests.delete(url, headers= headers)
	# 	self.assertEqual(delete.status_code, OK)
		
	# def test_delete_subject_with_wrong_reference(self):
	# 	"""check status code"""
	# 	url = "http://api.callectiv.com/subject/2347"
	# 	delete = requests.delete(url, headers=self.headers)
	# 	self.assertIsNot(delete.status_code, OK)

	# def time(self, text):
	# 	date = parser.parse(text)
	# 	return date.isoformat()


	# def test_make_connections(self):
	# 	url = "http://api.callectiv.com/connection"
	# 	headers = {'Content-Type':APPL_JSON,'Authorization':self.token}
	# 	time = self.time(str(datetime.datetime.now()))
	# 	request_a = {
	# 				"from":{
	# 					"phone":"23327508668",
	# 					"message":"Hello world"
	# 				},
	# 				"subjectReference":"12345",
	# 				"startDateTime": time}

	# 	request_b = {
	# 				"to":{
	# 					"phone":"23320755555",
	# 					"message":"How are you"
	# 				},
	# 				"subjectReference":"12345",
	# 				"startDateTime":time
	# 				}
	# 	request_a = requests.post(url, headers=headers, data=request_a)
	# 	request_b = requests.post(url, headers=headers, data=request_b)
	# 	self.assertEqual(request_a.status_code, OK)
	# 	self.assertEqual(request_b.status_code, OK)

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
