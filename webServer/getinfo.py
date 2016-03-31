import urllib2
url='http://192.168.0.120'
content = urllib2.urlopen(url).read()

print content
