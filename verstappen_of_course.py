#!/usr/bin/env python3 

'''

To-Do's

+ calculate number of "of courses" per sentence

'''

import requests
from bs4 import BeautifulSoup
import mout
import json
import matplotlib.pyplot as plt

rescrape = False

big_total = 0

if rescrape:

	races = [	
				"bahrain",
				"saudi-arabian",
				"australian",
				"emilia-romagna",
				"miami",
				"spanish",
				"monaco",
				"azerbaijan",
				"canadian",
				# "italian",
			]

	urls = []

	for race in races:

		# https://www.fia.com/news/f1-2022-emilia-romagna-grand-prix-post-race-press-conference-transcript

		urls.append(f"https://www.fia.com/news/f1-2022-{race}-grand-prix-friday-press-conference-transcript")
		if race not in ["miami","saudi-arabian","emilia-romagna"]:
			urls.append(f"https://www.fia.com/news/f1-2022-{race}-grand-prix-saturday-press-conference-transcript")
		if race not in ["italian","emilia-romagna"]:
			urls.append(f"https://www.fia.com/news/f1-2022-{race}-grand-prix-post-qualifying-press-conference-transcript")
		if race == "italian":
			urls.append(f"https://www.fia.com/news/f1-2022-emilia-romagna-grand-prix-post-race-press-conference-transcript")
		else:
			urls.append(f"https://www.fia.com/news/f1-2022-{race}-grand-prix-post-race-press-conference-transcript")

	data = []

	for url in urls:

		# if "post-race" in url:
		# 	interview_type="post-race"
		
		html_text = requests.get(url).text
		soup = BeautifulSoup(html_text, 'html.parser')

		title = soup.title.string
		
		try:
			body = soup.find("div", {"class": "content-body"})
			text = body.get_text()
		except:
			text = soup.get_text()

		# print(url)
		# print(title)

		try:
			key = title.split(" - ")[1].strip()
		except:
			mout.headerOut(title)
		# print(title.split(" - "))

		try:
			interview_type = title.split(" - ")[2].strip().split(" ")[0].strip()
		except:
			title.split(" - ")[1].split("press conference")

			interview_type = "Friday"

		mout.headerOut(key)
		mout.out(interview_type)

		date = soup.find("span",{"class":"date-display-single"}).get_text()

		paragraphs = body.find_all("p")

		if not "MV:" in body.get_text():
			continue

		n_oc = 0
		n_words = 0
		n_sentences = len(paragraphs)
		for p in paragraphs:
			t = p.get_text()
			if t.startswith("MV:") or t.startswith("Max"):
				# print(t)
				n_oc += t.count("of course")
				n_oc += t.count("Of course")
				n_sentences += t.count(". ")
				n_sentences += t.count("! ")
				n_sentences += t.count("? ")
				n_words += len(t.split(" "))
				big_total += t.count("of course")
				big_total += t.count("Of course")

		n_paragraphs = len(paragraphs)

		mout.varOut("date",date)
		mout.varOut("url",url)
		# mout.varOut("#of courses",n_oc)
		# mout.varOut("#of courses%",100*n_oc/(n_words/2))
		# mout.varOut("#of courses/sentences",n_oc/n_sentences)
		# mout.varOut("#of courses/paragraph",n_oc/n_paragraphs)

		data.append(dict(key=key,date=date,type=interview_type,n_oc=n_oc,n_words=n_words,n_sentences=n_sentences,n_paragraphs=n_paragraphs))

	json.dump(data,open("of_course.data",'w'))

else:

	data = json.load(open("of_course.data",'r'))

print(big_total)

fig,ax = plt.subplots()

# data = sorted(data, key=lambda b: b['date']) 

ydata = [d['n_oc'] for d in data]
ddata = [d['date'] for d in data]
xdata = [i for i in range(len(ydata))]
kdata = [d['key'] for d in data]

plt.xticks(rotation = 90)

ax.set_title("How often does Verstappen say 'of course' in interviews?")
ax.set_xlabel("Date")
ax.set_ylabel("# 'of course'")

plt.subplots_adjust(bottom=0.2)

plt.bar(xdata,ydata,tick_label=ddata,color='r')

plt.show()

