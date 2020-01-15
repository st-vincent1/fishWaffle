from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, BatchNormalization, Lambda
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.utils as ku
import numpy as np
import re
import pprint as pp
import warnings
warnings.filterwarnings('ignore')

# Note: num_words does NOT reduce the size of the dictionary on its own; see
# https://github.com/keras-team/keras/issues/8092#issuecomment-372833486
""" This definition is if handling UNK words """
# total_words = 5000
# tokenizer = Tokenizer(lower = False, oov_token = 'UNK', filters = '!"#$%&()*+,./:;<=>?@\\^_`{|}~\t\n', num_words = total_words)
""" End """
tokenizer = Tokenizer(lower = False, oov_token = 'UNK', filters = '!"#$%&()*+,/:;<=>?@\\^_`{|}~\t\n')
# tokenizer = Tokenizer()
def sentencise(text):
	dump = ""
	line = text.readline()
	while(line):
		line = re.sub('\.\.\.', ' eos', line)
		dump = dump + line + ' '
		line = text.readline()
	print(dump)
	return dump

def dataset_preparation(data):
	# basic cleanup
	corpus = data.lower().split("\n")
	# tokenization
	tokenizer.fit_on_texts(corpus)
	total_words = len(tokenizer.word_index)


	""" Fragment below is for handling unknown words """
	# getting rid of infrequent words
	# pp.pprint(tokenizer.word_index)
	# KEY STEP FOR HANDLING UNK
	# tokenizer.word_index = {e:i for e,i in tokenizer.word_index.items() if i < total_words}
	# tokenizer.word_index[tokenizer.oov_token] = total_words
	# pp.pprint(len(tokenizer.word_index))
	# pp.pprint(tokenizer.texts_to_sequences(corpus))
	""" End """

	# create input sequences using list of tokens
	input_sequences = []
	for line in corpus:
		token_list = tokenizer.texts_to_sequences([line])[0]
		for i in range(1, len(token_list)):
			n_gram_sequence = token_list[:i+1]
			input_sequences.append(n_gram_sequence)

	# pad sequences
	max_sequence_len = max([len(x) for x in input_sequences])
	input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

	# create predictors and label
	predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
	label = ku.to_categorical(label, num_classes=total_words+1)

	return predictors, label, max_sequence_len, total_words

def create_model(predictors, label, max_sequence_len, total_words):

	model = Sequential()
	model.add(Embedding(total_words+1, 10, input_length=max_sequence_len-1))
	model.add(LSTM(512,
			  activation = 'tanh',
			  recurrent_activation = 'hard_sigmoid',
			  recurrent_dropout=0.0,
			  dropout = 0.2,
			  return_sequences = True))
	model.add(BatchNormalization())
	model.add(LSTM(512,
			  activation = 'tanh',
			  recurrent_activation = 'hard_sigmoid',
			  recurrent_dropout=0.0,
			  dropout = 0.2,
			  return_sequences = False))
	model.add(BatchNormalization())
	model.add(Dropout(0.5))
	# Temperature
	model.add(Lambda(lambda x: x / 0.8))
	model.add(Dense(total_words+1, activation='softmax'))

	model.compile(loss='categorical_crossentropy', optimizer=Adam(lr = 2e-3), metrics=['accuracy'])
	# earlystop = EarlyStopping(monitor='val_loss', min_delta=1, patience=5, verbose=0, mode='auto')
	model.fit(predictors, label, epochs=128, verbose=1, batch_size=512)
	print(model.summary())
	return model

def generate_text(seed_text, next_words, max_sequence_len):
	for _ in range(next_words):
		# Tokenize current predicted sequence and pad it
		token_list = tokenizer.texts_to_sequences([seed_text])[0]
		token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
		# Use model to predict next word
		predicted = model.predict_classes(token_list, verbose=0)

		output_word = ""
		for word, index in tokenizer.word_index.items():
			if index == predicted:
				output_word = word
				break

		seed_text += " " + output_word
	seed_text = re.sub(' eos', '...', seed_text)
	seed_text = '...'.join(i.strip().capitalize() for i in seed_text.split('...'))
	return seed_text

def save_model(filename, weights, model):
	model_json = model.to_json()
	with open(filename, "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights(weights)
	print("Saved model to disk")

def load_model(filename, weights):
	json_file = open(filename, 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = model_from_json(loaded_model_json)
	# load weights into new model
	model.load_weights(weights)
	print("Loaded model from disk")
	return model

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))

# Analysing punctuation in data
def analyse(text):
	res_dic = {}
	dump = ""
	line = text.readline()
	# Analysing comma words
	while(line):
		res = re.findall('\, [a-z]*', line)
		res_dic.update(wordListToFreqDict(res))
		dump += line
		line = text.readline()
	pp.pprint(res_dic)
	print(max(res_dic, key = res_dic.get))
	return res_dic

data = open('../data/trainData/train.txt')

# Analysing punctuation in data
# analyse(data)

data = sentencise(data)
predictors, label, max_sequence_len, total_words = dataset_preparation(data)
model = create_model(predictors, label, max_sequence_len, total_words)
save_model('conv_model.json', 'conv_model.h5', model)

# model = load_model('k_punk_model.json', 'model.h5')
print(generate_text("Is that yours? ", 500, max_sequence_len))
