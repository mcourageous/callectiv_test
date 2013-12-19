import requests
import unittest
from requests_runscope import RunscopeAdapter
import json
from xml.etree import ElementTree as etree 
import StringIO
import dateutil.parser as parser
import datetime

AUTH =  {"apikey":"xxxxxxxxx", "secret":"xxxxxxxxxxx"}
APPL_JSON = 'application/json'
APPL_XML = 'application/xml'
OK = 200
REFERENCE = "12345"
REFERENCE_1 = "67890"

class AuthenticationTest(unittest.TestCase):
	def setUp(self):
		# self.uri = "http://api.callectiv.com/authentication"
		self.uri = "http://api-callectiv-com-u453h6ad29k7.runscope.net/authentication"



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
		# uri = 'http://api.callectiv.com/authentication'
		uri = "http://api-callectiv-com-u453h6ad29k7.runscope.net/authentication"
		headers = {'Content-Type':APPL_JSON, 'Accept':APPL_JSON}
		response = requests.post(uri, data=json.dumps(AUTH), headers=headers)
		self.token = json.loads(response.content).get('token')


class RegisterSubjectTest(CallectivTestCase):
	
	def test_post_json_request(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
		REQUEST_BODY =  {"reference":REFERENCE,
				"contact":{"phone":"0207508668"},
				"message":"Callactiv Test"
				} 
		response =requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_post_json_requset_without_content_type(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Authorization':self.token}
		REQUEST_BODY =  {"reference":REFERENCE,
				"contact":{"phone":"0207508668"},
				"message":"Callactiv Test"
				} 
		response = requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertIsNot(response.status_code, OK)

	def test_post_json_without_auth(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Content-Type':APPL_JSON}
		REQUEST_BODY =  {"reference":REFERENCE,
				"contact":{"phone":"0207508668"},
				"message":"Callactiv Test"
				} 
		response = requests.post(url, data=json.dumps(REQUEST_BODY), headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_xml_request(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Content-Type':APPL_XML,'Authorization':self.token}
		REQUEST_BODY_XML = """ 
		<subject>
		<reference>12345</reference>
		<contact>
		<phone> 0207508668</phone>
		</contact>
		<message> Callactiv Test</message>
		</subject>	"""
		response = requests.post(url, data=REQUEST_BODY_XML, headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_post_xml_request_without_content_type(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Authorization':self.token}
		REQUEST_BODY_XML = """ 
		<subject>
		<reference>12345</reference>
		<contact>
		<phone> 0207508668</phone>
		</contact>
		<message> Callactiv Test</message>
		</subject>	"""
		response = requests.post(url, data=REQUEST_BODY_XML, headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_xml_without_auth(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Content-Type':APPL_XML}
		REQUEST_BODY_XML = """ 
		<subject>
		<reference>12345</reference>
		<contact>
		<phone> 0207508668</phone>
		</contact>
		<message> Callactiv Test</message>
		</subject>	
			"""
		response = requests.post(url, data=json.dumps(REQUEST_BODY_XML), headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_post_json_with_request_body_1(self):
		# url = "http://api.callectiv.com/subject"
		url = "http://api-callectiv-com-u453h6ad29k7.runscope.net/subject"
		headers = {'Content-Type':APPL_JSON,'Authorization':self.token}
		REQUEST_BODY_1 =  {"reference":REFERENCE,
					"contact":{"phone":"0207508668"},
					"message":"Call Test"
				  } 
		response = requests.post(url, data=json.dumps(REQUEST_BODY_1), headers=headers)
		self.assertEqual(response.status_code, OK)


class GetSubjectDetailsTest(CallectivTestCase):
	def test_post(self):
		# url = 'http://api.callectiv.com/subject/12345'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345'
		headers = {'Authorization':self.token}
		response = requests.post(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)
		self.assertNotEqual(response.content, None)

	def test_get_default_response(self):
		# url = 'http://api.callectiv.com/subject/12345'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		root_xml = etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertEqual(root_xml.tag, 'subject')
		self.assertIsNotNone(root_xml.find('creationDateTime'))
		self.assertIsNotNone(root_xml.find('message'))

	def test_get_json_response(self):
		# url = 'http://api.callectiv.com/subject/12345'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345'
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
		# url = 'http://api.callectiv.com/subject/12345'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345'
		headers =  {'Accept':APPL_JSON}
		response = requests.get(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_get_without_subject_reference(self):
		# url = 'http://api.callectiv.com/subject/'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		self.assertEqual(response.status_code, OK)


class GetConnectionsSubject(CallectivTestCase):
	def test_get_json_response(self):
		# url = 'http://api.callectiv.com/subject/12345/connections'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/connections'
		headers = {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.get(url, headers=headers)
		content = response.content
		json_response = json.loads(content)
		self.assertIsNotNone(json_response)

	def test_get_xml_response(self):
		# url = 'http://api.callectiv.com/subject/12345/connections'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/connections'
		headers = {'Authorization':self.token}
		response = requests.get(url, headers=headers)
		root_xml = etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertEqual(root_xml.tag, 'connections')
		# self.assertIsNotNone(root_xml.find('connections'))
		self.assertIsNotNone(root_xml.find('id'))
		self.assertIsNotNone(root_xml.find('subjectReference'))


class ChangeSubjectStatus(CallectivTestCase):
	def test_put_method_with_json(self):
		# url = 'http://api.callectiv.com/subject/12345/status/enabled'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/status/enabled'
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
		# url = 'http://api.callectiv.com/subject/12345/status/enabled'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/status/enabled'
		headers = {'Authorization':self.token, 'Accept':APPL_XML}
		response = requests.put(url, headers=headers)
		root_xml =etree.fromstring(response.content)
		self.assertEqual(response.status_code, OK)
		self.assertIsNotNone(root_xml.find('message'))
		self.assertIsNotNone(root_xml.find('reference'))
		self.assertIsNotNone(root_xml.find('contact'))
		self.assertIsNotNone(root_xml.find('creationDateTime'))

	def test_put_method_with_disabled_status(self):
		# url =  'http://api.callectiv.com/subject/12345/status/disabled'
		url =  'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/status/disabled'
		headers =  {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.put(url, headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_put_without_auth(self):
		# url = 'http://api.callectiv.com/subject/12345/status/disabled'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/status/disabled'
		headers = {'Accept':APPL_JSON}
		response = requests.put(url,headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_put_with_disabled_status(self):
		# url = 'http://api.callectiv.com/subject/12345/status/disabled'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345/status/disabled'
		headers =  {'Authorization':self.token, 'Accept':APPL_JSON}
		response = requests.put(url, headers=headers)
		content = response.content
		json_response = json.loads(content)
		self.assertIsNotNone(json_response)
		self.assertEqual(json_response.get('status'), 'disabled')


class DeleteSubjectTest(CallectivTestCase):
	def test_delete_with_wrong_reference(self):
		# url = 'http://api.callectiv.com/subject/000000'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/000000'
		headers = {'Authorization':self.token}
		response = requests.delete(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)

	def test_delete_with_reference(self):
		# url = 'http://api.callectiv.com/subject/12345'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/12345'
		headers = {'Authorization':self.token}	
		response = requests.delete(url, headers=headers)
		self.assertEqual(response.status_code, OK)

	def test_delete_without_auth(self):
		# url = 'http://api.callectiv.com/subject/1234'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/1234'
		response = requests.delete(url)
		self.assertNotEqual(response.status_code, OK)

	def test_delete_without_subject(self):
		# url =  'http://api.callectiv.com/subject/1234'
		url =  'http://api-callectiv-com-u453h6ad29k7.runscope.net/subject/1234'
		headers =  {'Authorization':self.token}	
		response = requests.delete(url, headers=headers)
		self.assertNotEqual(response.status_code, OK)


class MakeConnectionTest(CallectivTestCase):
	def test_connection_with_request_A(self):
		# url = 'http://api.callectiv.com/connection'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/connection'
		headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
		REQUEST_A = {
		"to": {
		"phone":"233207508668",
		"message": "Please deliver the goods at the mall"
		},
		"subjectReference": REFERENCE,
		"startDateTime":"2012-06-11T04:29:22+0100"
	
		}
		response = requests.post(url, headers=headers, data=json.dumps(REQUEST_A))
		self.assertEqual(response.status_code, OK)

	def test_connection_with_request_B(self):
		# url = 'http://api.callectiv.com/connection'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/connection'
		headers = {'Content-Type':APPL_JSON, 'Authorization':self.token}
		REQUEST_B ={
		"from":{
		"phone":"233207508668",
		"message": "This is the place we call home"
		},
		"subjectReference":REFERENCE_1,
		"startDateTime":"2012-06-11T04:29:22+0100"
		}
		response = requests.post(url, headers=headers, data=json.dumps(REQUEST_B))
		self.assertEqual(response.status_code, OK)

	def test_connection_xml_A(self):
		# url = 'http://api.callectiv.com/connection'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/connection'
		headers = {'Content-Type':APPL_XML, 'Authorization':self.token}
		REQUEST_A = """
		<connection>
  		<to>
 		<phone>233207508668</phone>
 		<message>This is JobWorld. We have the recruiter for the Python Developer job on the line.</message>
  		</to>
  		<subjectReference>12345</subjectReference>    
 		<startDateTime>2012-06-11T04:20:22+0100</startDateTime>
		</connection>
		"""
		response = requests.post(url, headers=headers, data=REQUEST_A)
		self.assertEqual(response.status_code, OK)

	def test_connection_xml_B(self):
		# url = 'http://api.callectiv.com/connection'
		url = 'http://api-callectiv-com-u453h6ad29k7.runscope.net/connection'
		headers = {'Content-Type':APPL_XML, 'Authorization':self.token}
		REQUEST_B =""" <connection>
   		 <from>
    	<phone>233243638773</phone>
    	<message>This is VacationLets. You have a call from the homeowner of the house on Brighton beach.</message>
   		 </from>
    	<subjectReference>67890</subjectReference>
   		<startDateTime>2012-06-11T04:29:22+0100</startDateTime>
		</connection>
		"""
		response = requests.post(url, headers=headers,data=REQUEST_B)
		self.assertEqual(response.status_code, OK)

class GetConnectionDetailsTest(CallectivTestCase):

	def test_get(self):
		""" Connection details test cannot be completed because 
		it needs an id from GetConnectionsForSubject which returns None
		"""
		url = 'http://api.callectiv.com/connection/{connectionId'
		headers  = {'Authorization':self.token}
		response = requests.get(url,headers=headers)

	def test_get_without_auth(self):
		pass
		

class GetConnectionStatus(CallectivTestCase):
	""" Get Connection Details requires an id parameter from GetConnectionsSubject
	which returns a None type
	"""

	def test_get(self):
		url = url = 'http://api.callectiv.com/connection/{connectionId'
		response = requests.get(url)

		

class CancelConnection(CallectivTestCase):
	""" Cancel Connection requires an id parameter from GetConnectionsSubject.
	GetConnectionsForSubject returns None type
	"""



def time(self, text):
	date = parser.parse(text)
	return date.isoformat()







if __name__ == "__main__":
	unittest.main()


