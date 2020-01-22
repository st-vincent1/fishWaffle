import modeling as mo
import sys
import os
import re

try:
	# choice = input"Choose model (origin/speakers)\n")
	choice = str(sys.argv[1])
	rel_path = re.sub(r'[^/]+$', '', os.getcwd())
	data_path = os.path.join(rel_path, 'data/trainData/')
	model_path = os.path.join(rel_path, 'models/')

	if choice == 'origin':
		model_choice = (os.path.join(model_path, 'conv_model_origin.json'),
					   os.path.join(model_path, 'conv_model_origin.h5'))
		data = open(os.path.join(data_path, 'train_origin.txt'))
	elif choice == 'speakers':
		model_choice = (os.path.join(model_path, 'conv_model_speakers.json'),
					   os.path.join(model_path, 'conv_model_speakers.h5'))
		data = open(os.path.join(data_path, 'train_speakers.txt'))
	else:
		raise Exception("An error occured")
except:
	print("Error; to run correctly, supply 1 argument from {origin, speakers}")
	exit()

data = mo.sentencise(data)
predictors, label, max_sequence_len, total_words = mo.dataset_preparation(data)
model = mo.create_model(predictors, label, max_sequence_len, total_words)
mo.save_model(model_choice[0], model_choice[1], model)
