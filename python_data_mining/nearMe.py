#!/usr/bin/env python
from selenium import webdriver as web
from selenium.webdriver.common.keys import Keys
import time, re, csv

#these are the column labels
label = ['Restaurants Name', 'price', 'category', 'address', 'website', 'rating', 'total ratings', 'day', '1 AM', '1 AM status', '2 AM', '2 AM status', '3 AM', '3 AM status',
        '4 AM', '4 AM status', '5 AM', '5 AM status', '6 AM', '6 AM status', '7 AM', '7 AM status',
        '8 AM', '8 AM status', '9 AM', '9 AM status', '10 AM', '10 AM status', '11 AM', '11 AM status',
        '12 PM', '12 PM status', '1 PM', '1 PM status', '2 PM', '2 PM status', '3 PM', '3 PM status', '4 PM',
        '4 PM status', '5 PM', '5 PM status', '6 PM', '6 PM status', '7 PM', '7 PM status', '8 PM', '8 PM stauts',
        '9 PM', '9 PM status', '10 PM', '10 PM status', '11 PM', '11 PM status', '12 AM', '12 AM status']

#list of days
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

# this code is not used in any script. Please ignore this function "open_csv"
def open_csv(filename):
    filewriter = []
    with open(filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(label)

#this is creating a list for to write it down on the excel sheet.
def arrange_time_and_value(list_label, dataList):
    finalized = []
    for label in list_label:
        finalized.append('N/A')
    if not dataList:
        return finalized

    for data in dataList:
        pos = list_label.index(data[0])
        finalized[pos] = data[2]
        finalized[pos+1] = data[1]

    return finalized

#this is writing the value into the excel sheet.
def write_value(filename, restaurants):
    with open(filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        #first write the label on the top in csv
        filewriter.writerow(label)
        for restaurant in restaurants:
            for day in days:
                list_l = []
                list_l.append(restaurant['restaurant name'])
                list_l.append(restaurant['price'])
                list_l.append(restaurant['category'])
                list_l.append(restaurant['address'])
                list_l.append(restaurant['website'])
                list_l.append(restaurant['rating'])
                list_l.append(restaurant['total ratings'])
                list_l.append(day)

                #checking the key in manually
                #here, restaurant[day] contains the data information in dictionary for times
                if day in restaurant:
                    finalized  = arrange_time_and_value(label[8:], restaurant[day])
                    list_l = list_l + finalized
                else:
                    for item in label[8:]:
                        list_l.append('N/A')

                filewriter.writerow(list_l)

def filter_heightVal(value):
    result = re.findall(r'[0-9]+', value)
    if result:
        return result[0]
    else:
        return None

def filter_status(status):
    regex = "(.*:)([ A-z]*)"
    if status:
        return re.findall(regex, status)
    return None

def three_tuple_generator(status, value):
    if not status:
        return None

    time = status[0][0]
    text = status[0][1]

    time = time[:len(time)-1]
    text = text[1:]

    return (time, text, value)

def filter_total_ratings(rating_text):
    list_s = rating_text.split()
    return list_s[0]

#this is the main mining process
def startMining(url, text):
    #initialize variable
    gl = []

    browser = web.Chrome()
    browser.get(url)
    search = browser.find_element_by_name('q')
    search.send_keys(text)
    search.send_keys(Keys.RETURN)


    more_places = browser.find_element_by_xpath('//span[text()="More places"]')
    more_places.click()

    #dbg0pd (restaurants name)
    list_of_restaurants = browser.find_elements_by_class_name('dbg0pd')
    if len(list_of_restaurants) == 0:
        print("There is no list of restaurants")
        browser.close()
        return None

    #BTtC6e (reviews)
    reviews_for_each_restaurants = browser.find_elements_by_class_name('BTtC6e')

    #run for every restaurants. It will click first and then collect the times
    for item in list_of_restaurants:

        dictionary = {}

        #restaurant name
        temp = item.text.replace("\n", " ")
        dictionary['restaurant name'] = temp

        index = list_of_restaurants.index(item)
        #get restaurant rating
        dictionary['rating'] = reviews_for_each_restaurants[index].text

        #click on the restaurant name and extract height data
        #the class name: iExHeOgPhxz4 but ends with
        item.click()
        time.sleep(3)

        #get restaurant address (LrzXr)
        dictionary['address'] = browser.find_element_by_class_name('LrzXr').text

        #get the website link
        link = browser.find_elements_by_xpath('//a[contains(@class, "CL9Uqc")]')
        if not link:
            dictionary['website'] = "N/A"
        else:
            dictionary['website'] = link[0].get_attribute('href')

        #get the total ratings
        total_ratings = browser.find_elements_by_xpath('//span[contains(text(), "Google reviews")]')
        if not total_ratings:
            dictionary['total ratings'] = "N/A"
        else:
            dictionary['total ratings'] = filter_total_ratings(total_ratings[0].text)

        #get the category of the restaurants
        #YhemCb
        restaurants_category = browser.find_elements_by_xpath('//span[contains(@class, "YhemCb")]')
        if not restaurants_category:
            dictionary['category'] = "N/A"
        else:
            if len(restaurants_category) > 1:
                dictionary['price'] = restaurants_category[0].text
                dictionary['category'] = restaurants_category[1].text
            else:
                dictionary['price'] = "N/A"
                dictionary['category'] = restaurants_category[0].text

        graphs = browser.find_elements_by_xpath('//div[contains(@class, "yPHXsc")]')
        counter = 0
        for date in graphs:
            data = date.find_elements_by_xpath('.//div')
            l = []
            #print('########')
            #(time, status, value)
            for item in data:
                status = item.get_attribute('aria-label')
                value = item.get_attribute('style')

                final = three_tuple_generator(
                    filter_status(status), filter_heightVal(value))

                if final:
                    l.append(final)
                #print(value, filter_heightVal(value))
            #print('########')
            dictionary[days[counter]] = l
            counter += 1
        gl.append(dictionary)
        #break
    #print(gl[0])
    browser.close()
    return gl

def main_start(url="https://www.google.com", search="restaurants near me"):
    restaurants = startMining(url, search)
    #for restaurant in restaurants:
    #    print(restaurant)
    if restaurants:
        write_value("temp.csv", restaurants)
