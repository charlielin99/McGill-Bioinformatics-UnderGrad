import pandas as pd
import json
import math
import gzip
import operator # sort dictionary in bonus

# !/Users/yueli/anaconda3/bin/python
# q1 reading ICD-9 definitions
def process_icd9_file(filename):
    """
    args:
        filename: Name of file containing ICD-9 definition
    returns:
        dictionary of dictionaries
        level 1 dictionary: icd9 group name as key
        level 2 dictionary: icd9 code as key and icd9 names as values
    """
    icd9_encyclopedia = {}
    code_name = {}

    filename = "icd9_info.txt"
    f = open(filename, 'r') # open file to read

    # YOUR CODE HERE
    
    # read file one line at a time and split contents of line into a list of str
    for line in f:
        values_list = line.split()
        
        # assign group names as keys
        if line[1].isalpha():
            group_name = line.strip("\n")
            icd9_encyclopedia[group_name] = {}
        # assign codes and disease names as values 
        else:
            icd9_encyclopedia[group_name][values_list[0]] = " ".join(values_list[1:len(values_list)])

    f.close()

    return icd9_encyclopedia


icd9_encyclopedia = process_icd9_file("icd9_info.txt")

outfile = "icd9_encyclopedia.json" # file contains correctly processed dict
f = open(outfile, "r")
icd9_encyclopedia_correct = json.load(f)
f.close()

# check
count = 0
print("\n\n**** output from q1 ****")
for k, x in icd9_encyclopedia.items():
    print('group name', k, sep='\t')
    for k1, x1 in x.items():
        print(k1, x1, sep='\t')
        count += 1
    if count > 10:
        break


# q2 process patient data to read in 1000 patients
def process_patient_data(filename, max_patients=5000):
    """
    args:
        filename: "DIAGNOSES_ICD.csv.gz"
        max_patients: optional argument for maximum number of patients to store
        in the dictionary
    returns:
        a dictionary with patient ID as key and a set of ICD-9 code as values
        NOTE: the ICD-9 code from DIAGNOSES_ICD.csv.gz is not directly compatible
        with the ICD9_encyclopedia from function process_icd9_file()
        This function will parse the ICD-9 code as follows.
        If the ICD-9 code is numeric or starts with "V", the first 3 characters
        of each ICD-9 code is stored as the values in the ICD-9 list; 
        If the ICD-9 code starts with "E", the first 4 characters of the ICD-9
        code is stored as the values in the ICD-9 list
    """

    patient_data = pd.read_csv(filename, compression="gzip")
    patient_data = patient_data.sort_values(by=["SUBJECT_ID"])
    patient_records = {} # save patient icd9_code into dict

    # YOUR CODE HERE

    curr_number_of_patient = 0 # initialize counter

    # access row by row and access columns subject_id and icd9_code
    for index, row in patient_data.iterrows():
        patId = row["SUBJECT_ID"]
        icd9_code = row["ICD9_CODE"]
        
        # create set of unique diseases and update counter
        if patId not in patient_records:
            patient_records[patId] = set([])
            curr_number_of_patient += 1

        # check if we reached maximum number of patient to load
        if curr_number_of_patient == max_patients:
            break

        # update dict subject id keys with formatted codes as values
        icd9_string = str(icd9_code)
        if icd9_string[0] == "E":
            icd9_string = icd9_string[0:4]
        else:
            icd9_string = icd9_string[0:3]

        patient_records[patId].add(icd9_string)

    return patient_records

patient_records = process_patient_data("DIAGNOSES_ICD.csv.gz")

# check
count = 0
print("\n\n**** output from q2 ****")
for k, x in patient_records.items():
    print(k, x, sep='\t')
    count += 1
    if count > 10:
        break

# check your patient_records with the correct one
filein = "patient_records.json"  # change var to outfile
f = open(outfile, "r")
patient_records_correct = json.load(f)
for k, x in patient_records.items():
    patient_records_correct[k] = set(x)
f.close()


# q3
def average_patient_icd9code(patient_records):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.csv.gz")
    returns:
        average number of patient observed per ICD-9 code
    """

    # YOUR CODE HERE
    
    unique_icd9 = set([])
    icd9_count = {}
    icd9sum = 0 # initialize code counter

    # create set with only unqiue codes
    for subjectID, icd9_set in patient_records.items():
        for code in icd9_set:
            unique_icd9.add(code)

    # initialize codes with 0 counts
    for icd9_code in unique_icd9:
        icd9_count[icd9_code] = 0

    # update code counter when seen
    for subjectID, icd9_set in patient_records.items():
        for code in icd9_set:
            icd9_count[code] += 1

    # calculate average using code counters and number of codes
    for key, value in icd9_count.items():
        icd9sum += (value / (len(icd9_count.keys())))

    return icd9sum # 57.21

print("\n\n**** output from q3 ****")
print(f"Average patient count {average_patient_icd9code(patient_records):.2f}")  # 57.53


# q4 group patient icd9 code by icd9 categories
def process_icd9_encyclopedia(icd9_encyclopedia):
    """
    args:
        icd9_encyclopedia obtained from process_icd9_info("icd9_info.txt")
    returns:
        icd9_encyclopedia_reverseIndex: dictionary with key as icd-9 code and value
        as the corresponding disease group names
    """

    icd9_encyclopedia_reverseIndex = {}
    
    # YOUR CODE HERE

    # reversing key value pairs for q1 dict
    for group_name, dict_codename in icd9_encyclopedia.items():
        for code in dict_codename.keys():
            icd9_encyclopedia_reverseIndex[code] = group_name

    return icd9_encyclopedia_reverseIndex

# check
# print("\n\n**** output from q4 ****")
icd9_encyclopedia_reverseIndex = process_icd9_encyclopedia(icd9_encyclopedia)


def summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex):
    """
    args:
        patient_records obtained from process_patient_data("DIAGNOSES_ICD.csv.gz")
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_records_summary: a dictionary with patient ID as key and a set of 
        disease group names as value
    """

    patient_records_summary = {}
    
    # YOUR CODE HERE

    # loop through patient and icd9 code q2 dict
    for pat_id, codes in patient_records.items():
        descriptions = set([])

        # replace icd9 code with description
        for code in codes:
            if code in icd9_encyclopedia_reverseIndex:
                descriptions.add(icd9_encyclopedia_reverseIndex[code])

        patient_records_summary[pat_id] = descriptions

    return patient_records_summary

patient_records_summary = summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)

# check
print("\n\n**** output from q4 ****")
for patId, summary in patient_records_summary.items():
    if patId in [34, 35]:
        print(patId, summary)


# q5 find similar patients
def getKey1(item):
    return item[1]

def get_patients_similarity(query_patient_records, patient_records_summary, icd9_encyclopedia_reverseIndex):
    """
    args:
        query_patient_records: same compound type as patient_records but for a test set of patients
        patient_records_summary: dictionary obtained from 
        summarize_patient_records(patient_records, icd9_encyclopedia_reverseIndex)
        icd9_encyclopedia_reverseIndex from process_icd9_encyclopedia(icd9_encyclopedia)
    returns:
        patient_similarity: a dictionary with key as test patient ID and value as a list of 2-value tuples
        The first value in the tuple is the neighbor patient ID and the second value in the tuple is the 
        similarity score between the neighbor patient and the test patient
        NOTE: the list must *not* contain the query patient ID and the similarity with the query patient themselves
    """

    # get list for query patients
    query_patient_records_summary = summarize_patient_records(query_patient_records, icd9_encyclopedia_reverseIndex)

    patient_similarity = {}
    
    # YOUR CODE HERE

    # loop through query patients
    for pat_id in query_patient_records:
        pat_records_summary = query_patient_records_summary[pat_id]

        data = []

        # find total per each patient except repeats
        for other_pat_id, other_pat_records in patient_records_summary.items():
            if pat_id != other_pat_id:  # not checking for same ID
                in_both_sets = len(list(pat_records_summary & other_pat_records))
                in_query_set = len(pat_records_summary) - in_both_sets
                in_other_set = len(other_pat_records) - in_both_sets

                total = in_both_sets - in_query_set - in_other_set

                data.append((str(other_pat_id), total))

        # sort set by total
        data.sort(key=getKey1, reverse=True)

        # add to dict
        patient_similarity[pat_id] = data

    return patient_similarity

icd9group_examples = [[295], [332], [491]]  # schizo, parkinson, copd
example_disorders_all = set([])
for i in icd9group_examples:
    for j in i:
        example_disorders_all.add(str(j))

query_patient_records = {}
for i in icd9group_examples:
    example_disorders = set([])
    for j in i:
        example_disorders.add(str(j))
    for patId, icd9list in patient_records.items():
        if len(icd9list & example_disorders) > 0 and \
           len(icd9list & (example_disorders_all - example_disorders)) == 0:
            query_patient_records[patId] = icd9list
            break

print(query_patient_records.keys()) # dict_keys(['71', '85', '394', '124'])

patient_similarity = get_patients_similarity(query_patient_records,
                                             patient_records_summary,
                                             icd9_encyclopedia_reverseIndex)

print("\n\n**** output from q5 ****")
for k, x in patient_similarity.items():
    print(k, x[0:5])

#71 [('2247', 1), ('1438', 0), ('2183', 0), ('4596', 0), ('750', -1)]
#85 [('5166', 0), ('2061', -1), ('5107', -1), ('4577', -2), ('4676', -2)]
#111 [('4453', 9), ('1598', 6), ('3122', 6), ('5077', 6), ('1038', 5)]


# q6 make diagnosis based on icd9 codes from top k most similar patient
def make_diagnosis(query_patient_records, patient_records_summary,
                   patient_records, top_k=20):
    """
    args:
        query_patient_records: same compound type as patient_records but for a test set of patients
        patient_records_summary: obtained from summarize_patient_records(patient_records)
        patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        top_k: integer value specifiy the number of most closely matched patients to each query patient (default: 20)
    returns:
        query_patient_diagnosis: a dictionary with key as the query patient ID and value as the 
        sorted list of tuples. The first value in the tuple is the icd-9 code and the second value in the 
        tuple is the frequency of icd-9 observed among the top_k matched patient. The list is sorted in _decreasing_ 
        order by the frequency of the ICD-9 code
    """

    # get patient similarity
    patient_similarity = get_patients_similarity(query_patient_records, patient_records_summary, icd9_encyclopedia_reverseIndex)

    query_patient_diagnosis = {}
    
    # YOUR CODE HERE

    # for each patient go through top_k similar patients and create dict
    for pat_id in patient_similarity.keys():
        pat_icd9_codes = query_patient_records[pat_id]

        icd9_pat_id_frequency = {}
        for i in range(top_k):
            other_pat_id = patient_similarity[pat_id][i][0]
            other_pat_icd9_codes = patient_records[int(other_pat_id)]

            # loop through other patient codes and check if query patient has it
            for code in other_pat_icd9_codes:
                # if patient already diagnosed with disease prediction not needed
                if code not in pat_icd9_codes:
                    # initializing and updating counters
                    if code not in icd9_pat_id_frequency:
                        icd9_pat_id_frequency[code] = 0
                    icd9_pat_id_frequency[code] += 1

        # create set of tuples and sort it
        data = []

        for k, v in icd9_pat_id_frequency.items():
            data.append((k, v / top_k))

        data.sort(key=getKey1, reverse=True)

        # add set to dictionary for query patient
        query_patient_diagnosis[pat_id] = data

    return query_patient_diagnosis

query_patient_diagnosis = make_diagnosis(query_patient_records, patient_records_summary, patient_records)

# check
def getCode_icd9code_Info(icd9_encyclopedia):
    icd9_info = {}

    for k, x in icd9_encyclopedia.items():
        for icd9_code, icd9_names in x.items():
            icd9_info[icd9_code] = {'group': k, 'code': icd9_code, 'name': icd9_names}
    return icd9_info


def write_diagnosis_report(query_patient_diagnosis, query_patient_records, icd9_info, outfile):
    
    f = open(outfile, 'w')

    f.write("patId\tsymptoms_status\ticd9 group\tICD9 code\tICD9 name\tFrequency\n")

    for patId, diagnosis in query_patient_diagnosis.items():

        for icd9 in query_patient_records[patId]:
            x = icd9_info[icd9]
            f.write(f"{patId}\tobserved\t{x['code']}\t{x['name']}\t1\n")

        for icd9_tuple in diagnosis:
            icd9_code = icd9_tuple[0]
            icd9_freq = icd9_tuple[1]
            if icd9_freq > 0.2:
                icd9_code_info = icd9_info[icd9_code]
                f.write(f"{patId}\tpredicted\t{icd9_code}\t{icd9_code_info['name']}\t{icd9_freq}\n")
    f.close()

print("\n\n**** output from q6 ****")
icd9_info = getCode_icd9code_Info(icd9_encyclopedia)
outfile = "diagnosis_report.txt"
write_diagnosis_report(query_patient_diagnosis, query_patient_records, icd9_info, outfile)
filein = open(outfile, 'r')
for i in range(10):
    line = filein.readline()
    print(line.rstrip())
    

# q7 evaluate diagnostic predictions to choose the best overall k
all_patient_records = process_patient_data("DIAGNOSES_ICD.csv.gz", max_patients=5000)

train_patient_records = {}
test_patient_records = {}

n_train = 2500

for patId in all_patient_records.keys():
    if len(train_patient_records.keys()) < n_train:
        train_patient_records[patId] = all_patient_records[patId]
    else:
        test_patient_records[patId] = all_patient_records[patId]

def icd9_prediction(target_icd9, test_patient_records, train_patient_records, icd9_encyclopedia_reverseIndex, top_k=5):
    """
    args:
        target_icd9: icd9 code that we will be predicting from a subset of the test_patient_records
        test_patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        train_patient_records: obtained from process_patient_data("DIAGNOSTIC_CODE.csv.gz")
        icd9_encyclopedia_reverseIndex: obtained from process_icd9_encyclopedia(icd9_encyclopedia)
        top_k: integer value specifies the number of most closely matched patients to each query patient (default: 20)
    returns:
        accuracy: a numeric value as the correct predictions divided by the total correct plus incorrect predictions
    """

    train_patient_records_summary = summarize_patient_records(train_patient_records, icd9_encyclopedia_reverseIndex)

    test_patient_records_new = {}

    for patId, icd9code in test_patient_records.items():
        if target_icd9 in icd9code:
            test_patient_records_new[patId] = icd9code - {target_icd9}

    test_patient_records_controls = {}

    for patId, icd9code in test_patient_records.items():
        if target_icd9 not in icd9code:
            test_patient_records_controls[patId] = icd9code
        if len(test_patient_records_controls) == len(test_patient_records_new):
            break

    test_patient_records_new.update(test_patient_records_controls)

    test_patient_diagnosis = make_diagnosis(test_patient_records_new, train_patient_records_summary, train_patient_records, top_k)

    correct = 0 # update if predicted
    incorrect = 0 # update if not predicted
    
    # YOUR CODE HERE
    
    # loop through all test patients summaries
    for pat_ID in test_patient_records_new.keys():
        # check patient target code before removal
        if target_icd9 in test_patient_records[pat_ID]:  
            prediction = False # initialize boolean
            # check if target code is predicted for patient
            for icd9Code, frequency in test_patient_diagnosis[pat_ID]:  
                if icd9Code == target_icd9:
                    if frequency > (1/top_k):
                        correct += 1
                    prediction = True # update boolean
                    break # exit nested for loop and restart
            # updates only if nested for loop not entered
            if prediction is False:
                incorrect += 1
        else:
            prediction = False
            # loop through patients originally without target code and check prediction
            for icd9Code, frequency in test_patient_diagnosis[pat_ID]:  
                if icd9Code == target_icd9:
                    if frequency > (1/top_k):
                        incorrect += 1  
                    prediction = True 
                    break
            if prediction is False:
                correct += 1            
    
    # using provided formula
    accuracy = correct/(correct+incorrect)

    return accuracy

# test
accuracies = {}
icd9_target_list = ['295', '332', '491']

for target_icd9 in icd9_target_list:
    accuracies[target_icd9] = icd9_prediction(target_icd9, 
              test_patient_records, train_patient_records, 
              icd9_encyclopedia_reverseIndex, top_k = 20)

print("\n\n**** output from q7 ****")
for icd9, accuracy in accuracies.items():
    print(f"{icd9}: {100 * accuracy:.0f}%")


# Bonus: choose best k
topk_list = [1, 5, 10, 20, 50, 100, 200, 300, 400, 500]
icd9_target_list = ['295', '332', '491']

# YOUR CODE HERE

k_value_dict = {} # empty dict to store k-value:avg accuracy key value pairs

# loop through possible k in list above
for k in topk_list:  
    accuracy_list = [] # store accuracy scores as decimals
    # check all target_icd9 codes for each k and find accuracy for each target_icd9
    for target_icd9 in icd9_target_list: 
        accuracy = icd9_prediction(target_icd9, test_patient_records, train_patient_records, icd9_encyclopedia_reverseIndex, k)  
        accuracy_list.append(accuracy)
    accuracy_sum = 0
    for dec in accuracy_list:
        accuracy_sum += dec
    # calculate average accuracy for respective k value
    avg_accuracy = accuracy_sum/len(accuracy_list)
    k_value_dict[k] = avg_accuracy

# create and sort list with items from k dict
output_list = []
for k, acc_rate in k_value_dict.items():
    output_list.append((k, acc_rate))
output_list.sort(key=operator.itemgetter(1), reverse=True)

# print as shown in output txt file
print("\n\n**** output from bonus ****")
print("K is sorted by accuracy:")
for k, acc_rate in output_list:
    print(f"{k}: {100*acc_rate:.0f}%")