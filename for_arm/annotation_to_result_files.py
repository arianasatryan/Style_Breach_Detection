import os
import json

annotated_files_path = '/Users/hekpo/PycharmProjects/Karas/for_arm/data/train_dataset'
json_results_path = '/Users/hekpo/PycharmProjects/Karas/for_arm/results/train_results'
annotated_files = os.listdir(annotated_files_path+'/')

def write_json_result(filename, positions):
    with open(json_results_path + '/' + ('%s.truth'%filename), 'w', encoding = 'utf-8') as fout:
        json.dump({"borders": positions}, fout, indent = 4)

def rewrite_file(filename, text):
    with open(annotated_files_path + '/' + ('%s.txt' % filename), 'w', encoding = 'utf-8') as fout:
        fout.write(text)

def annotation_to_truth_files():
    for file in annotated_files:
        filename, file_format = os.path.splitext(file)
        with open(annotated_files_path + '/' + file, encoding = 'utf-8')as fin:
            text = fin.read()
            start = 0
            end = len(text) - 1
            borders = []
            while True:
                finded_split_sign_index = text.find('$', start, end)
                if finded_split_sign_index != -1:
                    text = text[:finded_split_sign_index] + text[finded_split_sign_index + 1:]
                    borders.append(finded_split_sign_index)
                    start = finded_split_sign_index
                else:
                    break
        write_json_result(filename, borders)
        rewrite_file(filename, text)


annotation_to_truth_files()
