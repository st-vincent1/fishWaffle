import modeling as mo
import sys
import os
import re


# Later to be corrected to wrapped 60-90
ans_len = 68

try:

	# choice = input"Choose model (origin/speakers)\n")
	choice = str(sys.argv[1])

	rel_path = re.sub(r'[^/]+$', '', os.getcwd())
	data_path = os.path.join(rel_path, 'data/trainData/')
	model_path = os.path.join(rel_path, 'models/')
	prompt_path = os.path.join(rel_path, 'data/prompts/')
	if choice == 'origin':
		model_choice = (os.path.join(model_path, 'conv_model_origin.json'), os.path.join(model_path, 'conv_model_origin.h5'))
		print(model_choice)
		data = open(os.path.join(data_path, 'train_origin.txt'))
	elif choice == 'speakers':
		model_choice = (os.path.join(model_path, 'conv_model_speakers.json'),
					   os.path.join(model_path, 'conv_model_speakers.h5'))
		data = open(os.path.join(data_path, 'train_speakers.txt'))
	else:
		raise Exception("An error occured")
except:
	print("Error")
	exit()

print("Sentencising")
data = mo.sentencise(data)
print("Prep")
predictors, label, max_sequence_len, total_words = mo.dataset_preparation(data)
print("Loading model")
model = mo.load_model(model_choice[0], model_choice[1])
# Change later to reading prompts from file
f = open(os.path.join(prompt_path, 'waffle_prompts.txt'), 'r')
prompts = f.read().splitlines()
print(prompts)
# "Baby I'm in the mood for you".split()

print("Generating text")
for prompt in prompts:
	# print(mo.generate_text(model, prompt, ans_len, max_sequence_len))
	g = open(os.path.join('../data/results/', choice + '_' + prompt[:12] + '.txt'), 'w+')
	g.write(mo.generate_text(model, prompt, ans_len, max_sequence_len))

# prompt = input("Give prompt\n")
# print(generate_text(prompt, ans_len, max_sequence_len))
