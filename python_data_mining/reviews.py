from selenium import webdriver as web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, re, csv, datetime, json

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist

def rating_filter(text):
    return "".join(text[6:9])

def rating_date_filter(text):
    temp = text.split(" ")
    return temp[0] + " " + temp[1]

def startBrowser(url, text="Kiraku"):

    def locateTextReviews(driver):
        review = None
        #review = driver.find_element_by_xpath('.//span[contains(@class, "review-full-text")]').text
        try:
            review = driver.find_element_by_xpath('.//span[@class = "review-full-text")]').text
            if review == "":
                review = driver.find_element_by_xpath('.//span[starts-with(@class, "r-i")]').text
        except:
            review = driver.find_element_by_xpath('.//span[starts-with(@class, "r-i")]').text
        return review

    browser = web.Chrome()
    browser.get(url)
    search = browser.find_element_by_name('q')
    search.send_keys(text)
    search.send_keys(Keys.RETURN)

    time.sleep(2)

    try:
        google_reviews = browser.find_element_by_xpath('//span[contains(text(), "Google reviews")]')
        google_reviews.click()
    except NoSuchElementException as ex:
        print(ex.message)


    time.sleep(4)

    #NkCsjc contains method
    try:
        scrollDownButton = browser.find_element_by_xpath('//g-dropdown-button[contains(@class, "NkCsjc")]')
        scrollDownButton.click()
    except NoSuchElementException as ex:
        print(ex.message)

    time.sleep(1)

    try:
        newestButton = browser.find_element_by_xpath('//div[contains(text(), "Newest")]')
        newestButton.click()
    except NoSuchElementException as ex:
        print(ex.message)


    time.sleep(3)

    page = browser.find_element_by_xpath('//div[contains(@class, "dialog-list")]')
    #browser.find_element_by_tag_name('body').send_keys(Keys.END)
    #browser.execute_script("return arguments[0].scrollIntoView();", page)
    #star-s

    #get the total ratings reviews
    total_ratings = browser.find_element_by_xpath('//span[contains(@class, "p13zmc")]')
    total_ratings = total_ratings.text
    total_ratings = ''.join(i for i in total_ratings if i.isdigit())

    while True:
        ratingboxes = browser.find_elements_by_xpath('//div[contains(@class, "google-review")]')
        browser.execute_script('arguments[0].scrollIntoView(true);', ratingboxes[-1])

        #print(len(ratingboxes), total_ratings)
        if len(ratingboxes) >= int(total_ratings):
            break

    #print('loop is done')
    result_list = []
    ratings_in_reviews = browser.find_elements_by_xpath('//span[contains(@class, "star-s")]')
    #print("collected ratings")

    #dehysf - collecting the time it got rated..
    rating_dates = browser.find_elements_by_xpath('//span[contains(@class, "dehysf")]')
    #print(rating_dates)

    #review-more-link
    reviewMoreButtons = browser.find_elements_by_xpath('//span[contains(@class, "review-more-link")]')
    for eachButton in reviewMoreButtons:
        eachButton.click()

    #reviews_text: Jtu6Td, subclass starts with r- or review-snipset
    text_reviews = browser.find_elements_by_class_name("Jtu6Td")

    pure_reviews = []
    for item in text_reviews:
        pure_text = locateTextReviews(item)
        pure_reviews.append(pure_text)

    for rating, date, r_text in zip(ratings_in_reviews[1:], rating_dates, pure_reviews):
        status = None
        r_temp = rating.get_attribute("aria-label")
        r_temp = rating_filter(r_temp)
        if float(r_temp) < 4.0:
            status = "negative"
        else:
            status = "positive"
        d_temp = rating_date_filter(date.text)
        result_list.append((r_temp, d_temp, r_text, status))

    return result_list

def convert_to_dictionary(ratings):
    p_list = []
    n_list = []
    prev_date = None

    p_dict = {}
    n_dict = {}

    for elem in ratings:
        #rating = elem[0]
        date = elem[1]
        #text = elem[2]
        status = elem[3]

        if not prev_date:
            if status == "positive":
                p_dict["time"] = date
                p_dict["count"] = 1

                n_dict["time"] = date
                n_dict["count"] = 0
            else:
                n_dict["time"] = date
                n_dict["count"] = 1

                p_dict["time"] = date
                p_dict["count"] = 0
            prev_date = date

        else:
            if prev_date != date:
                p_list.append(p_dict)
                n_list.append(n_dict)
                p_dict = {}
                n_dict = {}

                if status == "positive":
                    p_dict["time"] = date
                    p_dict["count"] = 1

                    n_dict["time"] = date
                    n_dict["count"] = 0
                else:
                    n_dict["time"] = date
                    n_dict["count"] = 1

                    p_dict["time"] = date
                    p_dict["count"] = 0
                prev_date = date
            else:
                if status == "positive":
                    p_dict["count"] += 1
                else:
                    n_dict["count"] += 1

    final_dict = {}
    final_dict["positive"] = p_list
    final_dict["negative"] = n_list
    return final_dict

def nltk_and_string_frequency(ratings):
    tokenizer = RegexpTokenizer(r'\w+')

    pos_list_words = []
    neg_list_words = []
    for elem in ratings:
        status = elem[3]
        tokens = tokenizer.tokenize(elem[2])
        tokens = clean_text(tokens)
        filtered = [w for w in tokens if w not in stopwords.words('english')]

        if status == "positive":
            pos_list_words += filtered
        else:
            neg_list_words += filtered

    fdist = FreqDist(pos_list_words)
    pos_fd_final = fdist.most_common(10)
    fdist = FreqDist(neg_list_words)
    neg_fd_final = fdist.most_common(10)

    pos_dic = []
    neg_dic = []

    for item in pos_fd_final:
        temp_dic = {}
        temp_dic['word'] = item[0]
        temp_dic['count'] = item[1]
        pos_dic.append(temp_dic)

    for item in neg_fd_final:
        temp_dic = {}
        temp_dic['word'] = item[0]
        temp_dic['count'] = item[1]
        neg_dic.append(temp_dic)

    return pos_dic, neg_dic

def clean_text(words):
    cleaned = []
    for w in words:
        temp = w.lower()
        cleaned.append(temp)
    return cleaned

def reverse_list(ratings):
    check_point = len(ratings) * -1
    index = -1
    reverse_order_list = []
    while index > check_point:
        reverse_order_list.append(ratings[index])
        index -= 1

    return reverse_order_list

def write_to_json(final_product, fname):
    with open(fname, 'w') as f:
        json.dump(final_product, f)
    f.close()

def write_into_text(final_product, fname):
    with open(fname, 'w') as f:
        for item in final_product:
            if item[2] is not "":
                f.write(item[2]+"\n")
        f.close()

def write_into_json(final_product, fname):
    final_dict = {}
    final_dict['positive'] = [];
    final_dict['negative'] = [];
    with open(fname, 'w') as f:
        for item in final_product:
            if item[2] is not "":
                if item[3] == 'positive':
                    final_dict['positive'].append(item[2])
                else:
                    final_dict['negative'].append(item[2])
        json.dump(final_dict, f)

if __name__ == "__main__":
    ratings = startBrowser(url="https://www.google.com")

    pos_fd, neg_fd = nltk_and_string_frequency(ratings)
    #write_to_json(pos_fd, 'pos_fd.json')
    #write_to_json(neg_fd, 'neg_fd.json')

    #write_into_text(ratings, "txt_reviews.txt")
    write_into_json(ratings, "text_reviews.json")
    #write_to_json(ratings, 'all_reviews.json')

    #ratings = reverse_list(ratings)
    #dic_ratings = convert_to_dictionary(ratings)
    #print(dic_ratings)
    #write_to_json(dic_ratings, 'reviews.json')
