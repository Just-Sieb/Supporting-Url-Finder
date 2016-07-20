import requests
from html.parser import HTMLParser
import logging

logger = logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')

class LinkFinder(HTMLParser):
	
	def __init__(self, domain, spider = True):	
		HTMLParser.__init__(self)
		
		self.url_scanned = domain
		self.base_url = None
		self.spider = spider

		self.url_html = None

		self.urls = []
		self.urls_href = []
		self.urls_src = []
		self.urls_img = []
		self.urls_css = []
		self.urls_js = []
		self.urls_a = []
		self.urls_unique_domains = []
		self.suggest_urls = []
			
	def curl_website(self):
		#todo: Switch to regex
		if self.url_scanned[0:6] != "http://" or self.url_scanned[0:7] != "https://":
			self.url_scanned = "http://" + self.url_scanned

		r = requests.get(self.url_scanned)
		if r.status_code is not requests.codes.ok:
			logging.error("When try to get page got " + str(r.status_code))
			raise http_error

		self.feed(r.text)


	# This is the the main function that finds the urls
	# When you run the inhertited feed function of the class it will call this function
	# for each start tag in the html doc.
	def handle_starttag(self, tag, attrs):
		if tag == "img":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
		elif tag == "link":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
		elif tag == "script":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
		elif tag == "a":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls_a.append(item[1])
		elif tag == "base":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
					self.base_url = item[1]
		elif tag == "frame":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
		elif tag == "iframe":
			for item in attrs:			
				if (item[0] == "href") or (item[0] == "src"):
					self.urls.append(item[1])
		pass
	
	# After running the feed function, call this function to run the analysis.
	# WIP
	def analyze(self):
		logging.info("Stated analyzer for " + self.url_scanned)

		self.curl_website()
		if self.spider:
			self.spider_urls()
		self.normalize_all_urls()
		self.get_unique_domains()
		
		pass	

	def normalize_all_urls(self):
		for url in self.urls:
			if (url[0:6] != "http://") and (url[0:7] != "https://") and (len(url) != 0):
				if url[0] == "/":
					if self.base_url is None:
						url = self.url_scanned + url	
					else:
						url = self.base_url + url
				else:
					if self.url_scanned[-1] == "/":
						url = self.url_scanned + url
					else:
						url = self.url_scanned[0:-2] + url
		pass
	
	# Removes email and phone number urls
	# WIP
	def remove_junk_urls(self):
		pass

	# this function is to create a full url if it is only give the directory
	# example: if facebook has the url "/profile/this_person" then it will
	# return the url facebook.com/profile/this_person
	# WIP
	def normalize_url(self, url):
		pass
		
	def get_domain(self, url):
		return url.split("//")[-1].split('/')[0]
		


	def get_unique_domains(self):
		for url in self.urls:
			domain = self.get_domain(url)
			if domain not in self.urls_unique_domains:
				self.urls_unique_domains.append(domain)
		pass
	
	# WIP
	def get_domain_percentage(self):
		pass
	
	# WIP
	def predict_importance(self):
		pass
	
	# Future Feature: run the analysis on subpages on the domain to get more accurate results
	# WIP
	def spider_urls(self):
		for url in self.urls_a: #these will all be link
			if self.get_domain(url) == self.url_scanned:
				logging.info("Spidering: " + url)
				page = LinkFinder(url, spider=False) #todo: make this multithreaded
				page.analyze()
				for spider_url in page.urls:
					self.urls.append(spider_url)
