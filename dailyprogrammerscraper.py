#!/usr/bin/python
import os
import sys
import praw
import urllib2
import re
import HTMLParser

def render_post_html(post, target_dir):
	if not post.selftext_html: return

	#setup
	html_parser = HTMLParser.HTMLParser()

	htmlbegin = """<html>
	<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	</head>
	<body>
	<div class="container">
	<h1>"""

	htmlend = """</div>
	</body>
	</html>"""

	#Add an entry to the master list for the challenge
	masterlist = open(os.path.join(target_dir, "dps.html"), 'a')
	masterlist.write('<li><a href="%s.html">%s</a></li>\n' % (post.id, post.title.encode('ascii', 'ignore')))
	masterlist.close()

	#Create and save the challenge page
	file = open(os.path.join(target_dir, post.id + ".html"), 'w+')	
	file.write(htmlbegin + post.title.encode('ascii', 'ignore') + "</h1>" + html_parser.unescape(post.selftext_html).encode('ascii', 'ignore') + htmlend)
	file.close()

def get_challenges():
	#Create a directory to save the output files in
	target_dir = 'dps'
	if not (os.path.exists(target_dir)):
	  os.mkdir(target_dir)

	#HTML setup for masterlist
	ml_html_head="""<html>
	<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	</head>
	<body>
	<div class="container">
	<h1>/r/dailyprogrammer challenge directory</h1>
	<ul>
	"""

	#Prepare the masterlist file
	masterlist = open(os.path.join(target_dir, "dps.html"), 'w+')
	masterlist.write(ml_html_head)
	masterlist.close()

	challenges = []

	#Download the /r/dailyprogrammer feed
	print "Getting posts from reddit..."
	r = praw.Reddit(user_agent='User-Agent: dailyprogrammerscraper v.1 by /u/bjshively')
	posts = r.get_subreddit('dailyprogrammer').search('challenge', limit=None)

	print "Making list of challenges..."
	for post in posts:
		if(re.search("\d+/\d+/\d+", post.title)):
			challenges.append(post)

	#Sort by creation date
	print "Sorting challenges..."
	challenges.sort(key=lambda x: x.created_utc)

	for challenge in challenges:
		print "Rendering " + challenge.id
		render_post_html(challenge, target_dir)

	#Wrapup the master index, dps.html
	masterlist = open(os.path.join(target_dir, "dps.html"), 'a')
	masterlist.write('</ul>\n</div></body>\n</html>')
	masterlist.close()

def main():
	print "#" * 40
	print "/r/dailyprogrammer challenge scraper"
	print "#" * 40
	get_challenges()

if __name__ == '__main__':
  main()