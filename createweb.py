import argparse
from functools import lru_cache
import twitter2
import folium
from geopy.geocoders import Nominatim, ArcGIS


arcgis = ArcGIS(timeout=10)
nominatim = Nominatim(timeout=10, user_agent="notme")
geocoders = [arcgis, nominatim]

@lru_cache(maxsize=None)
def geocode(address: str):
    """
    Returns a tuple of latitude and longitude of an address
    Args:
        address (str): an address of a location
    Returns:
        tuple: tuple of float numbers
    >>> geocode("New York, USA")
    (40.71455000000003, -74.00713999999994)
    """
    i = 0
    try:
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude
        i += 1
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude
    except AttributeError:
        return None


def creating_map(friends_marks: list):
    """
    Creates a map with markers of friends' accounts
    Args:
        friends_marks (list): a list of tuples: first elem
        - follower's location, second - his name.
    Returns None, creates html file
    """
    map = folium.Map(location=[30, 30], zoom_start=2)
    fg = folium.FeatureGroup(name=f"My friends from Twitter")
    html = """
    Friend's name: {}<br>
    His/her location: {}
    """
    for friend in friends_marks:
        html_format = html.format(friend[1], friend[0])
        iframe = folium.IFrame(html=html_format, width=150, height=150)
        fg.add_child(
            folium.Marker(location=geocode(friend[0]),
                          popup=folium.Popup(iframe),
                          icon=folium.Icon(color='darkpurple')))
    map.add_child(fg)
    map.save('twitter_friends.html')


def get_loc_name(nickname: str):
    """
    Returns a list of friends' locations and names
    Args:
        nickname (str): user's Twitter nickname
    """
    user_info = twitter2.getting_user_info(nickname)
    res = list()
    for item in user_info["users"]:
        res.append((item["location"], item["screen_name"]))
    return list(filter(lambda x: x[0] != "", res))


def main(nickname: str):
    loc_and_name = get_loc_name(nickname)
    creating_map(friends_marks=loc_and_name)

if __name__ == "__main__":
    main("mrkorchsorch")
    # parser = argparse.ArgumentParser() # parsing user's nickname
    # parser.add_argument('nickname', type=str, help='Twiiter name')
    # args = parser.parse_args()
    # nickname = args.nickname
    
