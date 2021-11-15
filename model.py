from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

def baseline_acc(X,y, strategy = "most_frequent",random_state = 174):
    # generates a baseline model using most frequent, since there are only two outcomes we are predicting.
    model = DummyClassifier(strategy = strategy, random_state = random_state)
    model.fit(X,y)
    # prints an accuracy for the baseline model.
    print(f"Baseline accuracy score is: {model.score(X,y):.3%}")
    # Returns the baseline model back for use.
    return model

def tree_model(X,y,max_depth = 5, criterion = "gini", splitter = "best", random_state = 174):
    dt_model = DecisionTreeClassifier(max_depth = max_depth, criterion = criterion, splitter = splitter, random_state = random_state)
    dt_model.fit(X,y)
    y_pred = dt_model.predict(X)
    print(f"This decision tree models accuracy score is: {dt_model.score(X,y):.3%}")
    return dt_model,y_pred

def rand_forest(X,y, n_estimators = 30, criterion = "gini",max_depth = 9, random_state = 174, min_samples_leaf = 3):
    rf_model = RandomForestClassifier(
        n_estimators = n_estimators,
        criterion = criterion,
        max_depth = max_depth,
        min_samples_leaf = min_samples_leaf,
        random_state = random_state )
    rf_model.fit(X,y)
    y_pred = rf_model.predict(X)
    print(f"This Random Forest models accuracy score is: {rf_model.score(X,y):.3%}")
    return rf_model,y_pred

def knneighbors(X,y,n_neighbors = 5, weights = "uniform",leaf_size = 10,p = 2):
    knn_model = KNeighborsClassifier(
        n_neighbors = n_neighbors,
        weights = weights,
        leaf_size = leaf_size,
        p = p,)
    knn_model.fit(X,y)
    y_pred = knn_model.predict(X)
    print(f"This K Nearest Neighbor models accuracy score is: {knn_model.score(X,y):.3%}")
    return knn_model,y_pred

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

def cmatrix(y_true, y_pred):
    '''
    Takes in true and predicted values to create a confusion matrix,
    then ouputs dictionary holding the true pos, true, neg, false pos,
    and false neg rates discerned from the matrix
    Used in conjunction with model_report
    '''

    # define confusion matrix, convert to dataframe
    cmatrix = confusion_matrix(y_true, y_pred)
    cmatrix = pd.DataFrame(confusion_matrix(y_true, y_pred),
                           index=['True Retain', 'True Churn'],
                           columns=['Predict Retain', 'Predict Churn'])
    # assign TN, FN, TP, FP
    true_neg = cmatrix.iloc[0, 0]
    false_neg = cmatrix.iloc[0, 1]
    true_pos = cmatrix.iloc[1, 0]
    false_pos = cmatrix.iloc[1, 1]
    #do math to find rates
    tpr = true_pos / (true_pos + false_neg)
    tnr = true_neg / (true_neg + false_pos)
    fpr = 1 - tnr
    fnr = 1 - tpr
    cmatrix_dict = {'tpr':tpr, 'tnr':tnr, 'fpr':fpr, 'fnr':fnr}

    return cmatrix_dict

def model_report(y_true, y_pred):
    '''
    Takes in true and predicted values to create classificant report
    dictionary and uses cmatrix function to obtain positive and
    negative prediction rates, prints out table containing all metrics
    for the positive class of target
    '''

    # create dictionary for classification report and confusion matrix
    report_dict = classification_report(y_true, y_pred, output_dict=True)
    cmatrix_dict = cmatrix(y_true, y_pred)
    # print formatted table with desired information for model report
    print(f'''
            *** Model  Report ***  
            ---------------------              
 _____________________________________________
|            Positive Case: blue win==1          |
|            Negative Case: red win==0          |
|---------------------------------------------|
|                 Accuracy: {report_dict['accuracy']:>8.2%}          |
|       True Positive Rate: {cmatrix_dict['tpr']:>8.2%}          |
|      False Positive Rate: {cmatrix_dict['fpr']:>8.2%}          |
|       True Negative Rate: {cmatrix_dict['tnr']:>8.2%}          |
|      False Negative Rate: {cmatrix_dict['fnr']:>8.2%}          |
|                Precision: {report_dict['1']['precision']:>8.2%}          |
|                   Recall: {report_dict['1']['recall']:>8.2%}          |
|                 F1-Score: {report_dict['1']['f1-score']:>8.2%}          |
|                                             |
|         Positive Support: {report_dict['1']['support']:>8}          |
|         Negative Support: {report_dict['0']['support']:>8}          |
|            Total Support: {report_dict['macro avg']['support']:>8}          |
|_____________________________________________|
''')