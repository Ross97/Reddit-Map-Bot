# Simple Reddit Map bot created by Ross Phelan, 14/10/2019
import praw, re, requests

def osm_result_found(search_term_formatted):
	url = 'https://www.openstreetmap.org/geocoder/search_osm_nominatim?query=' + search_term_formatted
	try:
		response = requests.get(url)
	except ConnectionError:  
   		print('Error requesting', url)
   		return False

	if response.status_code is not 200:
		print('Bad status code from ', url, response.status_code) 
		return False

	if 'No results found' not in response.text:
		return True

	return False


def main():
	BOT_NAME = ''
	SUBREDDIT_TO_SEARCH = '' 

	gmaps_link = 'https://www.google.com/maps/search/'
	osm_link = 'https://www.openstreetmap.org/search?query='
	
	reddit = praw.Reddit(BOT_NAME)
	for comment in reddit.subreddit(SUBREDDIT_TO_SEARCH).stream.comments(skip_existing=True):

		text = comment.body
		if text[:8].lower() == '!mapbot ':
			reply = ''

			search_term = text[8:]
			print('Searching for: ' + search_term)
			search_term_formatted = re.sub("[ ]", "%20", search_term)

			# Check for OSM results
			# Add OSM result if found
			if osm_result_found(search_term_formatted):
				osm_url = osm_link + search_term_formatted
				reply += '[Open Street Maps link](' + osm_url + ') for ' + search_term + '.\n\n'
			else:
				print('Could not find OSM result for ' + search_term)

			# Add GMAPS result
			gmaps_url = gmaps_link + search_term_formatted
			reply += '[Google Maps link](' + gmaps_url + ') for ' + search_term + '.'

			# Reply to the post
			print('Replied to', text, 'with:\n' + reply + '\n')
			comment.reply(reply)

if __name__ == "__main__":
	main()