import numpy as np
import csv, json, random
from sklearn.linear_model import LinearRegression

def open_csv(fname):
    result = []
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        first_time = True
        for row in csv_reader:
            if first_time:
                first_time = False
            else:
                result.append((row[0], row[1], row[2]))
    return result

def get_only_ratings(result):
    x = []
    count = 1
    for item in result:
        x.append(count)
        count += 1
    y = [record[2] for record in result]
    return x,y

def save_to_json(data, fname):
    with open(fname, 'w') as f:
        json.dump(data, f)

if __name__=="__main__":
    result = open_csv("yelp_collection.csv")
    x,y = get_only_ratings(result)

    #shuffle it randomize it.
    #random.shuffle(y)

    index = int(len(y)*0.9)

    training_data = y[:index]
    test_data = x[index:]
    result = y[index:]
    #print(len(y))
    #print(len(training_data))
    #print(len(test_data))


    #turn result into np
    x = np.array(x).reshape((-1,1))
    y = np.array(y)

    #this is getting the length of np.array
    future_x = x.shape[0]+1

    #create a linear regression model (initialize)
    linear_reg_model = LinearRegression().fit(x,y)

    #predict the next x-value
    y_pred = linear_reg_model.predict(future_x)
    print(y_pred)
