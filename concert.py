# This module contains the Concert class and a function to extract the geographical location of each concert

# city, country     location of the concert
# date              date of the concert (month, day)
# venue             name of the venue where the concert is performed


class Concert:

    def __init__(self, city, country, date, venue):
        self.city = city
        self.country = country
        self.date = date
        self.venue = venue


# find the coordinates for the concerts in the input list
def geolocate_concerts(concerts, latitudes, longitudes, tooltips):

    import googlemaps
    gmaps = googlemaps.Client(key="AIzaSyCO93ffDf0xBgyb8elvUsPJv9ZYQiGeRJo")

    for concert in concerts:
        geocode_result = gmaps.geocode(concert.venue + " " + concert.city + " " + concert.country)
        if len(geocode_result) > 0:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
        else:
            geocode_result = gmaps.geocode(concert.city + " " + concert.country)
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']

        # check if the band already played in the current venue
        try:
            tooltips[latitudes.index(lat)] += "\\n" + concert.date + " (" + concert.venue + ")"
        except ValueError:
            latitudes.append(lat)
            longitudes.append(lng)
            tooltips.append(concert.date + " (" + concert.venue + ")")
