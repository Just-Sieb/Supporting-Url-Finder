import requests
from requests import HTTPError
from requests.exceptions import InvalidURL, SSLError, MissingSchema, ConnectionError
from html.parser import HTMLParser
import logging
import re
#import yappi

logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')


class LinkFinder(HTMLParser):

	def __init__(self, domain, spider=0):
		HTMLParser.__init__(self)

		self.url_scanned = domain
		self.redirected_url = None
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
		self.normalized_urls = []

		self.status_code = None


	def curl_website(self):

		if self.url_scanned[0:7] != "http://" and self.url_scanned[0:8] != "https://":
			self.url_scanned = "http://" + self.url_scanned

		if self.url_scanned[-1] == "/":
			self.url_scanned = self.url_scanned[0:-1]

		header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}

		r = requests.get(self.url_scanned, headers=header, verify=False)
		self.status_code = r.status_code

		if self.status_code is not requests.codes.ok:
			logging.error("Page: %s = ERROR: %d ", self.url_scanned, r.status_code)
			raise HTTPError

		self.redirected_url = r.url

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
	def analyze(self):
		#print("Running analyzer")
		#count += 1
		#logging.info("Stated analyzer for " + self.url_scanned)

		try:
			self.curl_website()
		except HTTPError as err:
			logging.error("HTTPError")
			logging.error(err)
		except InvalidURL as err:
			logging.error(err)
		except SSLError as err:
			logging.error(err)
		except MissingSchema as err:
			logging.error(err)
		except ConnectionError as err:
			logging.error(err)



		self.remove_junk_urls()
		self.normalize_all_urls()


	def normalize_all_urls(self):
		for url in self.urls:
			self.normalized_urls.append(self.normalize_url(url))


	# this function is to create a full url if it is only give the directory
	# example: if facebook has the url "/profile/this_person" then it will
	# return the url facebook.com/profile/this_person
	def normalize_url(self, url):
		#logging.info("URL_BEFORE: " + url)
		if (url[0:7] != "http://") and (url[0:8] != "https://") and (len(url) != 0):
			#logging.info(url[0:2])
			if url[0:2] == "//":
				url = "http:" + url
			elif url[0] == "/":
				if self.base_url is None:
					url = self.url_scanned + url
				else:
					url = self.base_url + url
			elif url[0] == ".":
				if self.base_url is None:
					url = self.url_scanned + url[1:]
				else:
					url = self.base_url + url[1:]
			elif url[0] == "?":
				if self.base_url is None:
					url = self.url_scanned + "/" + url[1:]
				else:
					url = self.base_url + "/" + url[1:]
			else:
				if self.url_scanned[-1] == "/":
					url = self.url_scanned + url
				else:
					url = self.url_scanned[0:-2] + url

		#logging.info("URL_AFTER: " + url)
		return url

	# Removes email and phone number urls
	def remove_junk_urls(self):
		self.urls_a = [x for x in self.urls_a if not self.junk_url(x)]


	def junk_url(self, url):
		if url[0:11] == "javascript:":
			#logging.info("Removing junk url in list")
			return True
