"""
Given a tag to search through the command line, this program will download
every file under that tag on imgur that is in the first
load.

I could probably use selenium later 
using Keys.END to scroll all the way 
down wait some time for new images to load 
and then continue downloading. Since rn it just
stops at the loading gif.
"""
import os, bs4, requests, sys

def downloadImg():
	category = ' '.join(sys.argv[1:])
	os.makedirs(category, exist_ok=True)
	res = requests.get(f"https://imgur.com/search?q={category}") # go the the search results
	res.raise_for_status() # make sure exists

	soup = bs4.BeautifulSoup(res.text, "lxml") # make an html parser 
	imageElements = soup.select('img') # get a list of all the images

	if imageElements == []:
		print('Could Not Find Any Images.')

	for image in imageElements:
		if str(image) == '<img src="//s.imgur.com/images/loaders/ddddd1_181817/48.gif"/>':
			continue # i dont want to download the loading gif

		res = requests.get(f"http:{image.get('src')}") # go to the image link (always add http: before a src to actually go to it)
		res.raise_for_status()

		# name the file whatever the basename of the src is 
		imageFileName = os.path.basename(image.get('src'))
		print(f"Downloading {image.get('src')}")

		# create file (remember need wb to create binary files)
		imageFile = open(os.path.join(category, imageFileName), 'wb')

		# donwload the image in chunks 
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close() # close this and move on to the next image

	print('Finished.')

def main():
	downloadImg()

if __name__ == '__main__':
	main()