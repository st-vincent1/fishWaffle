# import relevant libraries

import modeling as mo
import sys
import os
import re
import warnings
warnings.filterwarnings('ignore')

def generate_waffle(model, prompt):
    output = mo.generate_text(model, prompt, ANS_LEN, WAFFLE_MAX_SEQUENCE_LENGTH)
    return output

# Later to be corrected to wrapped 60-90
ANS_LEN = 68

# load data files

try:
    rel_path = re.sub(r'[^/]+$', '', os.getcwd())
    data_path = os.path.join(rel_path, 'data/trainData/')
    model_path = os.path.join(rel_path, 'models/')

    model_choice = (os.path.join(model_path, 'conv_model_origin.json'), os.path.join(model_path, 'conv_model_origin.h5'))
    data = open(os.path.join(data_path, 'train_origin.txt'))
except:
    print("Error")
    exit()


# Sentencising
data = mo.sentencise(data)
# Prep (TODO dump tokenizer)
predictors, label, WAFFLE_MAX_SEQUENCE_LENGTH, total_words = mo.dataset_preparation(data)



def main():
    # Load model (run once)
    model = mo.load_model(model_choice[0], model_choice[1])

    # for each prompt
    prompt = "hello, how are you?"
    waffle_output = generate_waffle(model, prompt)
    print(waffle_output)

if __name__ == '__main__':
    main()

