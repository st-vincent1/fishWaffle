"""
Initialising:
def waffle_initialise

Generating:
def waffle_generate
"""

import modeling as mo
import sys
import os
import re


# Later to be corrected to wrapped 60-90
ans_len = 68

try:
	rel_path = re.sub(r'[^/]+$', '', os.getcwd())
	data_path = os.path.join(rel_path, 'data/trainData/')
	model_path = os.path.join(rel_path, 'models/')
	prompt_path = os.path.join(rel_path, 'data/prompts/')

	model_choice = (os.path.join(model_path, 'conv_model_origin.json'), os.path.join(model_path, 'conv_model_origin.h5'))
	data = open(os.path.join(data_path, 'train_origin.txt'))
	else:
		raise Exception("An error occured")
except:
	print("Error")
	exit()

# print("Sentencising")
data = mo.sentencise(data)
# print("Prep")
predictors, label, max_sequence_len, total_words = mo.dataset_preparation(data)
# print("Loading model")
model = mo.load_model(model_choice[0], model_choice[1])
# Change later to reading prompts from file
f = open(os.path.join(prompt_path, 'waffle_prompts.txt'), 'r')
# prompts = f.read().splitlines()
# print(prompts)
prompts = "Baby I'm in the mood for you".split()

print("Generating text")

"""

while(system is running):
	wait for a prompt
	[now someone just sent a prompt our way]
	generate text from prompt

"""

# the g.sth things were used to generate prompts for questionnaire
for prompt in prompts:
	print(mo.generate_text(model, prompt, ans_len, max_sequence_len))
	# g = open(os.path.join('../data/results/', choice + '_' + prompt[:12] + '.txt'), 'w+')
	# g.write(mo.generate_text(model, prompt, ans_len, max_sequence_len))

# Alternative prompt generator: give me input (commandline), i'll give you an answer (works just once)
# prompt = input("Give prompt\n")
# print(generate_text(prompt, ans_len, max_sequence_len))
