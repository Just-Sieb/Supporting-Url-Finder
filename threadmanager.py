from linkanalyzer import LinkFinder
from threading import Thread
import time
import logging


logger = logging.basicConfig(filename="url.log", level=logging.INFO, filemode='w', format='%(levelname)s: %(asctime)s - %(message)s')


class ProcessManager(Thread):

    def __init__(self, init_url):
        Thread.__init__(self)
        self.count = 50
        self.urls_to_scan = []

        self.active_threads = 0

        self.potential_urls = []
        self.urls_scanned = set()
        self.continue_scanning = True

        self.init_url = init_url
        pass


    def run(self):
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
        if self.continue_scanning:
            if url not in self.urls_scanned:
                self.count -= 1
                if self.count == 50:
                    self.continue_scanning = False
                self.urls_scanned.add(url)
                p = Thread(target=self.start_analyser, args=(url,))
                p.start()
                self.active_threads += 1
        else:
            pass


    def start_analyser(self, url):
        lf = LinkFinder(url)
        lf.analyze()
        self.add_urls_to_list(lf.urls_a ,lf.normalized_urls)
        self.active_threads -= 1
        self.process_manager()


    def process_manager(self):
        if self.count == 0 or len(self.urls_to_scan) == 0:
            self.analyze_potential_urls()
            self.continue_scanning = False
        else:
            for url in self.urls_to_scan:
                try:
                    self.start_process(url)
                except RuntimeError:
                    print("RuntimeError")
                    print(self.active_threads)




    def analyze_potential_urls(self):
        pass
