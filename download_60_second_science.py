#! python3
# download 60_second_science mp3 and transcript.

import argparse
import requests
import os
from bs4 import BeautifulSoup

# commandline args
parser = argparse.ArgumentParser(description="download mp3 and transcript of 60 second science")

parser.add_argument('output', help="saving folder")
parser.add_argument('-s', '--start', type=int, default=1, help="startPage, default is 1")
parser.add_argument('-e', '--end', type=int, default=139, help="endPage, default is 139")

# get args
args = parser.parse_args()

startPage = args.startPage
endPage = args.endPage
OUTPUT = args.output


url = 'https://www.scientificamerican.com/podcast/60-second-science/'
os.makedirs(OUTPUT, exist_ok=True)   # store mp3 and transcript in ./60_second_science
os.chdir(OUTPUT)
os.makedirs('mp3', exist_ok=True) # subfolder to store mp3
os.makedirs('Transcript', exist_ok=True) # subfolder to store transcript


def get_html(url):
	html = requests.get(url)
	try:
		html.raise_for_status()
	except Exception as e:
		print('There was a problem: %s' % e)
	return html


def download_science(startPage, endPage):
	for urlNumber in range(startPage, endPage + 1):
		# Download the page.
		print('Downloading page https://www.scientificamerican.com/podcast/60-second-science/?page=%s...' % urlNumber)
		html = get_html('https://www.scientificamerican.com/podcast/60-second-science/?page=' + str(urlNumber))

		soup = BeautifulSoup(html.text, 'html.parser')

		# Find the URL of the mp3 and transcript.
		content_urls = soup.select('h3 a')
		if content_urls == []:
			print('Could not find resource.')
		else:
			# There are 17 radios per page
			for i in range(17):
				content_url = content_urls[i].get('href')
				title = content_urls[i].getText()
				# clean title to use as legal filename
				title = title.replace(': ', '-').replace(' ', '_').replace('\"', '\'').replace('?', '')
				html = get_html(content_url)
				soup = BeautifulSoup(html.text, 'html.parser')

				# Download the mp3 and save to ./60_second_science/mp3
				mp3_url = 'https://www.scientificamerican.com' \
						+ soup.select('div[class=tooltip-outer] a')[0].get('href')
				print('Downloading mp3 of %s...' % title)
				mp3 = get_html(mp3_url)
				with open(os.path.join('mp3', title + '.mp3'), 'wb') as mp3_file:
					for chunk in mp3.iter_content(100000):
						mp3_file.write(chunk)

				# Download the Transcript and save to ./60_second_science/Transcript
				print('Downloading transcript of %s...' % title)
				with open(os.path.join('Transcript', title + '.txt'), 'wb') as transcript_file:
					transcript = soup.select('div[class=transcript__inner] p')[:-2]
					for paragraph in transcript:
						transcript_file.write((paragraph.getText() + '\n').encode('utf-8'))
		time.sleep(2)
	print('Done.')

if __name__ == '__main__':
	# there are 139 pages on 2016.11.3
	download_science(startPage, endPage)





