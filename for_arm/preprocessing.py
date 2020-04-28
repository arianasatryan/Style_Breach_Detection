import os
import re

train_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/train_dataset/'
test_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/test_dataset/'
train_files = os.listdir(train_path)
test_files = os.listdir(test_path)
train_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/train_results/'
test_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/test_results/'

def simbol_correction_in(files):
    if files == train_files:
        path = train_path
    else:
        path = test_path
    for file in files:
            with  open(path + file, 'r', encoding = 'utf-8') as fin:
                lines = fin.readlines()
                lines = [x.strip() for x in lines]
                new_lines=[]
                for line in lines:
                    #brackets
                    line = re.sub('> *>', '»', line)
                    line = re.sub('< *<', '«', line)
                    #rome dates
                    line = re.sub('\) ?\(', 'X', line)
                    line = re.sub('՝/', 'V', line)
                    line = re.sub('>Հ', 'X', line)
                    line = re.sub(' ?\| ?', 'I', line)
                    #punctation
                    line = re.sub('↑', '', line)
                    line = re.sub('’', '՛', line)
                    #enumeration
                    line = re.sub('^ֆ( +|\.)', '~ ', line)
                    line = re.sub('^՝/( +|\.)', '— ', line)
                    line = re.sub('^-', '— ', line)
                    line = re.sub('^շ( +|\.)', '2 ', line)
                    line = re.sub('^[ՅՑ]( +|\.)', '3 ', line)
                    line = re.sub('^Չ( +|\.)', '9 ', line)
                    #chars
                    line = re.sub('՝ս', 'ն', line)
                    line = re.sub('Ււ', 'խ', line)
                    line = re.sub('Ւփ', 'խի', line)
                    # deleting [anything]     #doenr match newlines
                    line = re.sub('\[.*\]', '', line)
                    #վերջածանցներ
                    line = re.sub(' *թ *յ *ա *', 'թյա', line)
                    line = re.sub(' *թ *յ *ո *', 'թյո', line)
                    line = re.sub('սծ ', 'ած', line)
                    line = re.sub('ևծ ', 'ած', line)
                    #additional processing for numbers with շ Յ Ց Չ
                    line = re.sub('շ\d+', '', line)
                    line = re.sub('[ՅՑ]\d+', '', line)
                    line = re.sub('[Օօ]\d+', '', line)
                    line = re.sub('Չ\d+', '', line)
                    #adding whitespace between numer and թվ․ թ․ թթ․
                    if (re.search('\d+թթ(\.|․)', line)):
                        line = re.sub('թթ(\.|․)', ' թթ․', line)
                    if (re.search('\d+թ(\.|․)', line)):
                        line = re.sub('թ(\.|․)', ' թ․', line)
                    if (re.search('\d+թվ(\.|․)', line)):
                        line = re.sub('թվ(\.|․)', ' թվ․', line)
                    if (re.search('\d+դդ(\.|․)', line)):
                        line = re.sub('դդ(\.|․)', ' դդ․', line)
                    if (re.search('\d+դ(\.|․)', line)):
                        line = re.sub('դ(\.|․)', ' դ․', line)
                    #adding whitespace between number and կմ մ
                    if (re.search('\d+կմ', line)):
                        line = re.sub('կմ', ' կմ', line)
                    if (re.search('\d+մ', line)):
                        line = re.sub('մ', ' մ', line)
                    #char->digit
                    words = line.split(' ')
                    for i in range(len(words)):
                        if (re.search('(\d+|[շՕօՅՑՉ])[շՕօՅՑՉ](\d+| *|[շՕօՅՑՉ։-])', words[i]) != None):   #!warning about Չօգնել & #doesnt match բառշ9
                            words[i] = re.sub('շ', '2', words[i])
                            words[i] = re.sub('[ՅՑ]', '3', words[i])
                            words[i] = re.sub('[Օօ]', '0', words[i])
                            words[i] = re.sub('Չ', '9', words[i])

                        if (re.search('([ա-ն]|[ո-ֆ]|»)\d', words[i]) != None):
                            words[i] = re.sub('\d+', '', words[i])
                    new_line =' '.join(words)
                    new_lines.append(new_line)
            with  open(path+file, 'w', encoding = 'utf-8') as fout:
                fout.write('\n'.join(new_lines))

"""
def write_corr_sized_docs(file_path, file, list, i):
    filename, file_format = os.path.splitext(file)
    if list:
        del list[-1]
        text = ''.join([str(elem) for elem in list])
        with open(file_path + filename + '_' + str(i) + file_format, 'w', encoding = 'utf-8')as fout:
            fout.write(text)

def paragraph_correction_in(files):
    if files == train_files:
        path = train_path
    else:
        path = test_path
    for file in files:
        with open(path + file, encoding = 'utf-8') as infile:
            lines = infile.readlines()
            new_lines = []
            index = 0
            #deleting double newlines
            while index < len(lines) - 1:
                while lines[index] == '\n' and lines[index + 1] == '\n':
                    del lines[index + 1]
                index += 1
            index = 0
            while index < len(lines) - 2:
                while lines[index] == '\n' and lines[index + 2] == '\n':
                    if re.search('։$', lines[index - 1]):
                        new_lines.append(lines[index])
                        new_lines.append(lines[index + 1])
                        index += 3
                    else:
                        new_lines.append(lines[index + 1])
                        index += 2
                if (index < len(lines) - 2):
                    new_lines.append(lines[index])
                    index += 1
        l = len(lines)
        new_lines.append(lines[l - 2])
        new_lines.append(lines[l - 1])
        text = ''.join(new_lines)
        with open(path + file, 'w', encoding = 'utf-8') as outfile:
            outfile.write(text)


def file_size_correction_in(files):
    if files == train_files:
        path = train_path
    else:
        path = test_path
    for file in files:
        with open(path + file, encoding = 'utf-8')as fin:
            filename, file_format = os.path.splitext(os.path.basename(path + file))
            kb_size = int(os.stat(path + file).st_size/1024)
            if kb_size > 500:
                text = fin.read()
                parag = get_paragraphs_of(path + file)
                paragcount = len(parag)
                list1 = []
                list2 = []
                list3 = []
                i = 0
                if kb_size < 1000:
                    for p in parag:
                        if(i < paragcount/2):
                            i += 1
                            list1.append(p)
                            list1.append('\n\n')
                        else:
                            i += 1
                            list2.append(p)
                elif kb_size > 1000 and kb_size < 1500:
                    for p in parag:
                        if (i < paragcount / 3):
                            list1.append(p)
                            list1.append('\n\n')
                            i += 1
                        elif (i > paragcount/3 and i < 2*paragcount/3):
                            list2.append(p)
                            list2.append('\n\n')
                            i += 1
                        else:
                            list3.append(p)
                            list3.append('\n\n')
                            i += 1
        if kb_size > 500:
            os.remove(path + file)
            write_corr_sized_docs(path, file, list1, 1)
            write_corr_sized_docs(path, file, list2, 2)
            write_corr_sized_docs(path, file, list3, 3)
"""

def delete_whitelines_in(files):
    if files == train_files:
        path = train_path
    else:
        path = test_path
    for file in files:
        with open(path + file, encoding = 'utf-8') as infile:
            filename, file_format = os.path.splitext(file)
            lines = infile.readlines()
            new_lines = []
            index = 0
            for i in range(len(lines)):
                lines[i]=re.sub(' \n', '\n', lines[i])
                if lines[i].strip():
                    new_lines.append(lines[i])
            text = ''.join(new_lines)
        with open(path + file, 'w', encoding='utf-8') as outfile:
            outfile.write(text)


