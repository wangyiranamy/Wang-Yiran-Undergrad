
# coding: utf-8


import pickle
import math
import sys
import re
from copy import copy
from collections import defaultdict
from optparse import OptionParser

directory = '' # Put your folder directory with all the
               # unzipped files here , Ex:'/Machine Learning/Project/'

language_list = ['CN','EN','ES','SG']
train = {}
dev_in = {}
dev_out = {}
dev_p2_out = {}
dev_p3_out = {}
dev_p4_out = {}
dev_p5_out = {}


label_list = ['START','O','B-positive','B-negative','B-neutral',
              'I-positive','I-negative','I-neutral','STOP']
reduced_label_list = ['O','B-positive','B-negative','B-neutral',
              'I-positive','I-negative','I-neutral']


outputColumnIndex = 1
separator = ' '

    
#Read entities from predcition
def get_predicted(predicted, answers=defaultdict(lambda: defaultdict(defaultdict))):

    example = 0
    word_index = 0
    entity = []
    last_ne = "O"
    last_sent = ""
    last_entity = []

    answers[example] = []
    for line in predicted:
        line = line.strip()
        if line.startswith("##"):
            continue
        elif len(line) == 0:
            if entity:
                answers[example].append(list(entity))
                entity = []
            example += 1
            answers[example] = []
            word_index = 0
            last_ne = "O"
            continue
        else:
            split_line = line.split(separator)
            #word = split_line[0]
            value = split_line[outputColumnIndex]
            ne = value[0]
            sent = value[2:]
            last_entity = []

            #check if it is start of entity
            if ne == 'B' or (ne == 'I' and last_ne == 'O') or (last_ne != 'O' and ne == 'I' and last_sent != sent):
                if entity:
                    last_entity = list(entity)
                entity = [sent]
                entity.append(word_index)
            elif ne == 'I':
                entity.append(word_index)
            elif ne == 'O':
                if last_ne == 'B' or last_ne == 'I':
                    last_entity =list(entity)
                entity = []

            if last_entity:
                answers[example].append(list(last_entity))
                last_entity = []

        last_sent = sent
        last_ne = ne
        word_index += 1
    if entity:
        answers[example].append(list(entity))
    return answers



#Read entities from gold data
def get_observed(observed):

    example = 0
    word_index = 0
    entity = []
    last_ne = "O"
    last_sent = ""
    last_entity = []

    observations=defaultdict(defaultdict)
    observations[example] = []

    for line in observed:
        line = line.strip()
        if line.startswith("##"):
            continue
        elif len(line) == 0:
            if entity:
                observations[example].append(list(entity))
                entity = []

            example += 1
            observations[example] = []
            word_index = 0
            last_ne = "O"
            continue

        else:
            split_line = line.split(separator)
            word = split_line[0]
            value = split_line[outputColumnIndex]
            ne = value[0]
            sent = value[2:]


            last_entity = []

            #check if it is start of entity, suppose there is no weird case in gold data
            if ne == 'B' or (ne == 'I' and last_ne == 'O') or (last_ne != 'O' and ne == 'I' and last_sent != sent):
                if entity:
                    last_entity = entity
                entity = [sent]
                entity.append(word_index)

            elif ne == 'I':
                entity.append(word_index)

            elif ne == 'O':
                if last_ne == 'B' or last_ne == 'I':
                    last_entity = entity
                entity = []

            if last_entity:
                observations[example].append(list(last_entity))
                last_entity = []

        last_ne = ne
        last_sent = sent
        word_index += 1

    if entity:
        observations[example].append(list(entity))

    return observations

#Print Results and deal with division by 0
def printResult(evalTarget, num_correct, prec, rec):
    if abs(prec + rec ) < 1e-6:
        f = 0
    else:
        f = 2 * prec * rec / (prec + rec)
    print('#Correct', evalTarget, ':', num_correct)
    print(evalTarget, ' precision: %.4f' % (prec))
    print(evalTarget, ' recall: %.4f' %   (rec))
    print(evalTarget, ' F: %.4f' % (f))

#Compare results bewteen gold data and prediction data
def compare_observed_to_predicted(observed, predicted):

    correct_sentiment = 0
    correct_entity = 0

    total_observed = 0.0
    total_predicted = 0.0

    #For each Instance Index example (example = 0,1,2,3.....)
    for example in observed:
        observed_instance = observed[example]
        predicted_instance = predicted[example]

        #Count number of entities in gold data
        total_observed += len(observed_instance)
        #Count number of entities in prediction data
        total_predicted += len(predicted_instance)

        #For each entity in prediction
        for span in predicted_instance:
            span_begin = span[1]
            span_length = len(span) - 1
            span_ne = (span_begin, span_length)
            span_sent = span[0]

            #For each entity in gold data
            for observed_span in observed_instance:
                begin = observed_span[1]
                length = len(observed_span) - 1
                ne = (begin, length)
                sent = observed_span[0]

                #Entity matched
                if span_ne == ne:
                    correct_entity += 1
                    

                    #Entity & Sentiment both are matched
                    if span_sent == sent:
                        correct_sentiment += 1

    print()
    print('#Entity in gold data: %d' % (total_observed))
    print('#Entity in prediction: %d' % (total_predicted))
    print()

    prec = correct_entity/total_predicted
    rec = correct_entity/total_observed
    printResult('Entity', correct_entity, prec, rec)
    print()

    prec = correct_sentiment/total_predicted
    rec = correct_sentiment/total_observed
    printResult('Sentiment',correct_sentiment, prec, rec)


def compare(file_gold,file_predict):

    gold = open(file_gold, "r", encoding='UTF-8')
    prediction = open(file_predict, "r", encoding='UTF-8')

    #column separator
    separator = ' '

    #the column index for tags
    
    #Read Gold data
    observed = get_observed(gold)

    #Read Predction data
    predicted = get_predicted(prediction)

    #Compare
    compare_observed_to_predicted(observed, predicted)


def train_model(f_train):
    
    f = open(f_train,'r', encoding='UTF-8')
    label_dict = dict.fromkeys(label_list,0)
    transition_dict = dict.fromkeys(label_list[0:-1],{})

    for i in label_list[0:-1]:
        transition_dict[i] = dict.fromkeys(label_list[1:],0)

    emission_dict = dict()
    prev_line = ['','']
    newLine = True
    
    for lines in f:
        
        line = str.split(lines)
        if len(line) == 0:
            if not newLine:
                transition_dict[prev_line[1]]['STOP'] += 1
                newLine = True

            
        if len(line) == 2:
            
            label_dict[line[1]] += 1
            if newLine:
                label_dict['START'] += 1
                label_dict['STOP'] += 1
                transition_dict['START'][line[1]] += 1
                newLine = False
            else:
                transition_dict[prev_line[1]][line[1]] += 1
                
            if line[0] not in emission_dict:
                emission_dict[line[0]] = {line[1]:1}
            elif line[1] not in emission_dict[line[0]]:
                emission_dict[line[0]][line[1]] = 1
            else:
                emission_dict[line[0]][line[1]] += 1  
            prev_line = line

    f.close()
    return [transition_dict,emission_dict,label_dict]


def predict_emission_model(f_train,f_devin,f_prediction):
    
    
    # data[0] = Transition_dictinoary
    # data[1] = Emission_dictionary
    # data[2] = Label_dictionary
    
    data = train_model(f_train)
    emission_dict = data[1]
    output = ''
    
    f_in = open(f_devin,'r', encoding='UTF-8')
    f_in_words = []
    for lines in f_in:
        line = str.split(lines)
        if len(line) != 0 and line[0] not in f_in_words:
            f_in_words.append(line[0])
    f_in.close()
    
    for train_word in emission_dict:
        if train_word in f_in_words:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / (data[2][label]+1)
        else:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / data[2][label]
                
    for word in f_in_words:
        if word not in emission_dict:
            emission_dict[word] = {}
            for label in data[2]:
                emission_dict[word][label] = 1.0 / (data[2][label] + 1)
    
    f_in = open(f_devin,'r', encoding='UTF-8')
    for lines in f_in:
        line = str.split(lines)
        if len(line) == 0:
            output += '\n'
        else:
            y_star = 'O'
            y_score = 0
            for label in emission_dict[line[0]]:
                next_y_score = emission_dict[line[0]][label]
                if next_y_score > y_score:
                    y_star = label
                    y_socre = next_y_score
            output+=str(line[0] + ' ' + y_star + '\n')

    f_in.close()
    
    f_out = open(f_prediction,'wb')
    f_out.write(output.encode('utf-8'))
    f_out.close()

    
def predict_transition_and_emission_model(f_train,f_devin,f_prediction):
    
    data = train_model(f_train)
    transition_dict = data[0]
    emission_dict = data[1]
    sentence_list = [[]]
    sentence_list_index = 0
    output = ''
    f_in_words = []
    
    f_in = open(f_devin,'r',encoding='UTF-8')
    for lines in f_in:
        line = str.split(lines)
        if len(line) == 0:
            sentence_list.append([])
            sentence_list_index += 1
        elif len(line) != 0:
            sentence_list[sentence_list_index].append(line[0])
        if len(line) != 0 and line[0] not in f_in_words:
            f_in_words.append(line[0])
    f_in.close()
    
    for prev_label in transition_dict:
        for label in transition_dict[prev_label]:
            if transition_dict[prev_label][label] == 0:
                transition_dict[prev_label][label] = 1.0 / (data[2][prev_label] + 1)
            else:
                transition_dict[prev_label][label] = transition_dict[prev_label][label] * 1.0 / data[2][prev_label]
                
    for train_word in emission_dict:
        if train_word in f_in_words:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / (data[2][label]+1)
        else:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / data[2][label]


    for word in f_in_words:
        if word not in emission_dict:
            emission_dict[word] = {}
            for label in reduced_label_list:
                emission_dict[word][label] = 1.0 / (data[2][label] + 1)

    for sentence in sentence_list:
        n = len(sentence)
        path_dict = {0: {'START': {"pi": 1.0, "previous": ''}}}
        for k in range(n):
            path_dict[k + 1] = {}
        for k in path_dict:
            if k == 0:
                continue
            for label in reduced_label_list:
                path_dict[k][label] = {}

        path_dict[n+1] = {'STOP': {}}

        for k in path_dict:
            if k == 0:
                continue
            if k == n + 1:
                best_pi = 0
                best_prev_label = ''
                for prev_label in path_dict[k - 1]:
                    pi = path_dict[k - 1][prev_label]["pi"] * transition_dict[prev_label]["STOP"]
                    if pi > best_pi:
                        best_pi = pi
                        best_prev_label = prev_label
                path_dict[k]['STOP'] = {"pi": best_pi, "previous": best_prev_label}
                continue
            for label in path_dict[k]:
                best_pi = 0
                best_prev_label = ''
                for prev_label in path_dict[k-1]:
                    if label in emission_dict[sentence[k-1]] : #or path_dict[k-1][prev_label]["pi"]!= 0:
                        pi = path_dict[k-1][prev_label]["pi"] * transition_dict[prev_label][label] *                            emission_dict[sentence[k-1]][label]
                    else:
                        pi = path_dict[k-1][prev_label]["pi"] * transition_dict[prev_label][label] / 100000
                    if pi > best_pi:
                        best_pi = pi
                        best_prev_label = prev_label
                path_dict[k][label] = {"pi": best_pi, "previous": best_prev_label}
        label = n
        path_reverse = ["STOP"]
        while label >= 0:
            path_reverse.append(path_dict[label + 1][path_reverse[len(path_reverse) - 1]]['previous'])
            label -= 1
        
        sentence_label = path_reverse[::-1][1:len(path_reverse) - 1]
        
        for i in range(len(sentence_label)):
            output += str(sentence[i] + ' ' + sentence_label[i]+'\n')
        output += '\n'
    f_out = open(f_prediction,'wb')
    f_out.write(output.encode("utf-8"))
    f_out.close()

    

def rank(kdict, probablity, prev_label, at_k):

    for i in range(len(kdict.keys())):
        if probablity > kdict[i]["pi"]:
            for j in range(len(kdict.keys()) - 1, i, -1):                    
                kdict[j] = kdict[j - 1]
            kdict[i] = {"pi": probablity,
                        "prev_label": prev_label,
                        "num": at_k}
            break
    return kdict


def predict_top_k_viterbi(top_K,f_train,f_devin,f_prediction):
    
    
    data = train_model(f_train)
    transition_dict = data[0]
    emission_dict = data[1]
    sentence_list = [[]]
    sentence_list_index = 0
    f_in_words = []
    output = ''
    f_in = open(f_devin,'r',encoding='UTF-8')
    
    
    for lines in f_in:
        line = str.split(lines)
        if len(line) == 0:
            sentence_list.append([])
            sentence_list_index += 1
        elif len(line) != 0:
            sentence_list[sentence_list_index].append(line[0])
        if len(line) != 0 and line[0] not in f_in_words:
            f_in_words.append(line[0])
    f_in.close()
    
    for prev_label in transition_dict:
        for label in transition_dict[prev_label]:
            if transition_dict[prev_label][label] == 0:
                transition_dict[prev_label][label] = 1.0 / (data[2][prev_label] + 1)
            else:
                transition_dict[prev_label][label] = transition_dict[prev_label][label] * 1.0 / data[2][prev_label]
                
    for train_word in emission_dict:
        if train_word in f_in_words:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / (data[2][label]+1)
        else:
            for label in emission_dict[train_word]:
                emission_dict[train_word][label] = emission_dict[train_word][label] * 1.0 / data[2][label]


    for word in f_in_words:
        if word not in emission_dict:
            emission_dict[word] = {}
            for label in reduced_label_list:
                emission_dict[word][label] = 1.0 / (data[2][label] + 1)

    for sentence in sentence_list:
        n = len(sentence)
        
        path_dict = {0: {'START': {}}}
        
        for i in range(top_K):
            path_dict[0]['START'][i] = {'pi': -sys.maxsize - 1, 'prev_label': '', "from_k_th": -1}
        path_dict[0]['START'] = rank(path_dict[0]['START'], 1.0, '', -1)
        
        for k in range(n):
            path_dict[k + 1] = {}
        for k in path_dict:
            if k == 0:
                continue
            for label in reduced_label_list:
                path_dict[k][label] = {}
                for i in range(top_K):
                    path_dict[k][label][i] = {'pi': -sys.maxsize - 1,'prev_label': '', 'from_k_th': -1}

        path_dict[n+1] = {"STOP": {}}
        
        for i in range(top_K):
            path_dict[n+1]['STOP'][i] = {'pi': -sys.maxsize - 1,'prev_label': '', 'from_k_th': -1}

        for k in path_dict:
            if k == 0:
                continue
            if k == n + 1:
                for prev_label in path_dict[k - 1]:
                    for k_th in range(top_K):
                        pi = path_dict[k - 1][prev_label][top_K-1]['pi'] * transition_dict[prev_label]['STOP']
                    path_dict[k]['STOP'] = rank(path_dict[k]['STOP'], pi, prev_label, k_th)
                continue
            for label in path_dict[k]:
                for prev_label in path_dict[k-1]:
                    for k_th in range(top_K):
                        if label in emission_dict[sentence[k-1]] : #or path_dict[k-1][prev_label]["pi"]!= 0:
                            pi = path_dict[k-1][prev_label][top_K-1]['pi'] * transition_dict[prev_label][label] *                                emission_dict[sentence[k-1]][label]
                        else:
                            pi = path_dict[k-1][prev_label][top_K-1]['pi'] * transition_dict[prev_label][label] / 100000
                        path_dict[k][label] = rank(path_dict[k][label],pi,prev_label,k_th)
                        
        label = n
        from_k_th = top_K - 1
        path_reverse = ['STOP']
        while label >= 0:
            while path_dict[label + 1][path_reverse[len(path_reverse) - 1]][from_k_th]['prev_label']== '':
                from_k_th-=1
            path_reverse.append(path_dict[label + 1][path_reverse[len(path_reverse) - 1]][from_k_th]['prev_label'])
            from_k_th = path_dict[label + 1][path_reverse[len(path_reverse)-2]][from_k_th]['num']
            label -= 1

        sentence_label = path_reverse[::-1][1:len(path_reverse) - 1]
        for i in range(len(sentence_label)):
            output += str(sentence[i] + ' ' + sentence_label[i]+'\n')
        output +='\n'
    
    f_out = open(f_prediction,'wb')
    f_out.write(output.encode("utf-8"))
    f_out.close()




def initialize_transition(states):
    transition = {}
    for previous_state in states[:-1]:
        transition[previous_state]={}
        if previous_state=="START":
            for current_state in states[1:]:
                transition[previous_state][current_state]=0
        else:
            for current_state in states[1:]:
                transition[previous_state][current_state]=0
    return transition
        
def initialize_emission(trgfile):
    emission = {}
    states =  ["B-negative", "B-neutral", "B-positive", "O", "I-negative", 'I-neutral', "I-positive"]
    for i in trgfile:
        i = i.replace("\n", "")
        xy_pair = i.split(" ")
        if len(xy_pair) == 2:
            if str(xy_pair[0]) not in emission.keys():
                emission[str(xy_pair[0])]={}
                for state in states:
                    emission[str(xy_pair[0])][state] = 0
            else:
                emission[str(xy_pair[0])][xy_pair[1]] = 0    
    return emission  


def perceptron_viterbi(observed_sequence, a_dict, b_dict):
    states = ["START", "B-negative", "B-neutral", "B-positive", "O", "I-negative", "I-neutral", "I-positive", "STOP"]
    pure_state = states[1:- 1]
    n = len(observed_sequence)
    path_dict = {0: {"START": {"p": 1.0, "previous": "NA"}}}
    for i in range(n):
        path_dict[i + 1] = {}
    for layer in path_dict:
        if layer == 0: continue
        for state in pure_state:
            path_dict[layer][state] = {}
    path_dict[n + 1] = {"STOP": {}}
    for layer in path_dict:
        if layer == 0: continue

        if layer == n + 1:
            max_p = 0
            max_previous_state = "NA"
            for previous_state in path_dict[layer - 1]:
                p = path_dict[layer - 1][previous_state]["p"] + a_dict[previous_state]["STOP"]
                if p > max_p:
                    max_p = p
                    max_previous_state = previous_state
            path_dict[layer]["STOP"] = {"p": max_p, "previous": max_previous_state}
            continue

        for current_state in path_dict[layer]:
            max_p = 0
            max_previous_state = "NA"
            for previous_state in path_dict[layer - 1]:
                if observed_sequence[layer-1] not in b_dict.keys():
                    b_dict[observed_sequence[layer-1]] = {}
                if current_state in b_dict[observed_sequence[layer - 1]]:
                    p = path_dict[layer - 1][previous_state]["p"] +                         a_dict[previous_state][current_state] +                         b_dict[observed_sequence[layer - 1]][current_state]
                else:
                    p = path_dict[layer - 1][previous_state]["p"] +                         a_dict[previous_state][current_state]
                if p > max_p:
                    max_p = p
                    max_previous_state = previous_state
            path_dict[layer][current_state] = {"p": max_p, "previous": max_previous_state}

    current_layer = n
    path_reverse = ["STOP"]
    while current_layer >= 0:
        prev = path_dict[current_layer + 1][path_reverse[-1]]['previous']
        if prev=='NA':
            prev = 'O'
        path_reverse.append(prev)
        current_layer -= 1
    return path_reverse[::-1][1:len(path_reverse) - 1]

def get_sequences(train):
    sequences = [[[],[]]]
    index = 0
    for input in train:
        if input == "\n":
            sequences.append([[],[]])
            index += 1
        else:
            input = input.replace("\n", "")
            input = input.split(" ")
            sequences[index][0].append(input[0])
            sequences[index][1].append(input[1])
    return sequences

def perceptron_train(train, n):
    states = ["START", "B-negative", "B-neutral", "B-positive", "O", "I-negative", 'I-neutral', "I-positive", 'STOP']
    transition = initialize_transition(states)
    emission = initialize_emission(train)

    for i in range(n):
        sequences = get_sequences(train)
        for seq in sequences:
            pred = perceptron_viterbi(seq[0],transition,emission)
            # Tune transition params
            for index in range(len(seq[0])-1):
                transition[pred[index]][pred[index+1]] -= 1
                transition[seq[1][index]][seq[1][index+1]] += 1
            # Tune emission params
            for index in range(len(seq[0])):
                emission[seq[0][index]][pred[index]] -= 1
                emission[seq[0][index]][seq[1][index]] += 1
    return transition,emission


def predict_perceptron_viterbi(loops,f_train,f_devin,f_prediction):
    
    train = open(f_train,'r',encoding='UTF-8').readlines()
    transition_dict,emission_dict = perceptron_train(train, loops)
    
    sentence_list = [[]]
    sentence_list_index = 0
    output = ''
    f_in_words = []
    
    f_in = open(f_devin,'r',encoding='UTF-8')
    for lines in f_in:
        line = str.split(lines)
        if len(line) == 0:
            sentence_list.append([])
            sentence_list_index += 1
        elif len(line) != 0:
            sentence_list[sentence_list_index].append(line[0])
        if len(line) != 0 and line[0] not in f_in_words:
            f_in_words.append(line[0])
    f_in.close()
    
    for sentence in sentence_list:
        sentence_label = perceptron_viterbi(sentence, transition_dict, emission_dict)
        
        for i in range(len(sentence_label)):
            output += str(sentence[i] + ' ' + sentence_label[i]+'\n')
        output += '\n'
    f_out = open(f_prediction,'wb')
    f_out.write(output.encode("utf-8"))
    f_out.close()

    





########### Main Function  ############
for language in language_list:
    
    top_K_value = 5 #  (for part 4 evaluation)
    loops = 10 # (for part 5 evaluation)
    
    train[language] = directory + language + '/train'
    dev_in[language] = directory + language + '/dev.in'
    dev_out[language] = directory + language + '/dev.out'
    dev_p2_out[language] = directory + language + '/dev.p2.out'
    dev_p3_out[language] = directory + language + '/dev.p3.out'
    dev_p4_out[language] = directory + language + '/dev.p4.out'
    dev_p5_out[language] = directory + language + '/dev.p5.out'
    
    predict_emission_model(train[language], dev_in[language],dev_p2_out[language])
    predict_transition_and_emission_model(train[language],dev_in[language],dev_p3_out[language])
    predict_top_k_viterbi(top_K_value,train[language],dev_in[language],dev_p4_out[language])     
    predict_perceptron_viterbi(loops,train[language],dev_in[language],dev_p5_out[language])     

    print ('Language : ' + language )
    print (language + ' Part 2 Score:')
    compare(dev_out[language],dev_p2_out[language])
    print()
    print (language + ' Part 3 Score:')
    compare(dev_out[language],dev_p3_out[language])
    print()
    print (language + ' Part 4 Score:')
    compare(dev_out[language],dev_p4_out[language])
    print()
    print (language + ' Part 5 Score:')
    compare(dev_out[language],dev_p5_out[language])
    print()
    print ('#########################')
    print()
    
test_EN = directory + '/test/EN/test.in'
test_ES = directory + '/test/ES/test.in'
test_EN_out = directory + '/test/EN/test.out'
test_ES_out = directory + '/test/ES/test.out'
train_EN = directory + '/EN/train'
train_ES = directory + '/ES/train'

predict_perceptron_viterbi(50,train_EN,test_EN,test_EN_out) 
predict_perceptron_viterbi(50,train_ES,test_ES,test_ES_out) 

