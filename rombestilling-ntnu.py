#Skript for automatisk bestilling av rom 2 uker frem i tid. Tiden da nye rom blir lagt ut
#Skriptet er for tp.uio.no/ntnu
#
#Lokasjonesvariabelen for Gjovik er:
#	area=50000
#
#Bygningskodene er som folger:		#Kan finnes ut gjennom tp.uio.no/ntnu i kildekoden
#	Ametyst : 501
#	Beryll 	: 504
#	Gneis	: 503
#	Helvin	: 505
#	Kobolt	: 502
#	Smaragd	: 510
#
#Lokasjone og rom er sammenslaaing av bygg og rom. Eksempel : 502K112, for k bygget med rom k112
#
romogbygg = '502K112'		#Bestemmer bygg og rom
starttid = '08:00'		#Klokkeslettformatet : 08:00
varigheten = '01:00'		#Varigheten. Format som klokka, men er antall timer og min som skal leies
				#Eksempel er format for 1 timer er : 01:00

from lxml import html
import requests
import ConfigParser	#For bruker og pass lesing fra fil
config = ConfigParser.RawConfigParser()
config.read('login.cfg')	#Henter passord og brukernavn fra fil. Her defineres lokasjonen
user = config.get('section1', 'user')
passw = config.get('section1', 'pass')



####################################################################################################
#Skaffer datoen to uker frem i tid
import datetime
from datetime import timedelta

now = datetime.datetime.now()		#For naatiden
diff = datetime.timedelta(days=14)	#legger til 14 dager aka 2 uker
future = now + diff			#Lager datoen som er om 2 uker

bestillingsdato = future.strftime("%Y-%m-%d")	#Lagrer det i riktig tidsformat

###################################################################################################




def bestill():
	c=requests.Session()
	url0 = 'https://tp.uio.no/ntnu/rombestilling/'
        url2 = 'https://tp.uio.no/ntnu/rombestilling/'

#####################################################################################################
	#For aa lagre cookies i variabel
		#laster inn sidne for aa skaffe cookies og token som brukes
		#i post requesten for aa logge inn gjenom feide
	data0 = {}			#Tom liste for post requesten
	a = c.get(url0)			#Selve post requesten
	SAML = c.cookies['SimpleSAMLSessionID']
	PHPSE = c.cookies['PHPSESSID']
	#print PHPSE

		#for aa skaffe riktig token og url hentes dette fra en nettside
		#Travaserer svaret fra server og henter ut token
	tree = html.fromstring(a.content)
	test = tree.xpath('//*[@id="languageSelector"]/input[2]/@value')
	test2 = ''.join(test)
	#print test2


######################################################################################################

	#skaffer lenden til teksten, forde den trengs for aa sende nummer paa lengden ogsaa
	AUTESTATE = test2
	ASLENGHT = len(AUTESTATE)	#teller karakterer i token AUTESTATE

		#url for innlogging som bruker token som er hentet tidligere
        url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=282&AuthState=_' + AUTESTATE + '&org=ntnu.no'

	login_data = {
		'asLen': ASLENGHT,
		'AuthState': test2,
		'org': 'ntnu.no',
		'has_js': 'true',
		'inside_iframe': '0',
		'feidename': user,
		'password': passw
		}
	svar = c.post(url, data=login_data) #loging in


#####################################################################################################
	#print svar.content	#For debuging

		#pga ikke javascript er i bruk i scriptet maa man innom en ekstra side for workaround
		#token fra svaren man fikk paa forje request
	tree2 = html.fromstring(svar.content)
        noJavascript = tree2.xpath('/html/body/form/input[2]/@value')
	noJavascript = ''.join(noJavascript)


	noJsData = {
			'SAMLResponse': noJavascript,
			'RelayState': 'https://tp.uio.no/ntnu/rombestilling/?'

		}
	noJsURL = 'https://tp.uio.no/simplesaml/module.php/saml/sp/saml2-acs.php/feide-sp'
	nadaJS = c.post(noJsURL, noJsData)

	#print nadaJS.content

###################################################################################################


	#for bestilling for aa faa tokenrb
		#Requeste en side med sok paa rom for aa faa token som brukes paa selve bestillingen
        beforebestill = {
                'start': starttid,	#Naar bestillingen starter
                'size': '5',
                'roomtype': 'NONE',
                'duration': varigheten,	#Hvor lenge man skal ha rommet. Starter fra start
                'area': '50000',	#Spesifiserer Gjovik
                #'room[]': '502k112',	#Byggning og rom
                #'building': "502",	#k bygget
                'preset_date': bestillingsdato,
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

#################################################################################################



	#bestill
		#Selve bestillingen og de parametere man trenger
        bestill = {
		'name': "",
		'note': "",
		'confirmed': 'true',
		'start': starttid,	#Naar tiden paa rommet starter
		'size': '5',
		'roomtype': 'NONE',
		'duration': varigheten,	#Hvor lenge man har rommet.
		'area': '50000',	#Spesifiserer Gjovik
		'room[]': romogbygg,	#Spesifiserer bygg og rom
		#'building': "502",	#Skript fungerer uten   #Spesifiserer bygg
		#'preset_day': 'WED',	#Skript fungerer uten
		'preset_date': bestillingsdato,
		'exam': "",
		'dates[]': bestillingsdato,
		'tokenrb': token,
	}
        r = c.post(url2, data=bestill)      #Sending bestill
        svar = c.post(url2, data=bestill)      #Sending bestill
	#print svar.content	"brukes for debug
bestill()


