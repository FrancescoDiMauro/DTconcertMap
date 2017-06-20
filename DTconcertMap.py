# Main module: extracts the tweets from the Dream Theater account and displays
# the venues where the concerts have been performed on google maps

import twitter
import re
import concert
import gmplot_modified


# --------- Authentication ---------

token = "3132951441-K77hbdmJ2ejjM3AduQVvUHRpW0J3FTTPUvKLYv2"
token_secret = "7jRXBWnmzbnPu2hugUBnsiEp7kg1m0LOLB1a5QUD4vsSt"
api_key = "2h95SvN2V69XeL1JTxBdNoB6k"
api_secret = "08iF7caP2M7zdptfX6MJpDr0T6PLCuhysySs3TSh0RphT7Vcyo"

auth = twitter.oauth.OAuth(token, token_secret, api_key, api_secret)
twitter_api = twitter.Twitter(auth=auth)


# --------- Tweets extraction ---------

user = "dreamtheaternet"        # name of the account
count = 200                     # number of tweets for each call
include_rts = "False"           # excludes the retweets (they still count in the total, but are not returned)
since_id = 812995769426968576   # start from this tweet (last of 2016)
all_text = []                   # collect the text of the tweets that refer to a concert

# Get the first batch of tweets from the user timeline
tmline = twitter_api.statuses.user_timeline(screen_name=user, count=count, include_rts=include_rts, since_id=since_id)

# store the text of the tweets that refer to a concert
for tweet in tmline:
    if tweet["text"][:5] == "Today":
        all_text.append(tweet["text"])

# get the next batches of tweets according to the last tweet id
while True:
    try:
        # get the next batch
        tmline = twitter_api.statuses.user_timeline(screen_name=user, count=count, include_rts=include_rts, since_id=since_id, max_id=tmline[len(tmline) - 1]["id"] - 1)

        if len(tmline) == 0:
            break

        # store the text of the tweets that refer to a concert
        for tweet in tmline:
            if tweet["text"][:5] == "Today":
                all_text.append(tweet["text"])

    except KeyError:
        break   # break the loop when no more tweets are available


# --------- Collect data on each conctert ---------

# tokenize the text of the tweets and create a list of concerts (one concert for each tweet)
concerts = []
all_text = list(reversed(all_text))     # reverse list of tweets (to have concerts in chronological order)

for tweet in all_text:
    words = re.split('(\W)', tweet)

    # get city name
    i = 4
    city = ""
    while True:
        if words[i] == ',':
            i += 3
            break
        city += words[i]
        i += 1

    # get country name
    country = ""
    while True:
        if words[i] == '-':
            i += 1
            break
        country += words[i]
        i += 1
    country = country.rstrip()

    # get concert date
    date = ""
    while True:
        if words[i] == 'at':
            i += 1
            break
        date += words[i]
        i += 1
    date = date.rstrip()
    date = date.lstrip()

    # get venue
    venue = ""
    while True:
        if len(words[i]) > 0 and (words[i][0] == 'h' or words[i][0] == '\"'):
            i += 3
            break
        venue += words[i]
        i += 1
    venue = venue.rstrip()
    venue = venue.lstrip()

    # create and geolocate the current concert
    concerts.append(concert.Concert(city, country, date, venue))


# geolocate concert venues (find coordinates for each city)
latitudes = []
longitudes = []
tooltips = []
concert.geolocate_concerts(concerts, latitudes, longitudes, tooltips)


# --------- Plot concert locations on google maps ---------

gmap = gmplot_modified.GoogleMapPlotter(47.5, 8.5, 6)                   # initial position (lat, lng, zoom)
gmap.scatter(latitudes, longitudes, tooltips, size=1, edge_width=10)    # plot a pin for each concert according to its location
gmap.draw("TourMap.html")                                               # save map as html file
