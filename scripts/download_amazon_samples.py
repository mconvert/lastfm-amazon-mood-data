import urllib.request
import re
import os
import requests

import time


def get_html_code(url, conn):

	while (1):
		r = conn.get(url)
		if r.status_code == 503:
			# print("Connection could not be established!")
			continue
		else:
			html = r.text
			break

	return html



def fetch_title_artist(songhtml):

	title_pattern = '<h1 class="a-size-large a-spacing-micro">(.*?)</h1>'
	artist_pattern = '<a id="ProductInfoArtistLink".*?>(.*?)</a>'

	title_regex = re.compile(title_pattern)
	artist_regex = re.compile(artist_pattern)

	title = title_regex.findall(songhtml)[0]
	artist = artist_regex.findall(songhtml)[0]

	return title, artist




def fetch_sample_link(songhtml):

	domain = 'https://www.amazon.co.jp'

	pattern = '<div class="sample-button disabled">\n.*?<a class="a-link-normal" href="(.*?)"></a>\n.*?</div>'
	regex = re.compile(pattern)
	result = regex.findall(songhtml)[0]

	link = domain + result

	return link


def fetch_songs_links(pagehtml):
	""" Takes the html string of one wishlist page.
		Returns a list of urls of the song samples.
	"""
	domain = 'https://www.amazon.co.jp'

	pattern = '<a id="itemName.*?href="(.*?)">'
	regex = re.compile(pattern)
	result = regex.findall(pagehtml)

	songs = [domain + x for x in result]

	return songs


def fetch_wishlist_page_links(listhtml, url):
	""" Takes the html string of the first page of a wishlist.
		Returns a list of urls of the different pages that make the wishlist.
	"""

	domain = 'https://www.amazon.co.jp'

	pattern = '<li data-action="pag-trigger".*?<a href="(.*?)">.*?</a></li>'
	regex = re.compile(pattern)
	result = regex.findall(listhtml)

	pages = [domain + x for x in result]

	if len(pages) == 0:
		pages.append(url)

	return pages





if __name__ == "__main__":
	
	# (manually) SPECIFY THE WISHLIST LINK AND THE MOOD GROUP
	url = "http://amzn.asia/fDKjp46"
	groupdir = "g6"
	mooddir = "mood_data/"
	path = mooddir+groupdir

	s = requests.Session()


	# OPEN AND RETRIEVE WISHLIST TOP PAGE HTML CODE
	roothtml = get_html_code(url, s)

	# CREATE LIST OF PAGE URLs
	pages = fetch_wishlist_page_links(roothtml, url)

	# CREATE DIRECTORY IF DOES NOT EXIST
	if not os.path.exists(path):
		os.makedirs(path)	

	for pageurl in pages:

		# OPEN AND RETRIEVE WISHLIST PAGE HTML CODE
		pagehtml = get_html_code(pageurl, s)

		# CREATE LIST OF SONGS URLs
		songs = fetch_songs_links(pagehtml)


		for songurl in songs:

			# OPEN AND RETRIEVE SONG PAGE HTML CODE
			songhtml = get_html_code(songurl, s)

			# RETRIEVE SAMPLE URL
			sampleurl = fetch_sample_link(songhtml)

			# RETRIEVE SAMPLE TITLE & ARTIST
			title, artist = fetch_title_artist(songhtml)


			# OPEN AND RETRIEVE SAMPLE PAGE HTML CODE (i.e. THE DIRECT LINK TO THE MP3 FILE)
			samplehtml = get_html_code(sampleurl, s)

			# DOWNLOAD SONG
			title = re.sub('[/;|]+', ' ', title)
			artist = re.sub('[/;|]+', ' ', artist)
			filename = path + '/' + title + ' - ' + artist + '.mp3'
			
			while (1):
				try:
					urllib.request.urlretrieve(samplehtml, filename)
					print("SUCCESS: " + filename)
					break
				except Exception as e:
					print("FAILURE: " + filename)
					continue





