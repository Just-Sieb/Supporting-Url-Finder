from linkanalyzer import LinkFinder
from threading import Thread
from collections import deque
import time
import logging


logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')


class ProcessManager(Thread):

    def __init__(self, init_url):
        Thread.__init__(self)
        self.count = 100
        self.max_urls_reached = False
        self.urls_to_scan = deque()

        self.more_threads_available = True
        self.active_threads = 0
        self.number_of_threads_created = 0


        self.potential_urls = []
        self.urls_unique_domains = []
        self.url_freq = dict()
        self.url_percentage = dict()

        self.urls_scanned = set()
        self.continue_scanning = True

        self.init_url = init_url


    def run(self):
        logging.info("Starting url analyzer for %s", self.init_url)
        self.start_process(self.init_url)
        pass

    def build_list(self):
        pass


    def add_urls_to_list(self, scan_urls, potential_urls):
        for url in scan_urls:
            if url not in self.urls_scanned:
                self.urls_to_scan.append(url)

        for url in potential_urls:
            self.potential_urls.append(url)


    def start_process(self, url):
        if self.continue_scanning and not self.max_urls_reached:
            if url not in self.urls_scanned:
                self.count -= 1
                if self.count == 0:
                    self.max_urls_reached = True
                self.urls_scanned.add(url)
                p = Thread(target=self.start_analyser, args=(url,))
                p.start()
                self.active_threads += 1
        else:
            pass


    def start_analyser(self, url):
        #logging.info("Started new thread. Number of active threads %d", self.active_threads)
        self.number_of_threads_created += 1
        lf = LinkFinder(url)
        lf.analyze()
        self.add_urls_to_list(lf.urls_a ,lf.normalized_urls)
        self.process_manager()
        self.active_threads -= 1


    def process_manager(self):
        # We test if active threads is equal to one because this will be in an active thread
        if (self.count == 0 or len(self.urls_to_scan) == 0) and self.active_threads == 1:
            logging.info("Closing Thread manager")
            logging.info("Number of threads created: %d", self.number_of_threads_created)
            self.analyze_potential_urls()
            self.continue_scanning = False
        else:
            if self.active_threads < 100:
                self.more_threads_available = True
            while self.more_threads_available:
                try:
                    url = self.urls_to_scan.popleft()
                except:
                    break
                
                self.start_process(url)

                if self.active_threads > 100:
                    self.more_threads_available = False


    def analyze_potential_urls(self):
        self.get_unique_domains()
        self.get_domain_percentage()
        pass


    def get_domain(self, url):
        domain = None
        try:
            domain = url.split("//")[1].split('/')[0]
        except IndexError:
            domain = url.split("//")[-1].split('/')[0]
        if domain == "":
            logging.info("URL: %s", url)
        return domain


    def get_unique_domains(self):
        for url in self.potential_urls:
            domain = self.get_domain(url)

            if url != "" and url is not None:
                #logging.info("Url Length: %d - Url: %s", len(url), url)
                if domain not in self.urls_unique_domains:
                    self.urls_unique_domains.append(domain)
                    self.url_freq[domain] = 1
                else:
                    self.url_freq[domain] += 1


    def get_domain_percentage(self):
        total_count = 0
        for key, value in self.url_freq.items():
            total_count += value

        for key in self.url_freq:
            count = self.url_freq[key]
            self.url_percentage[key] = (count * 100) / total_count
            #logging.info("Percentage for " + key + ": " + str(self.url_precentage[key]))