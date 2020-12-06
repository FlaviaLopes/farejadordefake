import os
import pandas as pd
import numpy as np

from keras import models, layers, regularizers, metrics, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.util import ngrams

import collections
import unicodedata

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt


# algumas funções úteis
def preprocess_embeddings(embeddings_path, max_words, embedding_dim, word_index):
    
    # Strongly inspired by listings 6.10 and 6.11 of "Deep Learning with Python", Francois Chollet, Manning.
    
    embeddings_idx = {};
    embeddings_file = open(embeddings_path)
    for row in embeddings_file:
        split_row = row.split(' ')
        if len(split_row) > 51:
            word = ' '.join(split_row[0:len(split_row) - 50])
            values = np.asarray(split_row[-50:])
        else:
            word = split_row[0]
            values = np.asarray(split_row[1:])
        embeddings_idx[word] = values
    embeddings_file.close()
    print(str(len(embeddings_idx)) + " words detected.")
    
    embeddings_mat = np.zeros((max_words, embedding_dim))
    print(embeddings_mat.shape)
    
    for word, idx in word_index.items():
        if (idx < max_words):
            embedding_vector = embeddings_idx.get(word)
            if embedding_vector is not None:
                embeddings_mat[idx] = embedding_vector
    
    return embeddings_mat

def build_model_nlp_lstm(regression_problem, max_words, embedding_dim, max_len, pre_trained_embeddings, embeddings_matrix, lstm_bidirectional, lstm_layers_neurons, lstm_layers_recurrent_dropout, lstm_layers_dropout, hidden_layers_neurons, hidden_activation_function, L1_coeffs, L2_coeffs, hidden_layers_dropout, final_layer_neurons, final_activation_function, model_optimizer, loss_function, metrics):
    
    model = models.Sequential()
    model.add(layers.Embedding(max_words,embedding_dim,input_length = max_len))
    if (pre_trained_embeddings == True):
        model.layers[0].set_weights([embeddings_matrix])
        model.layers[0].trainable = False
        
    for i in range(len(lstm_layers_neurons)):
        if ((i == 0) & (len(lstm_layers_neurons) > 1)):
            return_sequences_bool = True
        else:
            return_sequences_bool = False
            
        if (lstm_bidirectional == True):
            model.add(
                layers.Bidirectional(
                    layers.LSTM(
                        lstm_layers_neurons[i],
                        return_sequences = return_sequences_bool, 
                        recurrent_dropout = lstm_layers_recurrent_dropout[i], 
                        dropout = lstm_layers_dropout[i]
                    )
                )
            )            
        else:
             model.add(
                 layers.LSTM(
                     lstm_layers_neurons[i],
                     return_sequences = return_sequences_bool, 
                     recurrent_dropout = lstm_layers_recurrent_dropout[i], 
                     dropout = lstm_layers_dropout[i]
                 )
             )
    
    for i in range(len(hidden_activation_function)):        
        model.add(
            layers.Dense(
                hidden_layers_neurons[i], 
                kernel_regularizer = regularizers.l1_l2(l1 = L1_coeffs[i], l2 =  L2_coeffs[i]),  
                activation=hidden_activation_function[i]
            )
        )
        if (hidden_layers_dropout[i] > 0.0):
            model.add(layers.Dropout(hidden_layers_dropout[i]))
            
    if regression_problem:
        model.add(layers.Dense(final_layer_neurons))
    else:
        model.add(
            layers.Dense(
                final_layer_neurons,
                activation = final_activation_function
            )
        )
            
    model.compile(optimizer = model_optimizer, loss = loss_function, metrics = metrics)    
    return model

# --------------------------------------------------------------------------------------


test_split                     = 0.2
regression_problem             = False
max_words                      = 20000
embedding_dim                  = 50
max_len                        = 250
pre_trained_embeddings         = True
pre_trained_embeddings_path    =  f'skip_s{embedding_dim}.txt'
lstm_bidirectional             = True
lstm_layers_neurons            = [64,32]
lstm_layers_recurrent_dropout  = [0.20,0.1]
lstm_layers_dropout            = [0.20,0.1]
hidden_activation_function     = ['relu']
hidden_layers_neurons          = [64]
hidden_layers_L1_coeffs        = [0.00]
hidden_layers_L2_coeffs        = [0.00]
hidden_layers_dropout          = [0.00]
final_activation_function      = 'sigmoid'
final_layer_neurons            = 1
model_optimizer                = optimizers.RMSprop(lr=1e-4)
loss_function                  = 'binary_crossentropy'
metrics                        = ['accuracy']
n_epochs                       = 25
batch_size                     = 275

# --------------------------------------------------------------------------------------

interim_data = f'{project_dir}/data/interim/'
models = f'{project_dir}/models'

df = pd.read_csv(f'{interim_data}tweets.csv')
x_train, x_test, y_train, y_test = train_test_split(df.tweet, df.desinfo, random_state = 0, test_size=test_split)

# para contornar este problema será utilizado o método resample de sklearn.utils
# para criar novas amostras da classe minoritária e equilibrar o dataset

from sklearn.utils import resample

df_train = pd.concat([x_train, y_train], axis=1)

fato = df_train.loc[df_train.desinfo == 1, :].copy()
fake = df_train.loc[df_train.desinfo == 0, :].copy()

# upsample minority
fake_unsampled = resample(
    fake,
    replace=True, # sample with replacement
    n_samples=fato.shape[0], # match number in majority class
    random_state=0 # reproducible results
)

# combine majority and upsampled minority
upsampled = pd.concat([fato, fake_unsampled])

# check new class counts
upsampled.desinfo.value_counts()

x_train = upsampled['tweet'].copy()
x_train = x_train.astype('string')
y_train = upsampled['desinfo'].copy()
del upsampled
del df_train
del fake_unsampled

tokenizer=Tokenizer(num_words = max_words)#, oov_tok = "<OOV>")
tokenizer.fit_on_texts(x_train)
train_sequences = tokenizer.texts_to_sequences(x_train)
word_index = tokenizer.word_index
x_train = pad_sequences(train_sequences,maxlen = max_len, padding='post', truncating='post')


test_sequences = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(test_sequences,maxlen = max_len,padding='post', truncating='post')

embeddings_matrix = preprocess_embeddings(pre_trained_embeddings_path, max_words, embedding_dim, word_index)

model = build_model_nlp_lstm(
    regression_problem, 
    max_words, 
    embedding_dim, 
    max_len, 
    pre_trained_embeddings, 
    embeddings_matrix, 
    lstm_bidirectional,
    lstm_layers_neurons, 
    lstm_layers_recurrent_dropout, 
    lstm_layers_dropout,
    hidden_layers_neurons, 
    hidden_activation_function, 
    hidden_layers_L1_coeffs, 
    hidden_layers_L2_coeffs, 
    hidden_layers_dropout, 
    final_layer_neurons, 
    final_activation_function, 
    model_optimizer, 
    loss_function, 
    metrics
)

model.compile(optimizer = model_optimizer, loss = loss_function, metrics = metrics)
early_exit = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
hst = model.fit(
    x_train, 
    y_train, 
    epochs = n_epochs, 
    batch_size = batch_size, 
    steps_per_epoch = x_train.shape[0]//batch_size, 
    validation_data = (x_test, y_test), 
    verbose = 1, 
    callbacks =[early_exit]
)

model.save(f'{models}/model_nlp_lstm')
