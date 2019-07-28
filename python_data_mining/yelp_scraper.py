from selenium import webdriver as web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, re, csv, datetime, json, datetime

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist


def startYelp(link, restaurant_name, location):

    def concat_for_pages(pages):
        list_result = [int(s) for s in pages.split() if s.isdigit()]
        if list_result[0] == list_result[1]:
            return True
        return False

    def filter_rating_title(rating):
        list_result = rating.split()
        return list_result[0]

    def get_year_month(date):
        split_by_space = date.split(" ")
        captured = split_by_space[0].split('/')

        #I am just returning year..
        year = captured[2]

        return year


    #go to the yelp link
    yelp = web.Chrome()
    yelp.get(link)

    #search the restaurant_name
    search = yelp.find_elements_by_xpath('.//input[starts-with(@class, "pseudo")]')
    search[0].send_keys(restaurant_name)

    #this will clear the previous location text before
    search[1].clear()
    search[1].send_keys(location)

    button = yelp.find_element_by_xpath('.//button[starts-with(@class, "ybtn")]')
    button.click()

    time.sleep(3)

    #find for the restaurant name that is acquired from parameter and click that restaurant name in website.
    list_of_restaurants_names = yelp.find_elements_by_xpath('.//a[starts-with(@class, "lemon--a")]')
    for item in list_of_restaurants_names:
        if item.text == restaurant_name:
            #print(item.text)
            item.click()
            break

    #look for the total pages because I am going to star tthe loop in order to scrape the data.
    total_pages = yelp.find_element_by_xpath('.//div[starts-with(@class, "page-of-pages")]').text
    next_page_btn = yelp.find_element_by_xpath('.//span[starts-with(@class, "pagination-label")]')

    """
    star_ratings = []
    reviews_in_text = []
    all_dates = []
    """

    result = []
    no_more = False

    while True:
        print(total_pages)
        review_contents = yelp.find_elements_by_xpath('.//div[starts-with(@class, "review-content")]')
        for item in review_contents:
            temp_dict = {}

            #grab the date value
            item.find_element_by_xpath('.//span[starts-with(@class, "rating-qualifier")]')
            date = item.text.split('\n')
            #print(date[0])

            #grab the text
            text = item.find_element_by_xpath('./p[starts-with(@lang, "en")]').text

            #grab the rating
            rating = item.find_element_by_xpath('.//div[starts-with(@class, "i-stars")]')
            rating = filter_rating_title(rating.get_attribute("title"))

            #print(rating)
            #print(text)

            temp_dict['date'] = get_year_month(date[0])
            #print(temp_dict['date'])
            temp_dict['text'] = text
            temp_dict['rating'] = rating

            result.append(temp_dict)

        if no_more:
            break

        next_page_btn = yelp.find_elements_by_xpath('.//span[starts-with(@class, "pagination-label")]')

        if len(next_page_btn) > 1:
            next_page_btn = next_page_btn[1]
        else:
            next_page_btn = next_page_btn[0]

        total_pages = yelp.find_element_by_xpath('.//div[starts-with(@class, "page-of-pages")]').text

        #clicks the next page button and wait for 3 seconds to load..
        next_page_btn.click()

        if concat_for_pages(total_pages):
            no_more = True

        time.sleep(5)
    return result

def count_total_pos_neg(result):
    #get current year
    current_year = datetime.datetime.now().year
    dict_overall = {}
    dict_overall['positive'] = {}
    dict_overall['negative'] = {}

    for dict_item in result:
        subtracted_year = current_year - int(dict_item['date'])
        if float(dict_item['rating']) > 3.0:

            #check if key exist
            key = str(subtracted_year) + " years ago"
            if key in dict_overall['positive'].keys():
                dict_overall['positive'][key] += 1
            else:
                dict_overall['positive'][key] = 1
        else:

            #check if key exist
            key = str(subtracted_year) + " years ago"
            if key in dict_overall['negative'].keys():
                dict_overall['negative'][key] += 1
            else:
                dict_overall['negative'][key] = 1

    return dict_overall

def open_csv(fname):
    result = []
    current_year = datetime.datetime.now().year
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        first_time = True
        for row in csv_reader:
            if first_time:
                first_time = False
            else:
                result.append((row[0], row[1], row[2]))
    return result

def write_to_csv(result, fname):
    with open(fname, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['date', 'text', 'rating'])
        for item in result:
            filewriter.writerow([item['date'], item['text'], item['rating']])

def write_to_json(result, fname):
    with open(fname, 'w') as f:
        json.dump(result, f)

def frequency_on_csvfile(result):
    neg_text = []
    pos_text = []

    tokenizer = RegexpTokenizer(r'\w+')

    for rev in result:
        tokens = tokenizer.tokenize(rev[1])
        tokens = [w.lower() for w in tokens]
        filtered = [w for w in tokens if w not in stopwords.words('english')]

        if float(rev[2]) > 3:
            pos_text += filtered
        else:
            neg_text += filtered

    fdist = FreqDist(pos_text)
    pos_fd_final = fdist.most_common(10)
    pos_result = []
    for item in pos_fd_final:
        temp_dict = {}
        temp_dict['word'] = item[0]
        temp_dict['count'] = item[1]
        pos_result.append(temp_dict)

    fdist = FreqDist(neg_text)
    neg_fd_final = fdist.most_common(10)
    neg_result = []

    for item in neg_fd_final:
        temp_dict = {}
        temp_dict['word'] = item[0]
        temp_dict['count'] = item[1]
        neg_result.append(temp_dict)

    return pos_result, neg_result

def get_trend_on_freq(pos_result, neg_result, result):
    pos_dict = {}
    neg_dict = {}

    #turn them into list
    pos_words = [w['word'] for w in pos_result]
    neg_words = [w['word'] for w in neg_result]
    current_year = int(datetime.datetime.now().year)

    tokenizer = RegexpTokenizer(r'\w+')

    for rev in result:
        tokens = tokenizer.tokenize(rev[1])
        tokens = [w.lower() for w in tokens]
        filtered = [w for w in tokens if w not in stopwords.words('english')]
        subtracted_year = current_year - int(rev[0])
        subtracted_year = str(subtracted_year) + " years ago"

        if float(rev[2]) > 3:
            if not subtracted_year in pos_dict.keys():
                pos_dict[subtracted_year] = {}

            #if the keyword we are looking for is in filtered words
            for word in filtered:
                if word in pos_words:
                    #check if key exists
                    if word in pos_dict[subtracted_year].keys():
                        pos_dict[subtracted_year][word] += 1
                    else:
                        pos_dict[subtracted_year][word] = 1

        else:
            if not subtracted_year in neg_dict.keys():
                neg_dict[subtracted_year] = {}

            for word in filtered:
                if word in neg_words:
                    if word in neg_dict[subtracted_year].keys():
                        neg_dict[subtracted_year][word] += 1
                    else:
                        neg_dict[subtracted_year][word] = 1

    return pos_dict, neg_dict

if __name__ == "__main__":
    #result = startYelp("https://www.yelp.com", "Kiraku", "Berkeley Downtown, CA")
    #write_to_csv(result, "yelp_collection.csv")
    #result = count_total_pos_neg(result)
    #write_to_json(result, "yelp_reviews_freq.json")
    result = open_csv("yelp_collection.csv")
    pos_result, neg_result = frequency_on_csvfile(result)
    pos_dict, neg_dict = get_trend_on_freq(pos_result, neg_result, result)
    #write_to_json(pos_result, "yelp_pos_fq.json")
    #write_to_json(neg_result, "yelp_neg_fq.json")
    write_to_json(pos_dict, "yelp_pos_fq_trend.json")
    write_to_json(neg_dict, "yelp_neg_fq_trend.json")
