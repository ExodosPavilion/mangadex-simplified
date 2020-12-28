import requests, bs4, json

site = 'https://mangadex.org/'
apiStartPoint = 'https://mangadex.org/api/v2/'

def getFrontPage():
	res = requests.get(site)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, features='lxml')
	#print(soup.prettify())

	#looking for a div that has "col-md-6 border-bottom p-2"
	titles = soup.select('.col-md-6.border-bottom.p-2 .manga_title.text-truncate')

	titleDetails = []
	'''
		{
			title: some title
			mangadex-id: 123
			link: site + href
		}
	'''

	for titleData in titles:
		title = titleData.text

		mangadexID = (titleData['href'].split('/'))[2]
		apiJson = getTitleApiData(mangadexID)

		link = site + titleData['href'][1:]
		
		titleDetails.append({
				'title':title, 
				'mangadexID':mangadexID, 
				'bayesianRating':apiJson['data']['rating']['bayesian'], 
				'meanRating':apiJson['data']['rating']['mean'], 
				'numOfUsers':apiJson['data']['rating']['users'], 
				'link':link
			})

	return titleDetails


def printFrontPage(titleDetails):
	for item in titleDetails:
		print('(' + item['mangadexID'] + ') ' + item['title'])
		print( 'Bayesian Rating: ' + str(item['bayesianRating']) )
		print( 'Mean user rating: ' + str(item['meanRating']) + 'by ' + str(item['numOfUsers']) )
		print(item['link'])
		print()


def getTitleApiData(mangaID):
	apiSite = 'https://mangadex.org/api/v2/manga/' + mangaID

	res = requests.get(apiSite)
	res.raise_for_status()

	return json.loads( res.text )


dets = getFrontPage()
printFrontPage(dets)
