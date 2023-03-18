import numpy as np
import pandas as pd
import json, csv, collections
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, top_k_accuracy_score
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, LayerNormalization, Embedding, LSTM, Bidirectional
from keras import regularizers
from keras.callbacks import EarlyStopping
from pathlib import Path 

NUMBER_OF_DIMENSIONS = 3352
for min_count in [10, 20, 50, 100]:

    names_data = pd.read_csv("./names.txt", names=['name'], sep=",,,,,,,")
    value_counts = names_data['name'].value_counts()
    frequent_values = value_counts[value_counts >= min_count].index
    names_data = names_data[names_data['name'].isin(frequent_values)]
    index = names_data.index

    vectors_data = pd.read_csv("./vectors.txt", names=['paths'])
    vectors_data = vectors_data.iloc[index]

    series_data = pd.read_csv("./series.txt", names=['series'], sep=",,,,,,,")
    series_data = series_data.iloc[index]

    df = pd.concat([vectors_data, names_data, series_data], axis=1)

    train, test = train_test_split(df, test_size=0.05,
                                    stratify=df['name'],
                                    random_state=42)

    train, dev = train_test_split(train, test_size=0.1, random_state=42)

    train.to_csv(Path('sequence/res/{}_train.csv'.format(min_count)), index=False, header=False) 
    test.to_csv(Path('sequence/res/{}_test.csv'.format(min_count)), index=False, header=False) 
    dev.to_csv(Path('sequence/res/{}_dev.csv'.format(min_count)), index=False, header=False) 
