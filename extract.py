import csv
import urllib2
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from DatumBox import DatumBox
datum_box = DatumBox("2a13913dda346761765020c1f66e34f8")
TAG_RE = re.compile(r"<[^>]+>")

color_number = {"Arts":1,"Business & Economy":2,"Computers & Technology":3,"Health":4,"Home & Domestic Life":5,"News":6,"Shopping":7,"Society":8,"Sports":9,"Recreation & Activities":10,"Reference & Education":11,"Science":12}

def fetch_page(site):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    # Perform a HTTP request by passing in our desired URL and setting our headers to equal
    # the headers that we've defined above.
    req = urllib2.Request(site, headers=hdr)

    try:
        # here we are going to open our desired page using urllib2.urlopen
        # and passing in our request object as a parameter and as a means of protection we
        # will surround this with a try except so that, should the script run into any errors
        # it will fail gracefully instead of just crashing.
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        # print out the HTTPError
        print e.fp.read()

    # lastly we will want to read the response which was generated by opening
    # the url and store it under content
    content = page.read()
    # and then print out this page.
    return content

def remove_tags(text):
    return TAG_RE.sub('', text)

def main(site):
    page = fetch_page(site)
    wordsNoTags = remove_tags(page)
    stop = set(stopwords.words('english'))
    arr = ['var', 'css', 'http', 'https', 'www', 'com', 'url', 'taboola', 'window', 'taboola', 'up', 'down', 'left',
           'right', 'rigth', 'script']
    # print [i for i in wordsNoTags.lower().split() if i not in stop]

    for char in wordsNoTags:
        if (not ((ord(char) >= 97 and ord(char) <= 122) or (ord(char) >= 65 and ord(char) <= 90))):
            wordsNoTags = wordsNoTags.replace(char, " ")

    word_list = {}
    stemmer = SnowballStemmer("english")
    for word in wordsNoTags.split(" "):
        word = word.replace("\n", "")
        word = word.replace("\t", "")
        word = word.replace("\r", "")
        word = word.lower()
        if (word in stop):
            word = word.replace(word, "")

        word = stemmer.stem(word)
        if (len(word) <= 2) or (word in arr):
            word = word.replace(word, "")
        if not word in word_list:
            word_list[word] = 1
        else:
            word_list[word] += 1

    for key in word_list.keys():
        if (word_list[key] == 1):
            del word_list[key]

    word_list = sorted(word_list.items(), key=lambda x: x[1], reverse=True)
    x = ['none']
    y = [0]
    del word_list[0]
    return word_list

def openfile(f):
    x = []
    y = []
    finial = []
    csvfile = open(f,'rb')
    final_csv = open("final.csv","w")
    reader = csv.DictReader(csvfile)
    writer = csv.DictWriter(final_csv, fieldnames=["id","lastVisitTime","title","typedCount","url","visitCount","category"])
    writer.writeheader()
    write_dic = {"id":"","lastVisitTime":"","title":"","typedCount":"","url":"","visitCount":"","category":""}
    for row in reader:
        for s in row.items():
	    write_dic[s[0]] = s[1]
            if s[0] == 'url':
                key_words = main(s[1])
                count = 0
		x = []
		y = []                
		string = ""
                for v, k in key_words:
                    if count < 10:
                        p = str(v)
                        q = int(k)
                        x.append(p)
                        y.append(q)
                        count = count + 1
                del x[0], y[0]
                for a in x:
                    string += a + " "
		print string
                class_is = datum_box.topic_classification(string)
                print class_is
		write_dic['category'] = color_number[class_is]
                print
	writer.writerow(write_dic)

openfile('test.csv')
