from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential, model_from_json
import tensorflow.keras.utils as ku
import numpy as np
import re
import pprint as pp
import warnings
warnings.filterwarnings('ignore')

# Max words for dictionary
total_words = 5000
# Note: num_words does NOT reduce the size of the dictionary on its own; see
# https://github.com/keras-team/keras/issues/8092#issuecomment-372833486
tokenizer = Tokenizer(oov_token = 'UNK', num_words = total_words)
# tokenizer = Tokenizer()
def sentencise(text):
	dump = ""
	line = text.readline()
	while(line):
		line = re.sub('\.(\r|\n| )+', ' EOS ', line)
		dump = dump + line + ' '
		line = text.readline()
		# Get rid of multiple apostrophe confusions
		# line = re.sub(r"([a-z]+)('?)([a-z]?)", r'\1', line)
	return dump

def dataset_preparation(data):

	# basic cleanup
	corpus = data.lower().split("\n")
	# tokenization
	tokenizer.fit_on_texts(corpus)
	# getting rid of infrequent words
	# pp.pprint(tokenizer.word_index)
	# pp.pprint(tokenizer.texts_to_sequences(corpus))

	# KEY STEP FOR HANDLING UNK
	# tokenizer.word_index = {e:i for e,i in tokenizer.word_index.items() if i < total_words}
	# tokenizer.word_index[tokenizer.oov_token] = total_words
	pp.pprint(len(tokenizer.word_index))
	# pp.pprint(tokenizer.texts_to_sequences(corpus))

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
	model.add(LSTM(100, return_sequences = True))
	model.add(Dropout(0.05))
	model.add(LSTM(100))
	model.add(Dense(total_words+1, activation='softmax'))

	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	earlystop = EarlyStopping(monitor='val_accuracy', min_delta=1, patience=5, verbose=0, mode='auto')
	model.fit(predictors, label, epochs=100, verbose=1, callbacks=[earlystop], batch_size=2096)
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
	seed_text = re.sub(' eos', '.', seed_text)
	seed_text = '. '.join(i.strip().capitalize() for i in seed_text.split('.'))
	return seed_text
	# return seed_text

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
	model.load_weights("k_punk_model.h5")
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

data = open('../data/k_punk_spellchecked.txt')

# Analysing punctuation in data
# analyse(data)

data = sentencise(data)
predictors, label, max_sequence_len, total_words = dataset_preparation(data)
model = create_model(predictors, label, max_sequence_len, total_words)
save_model('k_punk_model.json', 'k_punk_model.h5', model)

# model = load_model('k_punk_model.json', 'model.h5')
print(generate_text("And don't get me started on", 100, max_sequence_len))
