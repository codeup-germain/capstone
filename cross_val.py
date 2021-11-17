def split(df,target,test_size):
    # Making the dataframe without the target as x. Dropping target column and adding it to y
    X,y = df.drop(columns = target), df[target]
    # Running train test split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = .2)
    # Getting the validation set from the train
    X_train, X_validate, y_train, y_validate = train_test_split(X_train,y_train, test_size = .3333)
    return (X_train, y_train, X_validate,y_validate, X_test, y_test)