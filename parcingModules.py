import requests
import re
import translateModules
from bs4 import BeautifulSoup

def postRegRu(mail, idd, mode):
	attemp = 0
	while attemp<3:
		if mode == 'mail':
			domain = mail.split('@')[1]
		elif mode == 'link':
			mail.replace("http://", '').replace("https://", '')
			domain = mail.split('/')[1]
		proxy = {'https':'socks5://Gea6AX:1YckDX@91.195.125.86:8000/',
		'http':'socks5://Gea6AX:1YckDX@91.195.125.86:8000/'}
		headers = {
	    'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
	    }
		s = requests.Session()
		s.proxies = proxy
		s.headers = headers
		while True:
			r = s.get("https://www.reg.ru/whois/"+domain, timeout=(10, 10), stream=True)
			if r.status_code == 200:
				break
		soup = BeautifulSoup(r.text, "html.parser")
		data = soup.findAll('td', class_='b-table__cell b-table__cell_type_content b-table__cell_node_first')
		data = str(data)
		if not(data.find("Registrant Organization:")==-1) or not(data.find("Администратор домена:")==-1):
			if not(data.find("Registrant Organization:")==-1):
				data = data.split('Registrant Organization:')[1]
				data = "Registrant Organization:" + data.split("Registrant Email:")[0]
				data = data.replace("<br>", "\n").replace("<br/>", '\n').replace("</a>", "")
				data = re.sub(r'<.*?>', '', data)
				data = data.replace('\n', '`\n').replace(': ', ': `')
				for i in range(len(data.split('\n'))-1):
					textToBeTranslated = str(re.search(r"(\w+:|\w+ \w+:|\w+ \w+\/\w+:)", data.split('\n')[i]).expand(r"\1"))
					data.replace((textToBeTranslated), (translateModules.translate(textToBeTranslated)))
			text = "Сайт принадлежит компании\n"+data
			break
		elif attemp==2:
			text = "Сайт принадлежит частному лицу"
		attemp+=1
		s.close()
	return text