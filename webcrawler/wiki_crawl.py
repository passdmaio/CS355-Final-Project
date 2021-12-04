import requests
from bs4 import BeautifulSoup
import pandas

# def scrape_popular_items(url):


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


results = food_soup.find(id="page_container")
restaurant_elements = results.findAll('div', class_="restaurants--restaurant_listings_row row")
for element in restaurant_elements:
    # -- snip --
    links = element.find_all("a")
    for link in links:
        link_url = link["href"]
        #print(f"{link_url}")
        get_restaurant_data(link_url)
        try:
            get_popular_menu(link_url)
            restaurantSites.append(link_url)
        except AttributeError:
            break

data = list(zip(restaurantSites, restaurantNames, menuItems))

d = pandas.DataFrame(data, columns=["Restaurant Site", "Restaurant Name & Location", "Popular Menu Items & Cost"])

# Writing the data frame to a new Excel File
try:
    d.to_excel("output.xlsx")
except:
    print("\nSomething went wrong ! Please check code / Internet Connection")
else:
    print("\nRestaurant data successfully written to Excel.")
finally:
    print("\nQuitting the program. Bye !")
