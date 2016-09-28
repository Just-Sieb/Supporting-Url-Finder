from linkanalyzer import LinkFinder
import cProfile

print("Enter the url you want to test: ")
url = input()


site = LinkFinder(url, spider=1)

#for url in site.urls:
#	print(url)
