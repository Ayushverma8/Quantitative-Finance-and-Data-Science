# Fitting various models on the data and a comparative analysis of performance

import pandas as pd
import numpy as np
import scipy
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

# Load the data from csv file
AAPL = pd.read_csv("AAPL.csv")

# Adjust predictors via train_names
# train_names = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
train_names = ['MACD 12 26 9', 'MACD 12 26 9 Signal', 'MACD 12 26 9 Hist', '5d Avg Vol vs 30d Avg Vol', '10d Avg Vol vs 90d Avg Vol', '14d RSI', '%K Full', '%D Full']

# Split the dataset into train set and test set
X_train, X_test, y_train, y_test = train_test_split(AAPL[train_names], AAPL['10d Label'], test_size=0.25, random_state=33)

# Standardized data by normalization
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)


def logisticRegression():
    # Initialize LogisticRegression Model
    lr = LogisticRegression()
    # Fit data and train
    lr.fit(X_train, y_train)
    # Predict test set
    lr_y_predict = lr.predict(X_test)

    # Analyze the results
    print("Accuracy of Logistic Regression Classifier:", lr.score(X_test, y_test))
    print(classification_report(y_test, lr_y_predict))


def sgdClassifier():
    # Initialize SGDClassifier Model
    sgdc = SGDClassifier()
    sgdc.fit(X_train, y_train)
    sgdc_y_predict = sgdc.predict(X_test)

    # Analyze the results
    print("Accuracy of SGD Classifier:", sgdc.score(X_test, y_test))
    print(classification_report(y_test, sgdc_y_predict))


def linearSVC():
    lsvc = LinearSVC()
    lsvc.fit(X_train, y_train)
    y_predict = lsvc.predict(X_test)

    print("Accuracy of Linear SVC:", lsvc.score(X_test, y_test))
    print(classification_report(y_test, y_predict))


def NBClassifier():
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    y_predict = mnb.predict(X_test)

    print("Accuracy of NB Classifier:", mnb.score(X_test, y_test))
    print(classification_report(y_test, y_predict))


def kNNClassifier():
    knc = KNeighborsClassifier()
    knc.fit(X_train, y_train)
    y_predict = knc.predict(X_test)

    print("Accuracy of kNN Classifier:", knc.score(X_test, y_test))
    print(classification_report(y_test, y_predict))


from sklearn import svm
from sklearn import cross_validation

if __name__ == '__main__':
    logisticRegression()
    sgdClassifier()
    linearSVC()
    NBClassifier()
    kNNClassifier()

    # clf = svm.SVC(kernel='linear', C=1)
    # scores = cross_validation.cross_val_score(clf, X_train, y_train, cv = 10)
    # print(type(scores))
    # print(scores)
