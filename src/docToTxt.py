import os
import re
import uuid
import textract

rel_path = re.sub(r'[^/]+$', '', os.getcwd())
in_dir = os.path.join(rel_path, 'data/docData')
out_dir = os.path.join(rel_path, 'data/convData')

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

for process_file in os.listdir(in_dir):
    file, ext = os.path.splitext(process_file)
    # Create a new text file
    dest_file_path = file + ".txt"
    # Extract contents
    content = textract.process(os.path.join(in_dir, process_file))
    # Prepare file for writing
    write_text_file = open(os.path.join(out_dir, dest_file_path), "wb")
    write_text_file.write(content)
    write_text_file.close()
