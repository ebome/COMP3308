# python MyClassifier.py training.txt testing.txt NB

#############################################################
# K-Nearest Neighbour
import sys
from Entry import Entry # each Entry is the instance (one row)
from myknn import KNN # KNN algorithm


file_training = open(sys.argv[1])

training_entries = []
testing_entries = []

# Training file has 9 attributes, including class yes/no
lines = file_training.readlines()
for i in lines:
    line = i.strip('\n')
    attributes = line.split(',')
    numeric_attributes = []
    for a in range(0, len(attributes)-1):
        numeric_attributes.append(attributes[a])
    result = attributes[-1]
    b = Entry(numeric_attributes, result)
    training_entries.append(b)
file_training.close()

# Testing file has 8 attributes, class is set as None
file_testing = open(sys.argv[2])
lines = file_testing.readlines()
for i in lines:
    line = i.strip('\n')
    attributes = line.split(',')
    numeric_attributes = []
    for a in range(0, len(attributes)):
        numeric_attributes.append(attributes[a])
    result = attributes[-1]
    b = Entry(numeric_attributes, None)
    testing_entries.append(b)
file_testing.close()

# From neighbouhood list [yes, no, no, yes, no], find the vote
def most_frequent(List):
    class_result = 'yes'
    yes_frequency = List.count('yes')
    no_frequency = List.count('no')
    if yes_frequency < no_frequency:
        class_result = 'no'
    return class_result

#############################################################
# Naive Bayes
import csv
import math  
#---------------------------------------------------------------
def prob_density(mean, std, x):
    std = float(std); mean = float(mean); x = float(x)
    #  set probabilities to 1 if standard deviation is 0
    if std==0:
        return 1
        
    base =  1/(std*math.sqrt(2*math.pi)) 
    exponent = ((-1)*(x-mean)**2)/(2*std**2)
    result = base*math.exp(exponent)
    return result

def naive_bayes(training_data, testing_data):   
    '''
    All the attributes are independent to each other. NB probability = f(x)
    '''
    num_of_attribute = len(training_data[0])
    #------------------------------------------------    
    # Get the probability of yes and no class in training set
    yes_count = 0
    for each_instance in training_data:
        if each_instance[-1] == 'yes':
            yes_count = yes_count + 1

    # 'no' is the total number in traing minus 'yes' in training
    num_of_instance = len(training_data)
    no_count = num_of_instance - yes_count

    p_yes = yes_count/num_of_instance # P(yes)
    p_no = no_count/num_of_instance # P(no)
    #------------------------------------------------    
    # get the average of yes/no counts
    summation = [] # for each attribute, there is a mean/std
    for i in range(num_of_attribute-1):
        summation.append({"yes":0,"no":0})
	
    for each_instance in training_data:
        if each_instance[-1] == "yes":
            for i in range(num_of_attribute-1):
                summation[i]["yes"] = summation[i]["yes"] + each_instance[i]
        else:
            for i in range(num_of_attribute-1):
                summation[i]["no"] = summation[i]["no"] + each_instance[i]

    mean = []
    for each_attri_num in summation:
        yes_mean = each_attri_num["yes"]/yes_count
        no_mean = each_attri_num["no"]/no_count
        mean.append({"yes":yes_mean,"no":no_mean})
    
    # After for loop, 8 attributes are added, so add class yes/no countings
    mean.append(yes_count) 
    #------------------------------------------------    
    # get the std of yes/no counts
    summation2 = [] # for each attribute, there is a mean/std
    for i in range(num_of_attribute-1):
        summation2.append({"yes":0,"no":0})
        
    for each_instance in training_data:
        class_of_diabete = each_instance[-1]
        for i in range(num_of_attribute-1):
            square = math.pow(each_instance[i] - mean[i][class_of_diabete],2)
            summation2[i][class_of_diabete] = summation2[i][class_of_diabete] + square

    std = []
    for each_square_num in summation2:
    
    # make sure your standard deviation function accounts for n=1 
    # (because it will do 1-1 then try to divide by 0, instead just return 0 if n = 1)
        if yes_count !=1 and no_count !=1:
            yes_std = math.sqrt(each_square_num["yes"]/(yes_count-1))
            no_std = math.sqrt(each_square_num["no"]/(no_count-1))
            std.append({"yes":yes_std,"no":no_std})
        elif yes_count ==1:
            yes_std = 0
            no_std = math.sqrt(each_square_num["no"]/(no_count-1))
            std.append({"yes":yes_std,"no":no_std})
        
        elif no_count ==1:
            yes_std = math.sqrt(each_square_num["yes"]/(yes_count-1))
            no_std = 0
            std.append({"yes":yes_std,"no":no_std})

    #------------------------------------------------    
    # Using testing data to get NB classifier result
    result = []
    for each_instance in testing_data:
        
        # To store P(attr1|yes),P(attr2|yes),P(attr3|yes)...in the lists
        prob_yes = []
        prob_no = []
        for i in range(num_of_attribute-1):
            prob_yes_for_this_attribute = prob_density(mean[i]["yes"],std[i]["yes"],each_instance[i])
            prob_yes.append(prob_yes_for_this_attribute)
            prob_no_for_this_attribute = prob_density(mean[i]["no"],std[i]["no"],each_instance[i])
            prob_no.append(prob_no_for_this_attribute)
            
        '''
        P(yes) and P(no) are known as p_yes and p_no in previous section, 
        to get P(yes|E) and P(no|E), we need 
        
        P(yes|E) =[ P(attr1|yes) * P(attr2|yes)* P(attr3|yes)*... ]*P(yes) / P(E)
        P(no|E) =[ P(attr1|no) * P(attr2|no)* P(attr3|no)*... ]*P(no) / P(E)
        '''            
        a = 1;b=1
        for p_y in prob_yes:
            a = p_y * a
        for p_n in prob_no:
            b = p_n * b
        
        nb_yes = a * p_yes        
        nb_no = b * p_no

        # Deccide the class based on NB probability
        if nb_no > nb_yes:
            result.append("no")
        else:
            result.append("yes")

    return result

#---------------------------------------------------------------------------- 
#----------------------------------------------------------------------------       
def parse_input_arguments(train_csv):
    file_train = open(train_csv)
    training_data = list(csv.reader(file_train))
    # Up to the above line, the input are read as Strings
    # convert str to float
    num_of_attribute = len(training_data[0])
    train_data = []
    for each_line in training_data:
        temp_data=[]
        for i in range(num_of_attribute-1):
            temp = float(each_line[i])
            temp_data.append(temp)
        temp_data.append(each_line[-1])
        train_data.append(temp_data)
    # now we have converted inputs
    return train_data
    
train_csv = sys.argv[1] 
test_csv = sys.argv[2]
algorithm = sys.argv[3]

training_data = parse_input_arguments(train_csv)
testing_data = parse_input_arguments(test_csv)
########################################################################
# Start to process

if algorithm == 'NB':
    result = naive_bayes(training_data, testing_data)
    for elt in result:
        print(elt)
else:
    k = int(algorithm[0])
    # knn classifier is just the storage of all the training data
    knn_classifier = KNN(k, training_entries)

    for e in testing_entries: # e is the instance (each row) in testing set
        
        # neighbour: 'k' instances that are closest to this testing data
        neighbour = knn_classifier.compute_distance(e)

        result_list = []
        for n in neighbour:
            result_list.append(n.result)

        # only get the last K elements in result_list
        reversed_result = result_list[::-1]
        second_result = reversed_result[0:k]
        final_result = second_result[::-1]
        # print(final_result)

        majority_class = most_frequent(final_result)
        print(majority_class)


