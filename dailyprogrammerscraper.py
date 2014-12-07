#!/usr/bin/python
import os
import sys
import praw
import urllib2
import re
import HTMLParser

#Create a directory to save the output files in
target_dir = 'dps'
if not (os.path.exists(target_dir)):
  os.mkdir(target_dir)

#Prepare the masterlist file
masterlist = open(os.path.join(target_dir, "dps.html"), 'w+')
masterlist.write('<html>\n<body>\n<ul>')
masterlist.close()

challenges = []

def render_post_html(post):
	if not post.selftext_html: return

	#setup
	html_parser = HTMLParser.HTMLParser()
	htmlbegin = "<html>\n<body>\n<h1>"
	htmlend = "</body>\n</html>"

	#Add an entry to the master list for the challenge
	masterlist = open(os.path.join(target_dir, "dps.html"), 'a')
	masterlist.write('<li><a href="' + post.id + '.html">'+ post.title.encode('ascii', 'ignore') + '</a></li>\n')
	masterlist.close()

	#Create and save the challenge page
	file = open(os.path.join(target_dir, post.id + ".html"), 'w+')	
	file.write(htmlbegin + post.title.encode('ascii', 'ignore') + "</h1>" + html_parser.unescape(post.selftext_html).encode('ascii', 'ignore') + htmlend)
	file.close()

#Download the /r/dailyprogrammer feed
print "Getting posts from reddit..."
r = praw.Reddit(user_agent='User-Agent: dailyprogrammerscraper v.1 by /u/bjshively')
posts = r.get_subreddit('dailyprogrammer').search('challenge', limit=None)

print "Making list of challenges..."
for post in posts:
	challenges.append(post)

#Sort by creation date
print "Sorting challenges..."
challenges.sort(key=lambda x: x.created_utc)

for challenge in challenges:
	print "Rendering " + challenge.id
	render_post_html(challenge)

masterlist = open(os.path.join(target_dir, "dps.html"), 'a')
masterlist.write('</ul>\n</body>\n</html>')
masterlist.close()

#Outputs a single challenge in decoded HTML
#print render_post_html(samplepost)

#for post in submissions:
#	challenge_title_dict[post.created_utc] = str(post)
#	challenge_url_dict[post.created_utc] = post.url
	#TODO - sort challenges by challenge # or date

	#ordered_challenges.append(str(post), key=post.created_utc)

#ordered_challenges = sorted(ordered_challenges, key=created_utc)

#post_dates = challenge_title_dict.keys()
#post_dates = sorted(post_dates)

#for e in post_dates:
#	print challenge_title_dict[e]
#	print challenge_url_dict[e]

#Identify which posts are challenges

#Download each of the challenges

#Save the challenge to a separate HTML document

#Build an index of the downloaded challenges