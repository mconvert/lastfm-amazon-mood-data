from amazonproduct import API
import amazonproduct.errors as ape
import csv 
import keys

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


config = {
	'access_key': keys.access_key(),
	'secret_key': keys.secret_key(),
	'associate_tag': 'maxime-22',
	'locale': 'jp'
}



api = API(cfg=config)


with open('../csv/tracks_mood.csv', 'rb') as infile, open('../csv/tracks_mood_amazon.csv', 'wb') as outfile:
# with open('tracks_mood.csv', 'rb') as infile:
	datareader = csv.reader(infile, delimiter=',')
	datawriter = csv.writer(outfile)

	datawriter.writerow("tid,title,artist,g1,g2,g5,g6,g7,g8,g9,g11,g12,g14,g15,g16,g17,g25,g28,g29,g31,g32,on_amazon_jp".split(","))
	next(datareader, None)


	for row in datareader:
		
		kwds = str(row[1]) + ' ' + str(row[2])
		title = str(row[1])


		song_is_on_amazon = False
		check = True

		while (check):
			try:
				items = api.item_search('MP3Downloads', Keywords=kwds, Title=title)
				if len(items)>=1:
					song_is_on_amazon = True
					break
			except ape.NoExactMatchesFound, e:
				check = False # 
			except ape.TooManyRequests, e:
				pass

		print(str(song_is_on_amazon) + ' | ' + row[1] + ' | ' + row[2])
		row.append(song_is_on_amazon)

		datawriter.writerow(row)

