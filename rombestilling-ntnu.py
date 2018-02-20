#Maa finne ut hvordan man bruker eksisterende cookies
from lxml import html
import requests

def bestill():
	c=requests.Session()
	url0 = 'https://tp.uio.no/ntnu/rombestilling/'
        url2 = 'https://tp.uio.no/ntnu/rombestilling/'



	#For aa lagre cookies i variabel
	data0 = {}
	a = c.get(url0)
	SAML = c.cookies['SimpleSAMLSessionID']
	PHPSE = c.cookies['PHPSESSID']
	#print PHPSE

	#for aa skaffe riktig token og url hentes dette fra en nettside
	tree = html.fromstring(a.content)
	test = tree.xpath('//*[@id="languageSelector"]/input[2]/@value')
	test2 = ''.join(test)
	#print test2












	#skaffer lenden til teksten, forde den trengs for aa sende nummer paa lengden ogsaa
	AUTESTATE = test2
	ASLENGHT = len(AUTESTATE)

        url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=282&AuthState=_' + AUTESTATE + '&org=ntnu.no'

	login_data = {
		'asLen': ASLENGHT,
		'AuthState': test2,
		'org': 'ntnu.no',
		'has_js': 'true',
		'inside_iframe': '0',
		'feidename': 'USERNAME',
		'password': 'PASSWORD'
		}
        #print c.cookies

	svar = c.post(url, data=login_data) #loging in

	#print svar.content

	#pga ikke javascript
	tree2 = html.fromstring(svar.content)
        noJavascript = tree2.xpath('/html/body/form/input[2]/@value')
	noJavascript = ''.join(noJavascript)
	#print noJavascript


	noJsData = {
			'SAMLResponse': noJavascript,
			'RelayState': 'https://tp.uio.no/ntnu/rombestilling/?'

		}
	noJsURL = 'https://tp.uio.no/simplesaml/module.php/saml/sp/saml2-acs.php/feide-sp'
	nadaJS = c.post(noJsURL, noJsData)

	#print nadaJS.content





	#for bestilling for aa faa tokenrb
	#bestill
        beforebestill = {
                'start': '08:00',
                'size': '5',
                'roomtype': 'NONE',
                'duration': '01:00',
                'area': '50000',
                'room[]': '502k112',
                'building': "502",	#k
                'preset_date': '2018-02-28',
                'exam': "",
		'submitall': 'Bestill'
        }
        svar = c.post(url2, data=beforebestill)      #Sending bestill
        #print svar.content

	tree3 = html.fromstring(svar.content)
        token = tree3.xpath('//*[@id="origform"]/input[11]/@value')	#pass paa input nummer kan endre seg
        #print token
	token = ''.join(token)
	#print token





	#bestill
        bestill = {
		'name': "",
		'note': "",
		'confirmed': 'true',
		'start': '08:00',
		'size': '5',
		'roomtype': 'NONE',
		'duration': '01:00',
		'area': '50000',
		'room[]': '502K112',
		'building': "502",
		'preset_day': 'WED',
		'preset_date': '2018-02-28',
		'exam': "",
		'dates[]': '2018-02-28',
		'tokenrb': token,
	}
        r = c.post(url2, data=bestill)      #Sending bestill
        svar = c.post(url2, data=bestill)      #Sending bestill
	print svar.content

	#r = c.get(url)
bestill()

