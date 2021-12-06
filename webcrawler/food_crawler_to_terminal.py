import requests
from bs4 import BeautifulSoup

# current bugs: popular food items all fitting into 1 element, long time to scrape?

# url declarations
root_url = 'https://www.dineinct.com'
robot_url = root_url + '/robots.txt'
target_url = root_url + '/restaurants/Restaurant%20Menus?area=06050_474'

# gets info for soup
robot_page = requests.get(robot_url)
target_page = requests.get(target_url)

# Beautifulsoup obj declarations
robot_soup = BeautifulSoup(robot_page.content, 'html.parser')
food_soup = BeautifulSoup(target_page.content, 'html.parser')

deadLinks = ['https://www.dineinct.com/order/restaurant/boston-market-menu/1041/06050', 'https://www.dineinct.com/order/restaurant/boston-market-menu/1054/06050', 'https://www.dineinct.com/order/restaurant/boston-market-menu/1061/06050', 'https://www.dineinct.com/order/restaurant/boston-market-menu/1066/06050', "https://www.dineinct.com/order/restaurant/boston-market-menu/1047/06050", 'https://www.dineinct.com/order/restaurant/jefferson-fry-company---cromwell-menu/1071/06050', 'https://www.dineinct.com/order/restaurant/jefferson-fry-company---canton-menu/986/06050']
restaurantNames = []
menuItems = []
restaurantSites = []


def get_restaurant_data(url):
    url_page = requests.get(url)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    restaurant_data_group = soup.find(id="restaurant_menu_head")
    restaurant_name = restaurant_data_group.find("h3", class_='media-heading')
    restaurant_name.find("a").decompose()
    restaurantNames.append(restaurant_name.text.strip())


def get_popular_menu(url):
    url_page = requests.get(url)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    popular_food_find = soup.find(id='heading-POPULAR')
    popular_food = popular_food_find.findAll("div", class_="row hover")
    for popular_data in popular_food:
        food_text = popular_data.find_all("b")
        for entry in food_text:
            entry_list = entry.text
            menuItems.append(entry_list)


# this block will find and collect the list of links to popular restaurant sites in ct
results = food_soup.find(id="page_container")
restaurant_elements = results.findAll('div', class_="restaurants--restaurant_listings_row row")
for element in restaurant_elements:
    # collects all the links in the a tag
    links = element.find_all("a")
    for link in links:
        # sets blacklist link state to 0 at beginning of loop
        cleanLink = True
        link_url = link["href"]

        # traverses link blacklist, if one is found, gets skipped.
        for currentDeadLink in deadLinks:
            if link_url == currentDeadLink:
                cleanLink = False
        if not cleanLink:
            continue
        # if the link_url is not found, data is scraped
        get_restaurant_data(link_url)
        try:
            deadLinks.append(link_url)
            #get_popular_menu(link_url)
            restaurantSites.append(link_url)
        except AttributeError:
            break

print(restaurantNames)
