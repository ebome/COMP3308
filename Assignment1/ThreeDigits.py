# When run:  python 3308.py B puzzle.txt
from Number import Number
import copy
import sys
   

################################################
# Read everything and store as variables
def read_the_input(filename):
	result=[]
	with open(filename,'r') as f:
		for line in f:
			result.append(list(line.strip('\n').split(',')))
	start_state = int(result[0][0])
	goal_state = int(result[1][0])
	forbidden_states=[]
	if len(result)==3: # forbiddens are exist, and as 3rd line exist, it will not be empty
		temp = result[2]
		forbidden_states = [ int(x) for x in temp ]
	# print(forbidden_states)
	return start_state,goal_state,forbidden_states

# Utility functions
def extract_digits_from_value(value): # value is a int
    if value >=100:
        value_str = str(value)
        first_str = value_str[0]
        second_str = value_str[1]
        third_str = value_str[2]
        first = int(first_str)
        second = int(second_str)
        third = int(third_str)
        return [first,second,third]
    if value >=10 and value < 100:
        value_str = str(value)
        first = 0
        second_str = value_str[0]
        third_str = value_str[1]
        second = int(second_str)
        third = int(third_str)
        return [first,second,third]
    if value < 10:
        value_str = str(value)
        first = 0
        second = 0
        third_str = value_str[0]
        third = int(third_str)
        return [first,second,third]

################################################
# To do search, the search list must be quene (FIFO) 
# not stack (LIFO)
################################################

# Only one parent for each node, so track back
def print_path(value): 
	temp = []
	parent = value.get_parent()
	while parent != None:
		temp.append( parent.object_to_str() )
		parent = parent.get_parent() # update parent to find grandparent of current node
	# insert the 'value' node to the 1st of the list
	temp.insert(0,value.object_to_str())
	# reverse the list
	path = temp[::-1]
	# path is a list, so we need change it to string
	output = ','.join(map(str, path))	
	print(output)

	
def print_expanded_list(expanded_list):
	s = ''
	for i in range(0,len(expanded_list)):
		number_object = expanded_list[i]
		s = s + number_object.object_to_str() + ','
	# remove ',' in the last index	
	s = s[:-1]			
	print(s)


def is_in_forbidden(node, forbidden_list): # forbidden_list is int list
    '''
    value is a node, forbidden_list is int list
    '''
    if len(forbidden_list)== 0:
        return False    
    for i in range(0,len(forbidden_list)):
        if node.value == forbidden_list[i]: # if node is in forbidden list
            return True
    # after for loop, node is not in forbidden list
    return False

# For h_val, if n_node is goal_node, then of course h_val=0
def calculate_manhattan_h(n_node, goal_node):
    a = abs(n_node.get_first_digit() -goal_node.get_first_digit())
    b = abs(n_node.get_second_digit()-goal_node.get_second_digit())
    c = abs(n_node.get_third_digit() -goal_node.get_third_digit())
    return a + b + c

def generate_heuristic_children_node(next_one, goal_node, forbidden_list):
    '''
    next_one, goal_node are necessary for heuristic methods
    next_one is the node that we want to get its children by following constraints
    Adds fringes node like a queue

    '''
    fringe_for_this_node = []
    new_depth = next_one.depth + 1
    # chech if the same digit is changed in successive moves
    #------------------------------------------------------------------------
    # get_digit_flag()=1: cannot change first digit
    if next_one.get_digit_flag() !=1:
        # check if 0 or 9 at this digit        
        if next_one.get_first_digit() !=0:
            first = next_one.get_first_digit() - 1
            second = next_one.get_second_digit()
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=1, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_first_digit() !=9:
            first = next_one.get_first_digit() + 1
            second = next_one.get_second_digit()
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=1, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )            
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)		
    #------------------------------------------------------------------------
	# get_digit_flag()=2: cannot change second digit
    if next_one.get_digit_flag() !=2:
        # check if 0 or 9 at this digit
        if next_one.get_second_digit() !=0:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit() - 1
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=2, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_second_digit() != 9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit() + 1
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=2, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)		
    #------------------------------------------------------------------------
	# get_digit_flag()=3: cannot change third digit
    if next_one.get_digit_flag() !=3:
        # check if 0 or 9 at this digit
        if next_one.get_third_digit() !=0:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit()
            third = next_one.get_third_digit() - 1
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=3, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_third_digit() !=9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit()
            third = next_one.get_third_digit() + 1
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=3, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)
            new_node.set_h_value( calculate_manhattan_h(new_node, goal_node) )
            new_node.set_f_val()

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)
    
    return fringe_for_this_node    

def generate_uninformed_children_node(next_one,forbidden_list):
    '''
    next_one, goal_node are necessary for heuristic methods
    next_one is the node that we want to get its children by following constraints
    Adds fringes node like a queue

    '''
    fringe_for_this_node = []
    new_depth = next_one.depth + 1
    # chech if the same digit is changed in successive moves
    #------------------------------------------------------------------------
    # get_digit_flag()=1: cannot change first digit
    if next_one.get_digit_flag() !=1:
        # check if 0 or 9 at this digit        
        if next_one.get_first_digit() !=0:
            first = next_one.get_first_digit() - 1
            second = next_one.get_second_digit()
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=1, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_first_digit() !=9:
            first = next_one.get_first_digit() + 1
            second = next_one.get_second_digit()
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=1, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)		
    #------------------------------------------------------------------------
	# get_digit_flag()=2: cannot change second digit
    if next_one.get_digit_flag() !=2:
        # check if 0 or 9 at this digit
        if next_one.get_second_digit() !=0:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit() - 1
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=2, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_second_digit() != 9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit() + 1
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=2, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)		
    #------------------------------------------------------------------------
	# get_digit_flag()=3: cannot change third digit
    if next_one.get_digit_flag() !=3:
        # check if 0 or 9 at this digit
        if next_one.get_third_digit() !=0:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit()
            third = next_one.get_third_digit() - 1
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=3, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_third_digit() !=9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit()
            third = next_one.get_third_digit() + 1
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=3, parent = next_one, depth=new_depth)
            new_node.set_1_2_3_digits_and_values(a_list)

            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)
    
    return fringe_for_this_node    


###################################################################
# Breath-first search
###################################################################
# returns two variables: current_node, expanded_list
def BFS(start_state,goal_state,forbidden_list):
    
    goal_node = Number(value=goal_state, digit_flag=-1,parent=None) 
    goal_node.set_1_2_3_digits_and_values( extract_digits_from_value(goal_state) )
    goal_node.set_h_value( calculate_manhattan_h(goal_node, goal_node) )
    # start node can only be construct after goal node is construct
    start_node = Number(value=start_state, digit_flag=-1,parent=None) 
    start_node.set_1_2_3_digits_and_values( extract_digits_from_value(start_state) )
    start_node.set_h_value( calculate_manhattan_h(start_node, goal_node) )
 
    # Initialization
    current_node = copy.deepcopy(start_node)
    expanded_list = []
    fringe = []
    #-------------------------------------------------------------------------------
    while current_node.is_number_equals(goal_node)==False and len(expanded_list) < 1000:
        # add the current node to expand list
        expanded_list.append(current_node)

        children = generate_uninformed_children_node(current_node,forbidden_list)
        fringe = fringe + children
        # print([node.value for node in fringe])
        
        # To expand the 1st node in fringe, we need to check if we can expand it
        # Reference: https://github.com/jess-ha
        for unexpanded_node in fringe:
            # if the node in fringe has same value as in expanded_list
            # then check if the digit_flag is same as well, if yes, then they are same node
            expanded_values = [node.value for node in expanded_list]
            if unexpanded_node.value in expanded_values:                
                if unexpanded_node.is_in_expand_list(expanded_list):
                    del unexpanded_node
                # if the digit_flag is different, then they are not same node, so we can use this node coming from fringe
                else:
                    current_node = unexpanded_node
                    del unexpanded_node
                    break
            else:
                # if the node in fringe has different value in expanded_list, then of course we can use it
                current_node = unexpanded_node
                del unexpanded_node
                break

        # Corner case: cannot find solution even if fringe is expanded completely
        if len(fringe) == 0 and current_node.is_number_equals(goal_node)==False:
            return current_node, expanded_list
    #-------------------------------------------------------------------------------
    # After the while loop is break, we get the goal node
    expanded_list.append(current_node)
    return current_node, expanded_list


##############################################################################
# Depth-First Search
##############################################################################
# returns two variables: current_node, expanded_list
def DFS(start,goal,forbidden_list): 
    
    goal_node = Number(value=goal, digit_flag=-1,parent=None) 
    goal_node.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    goal_node.set_h_value( calculate_manhattan_h(goal_node, goal_node) )
    
    start_node = Number(value=start, digit_flag=-1,parent=None) 
    start_node.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    start_node.set_h_value( calculate_manhattan_h(start_node, goal_node) )
    
    current_node = copy.deepcopy(start_node)
    expanded_list = []
    fringe = []
    #-------------------------------------------------------------------------------
    while current_node.is_number_equals(goal_node)==False and len(expanded_list) < 1000:
        expanded_list.append(current_node)
        children = generate_uninformed_children_node(current_node,forbidden_list)
        fringe = children + fringe
        
        # To expand the 1st node in fringe, we need to check if we can expand it        
        for unexpanded_node in fringe:
            # if the node in fringe has same value as in expanded_list
            # then check if the digit_flag is same as well, if yes, then they are same node
            if unexpanded_node.value in [node.value for node in expanded_list]:
                if unexpanded_node.is_in_expand_list(expanded_list) == False:
                    current_node = unexpanded_node
                    fringe.remove(unexpanded_node)
                    break
            else:
                current_node = unexpanded_node
                fringe.remove(unexpanded_node)
                break           

        
        
        # Corner case: cannot find solution even if fringe is expanded completely
        if len(fringe) == 0 and current_node.is_number_equals(goal_node)==False:
            return current_node, expanded_list
    #-------------------------------------------------------------------------------
    # After the while loop is break, we get the goal node
    expanded_list.append(current_node)
    return current_node, expanded_list

    
############################################################################
# Iterative Deepening Search
# From lecture: deep-limit search impose a cut-off on maximal depth,
# So IDS is the loop of DLS until solution is found
############################################################################
# returns two variables: current_node, expanded_list
def IDS(start,goal,forbidden_list): # start, goal are int

    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    expanded_list = []
    #-------------------------------------------------------------------------------	
    depth_limit = 0
    max_len_of_expanded_list = 1000
    
    while len(expanded_list) < 1000:
        # do deep-limit search on given depth
        dls_current_node, deep_limit_list = DLS(start,goal_value,forbidden_list,max_len_of_expanded_list,depth_limit)
        
        # after one DLS check, we will add the depth limit
        depth_limit = depth_limit + 1
        
        # Get the dls expanded_list, and add it to the current expanded_list        
        expanded_list = expanded_list + deep_limit_list
        
        # loop should less than 1000, but if 1000 loops are finished --> cannot find solution yet
        max_len_of_expanded_list = max_len_of_expanded_list - len(deep_limit_list)
        if max_len_of_expanded_list <= 0:
            return dls_current_node, expanded_list
       
        # If we find goal, just return the results
        if dls_current_node.is_number_equals(goal_value):
            return dls_current_node, expanded_list
    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    return dls_current_node, expanded_list



def DLS(start,goal_value,forbidden_list,max_len_of_expanded_list,depth_limit): 
    '''
    start: int    goal_value: node
    Why adding max_len_of_expanded_list as input? since cut-off is 1000 nodes
    '''
    start_value = Number(value=start, digit_flag=-1,parent=None,depth=0) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    expanded_list = []
    expanded_list.append(start_value) # Initialize expanded_list with start value!
    
    # Corner case: just search level = 0, so expanded_list only contains start_node
    if depth_limit == 0:
        return start_value, expanded_list

    current_node = copy.deepcopy(start_value)
    fringe = []

    #-------------------------------------------------------------------------------	
    while (current_node.is_number_equals(goal_value) == False and len(expanded_list) < max_len_of_expanded_list):
                 
        # Corner case: the next_node is in forbidden list, and fringe still has some nodes
        # Discard the current next_one, and take the first node from fringe as new next_one
        if is_in_forbidden(current_node,forbidden_list) == True and len(fringe) != 0:
            current_node = fringe.pop(0)
        
        # Normal case: the node is not in forbidden list, and the deep limit is not reached,
        # so the loop will start to expand the fringe_list
        fringe_for_this_node=[]
        if is_in_forbidden(current_node,forbidden_list) == False:
            if current_node.depth < depth_limit:
                # fringe_for_this_node can guarantee that children nodes are not in forbidden list
                fringe_for_this_node = generate_uninformed_children_node(current_node, forbidden_list)
                fringe_for_this_node = fringe_for_this_node[::-1]
                
        # check if children nodes are in expanded_list, if not add it to the front of fringe
        for child in fringe_for_this_node:
            if child.is_in_expand_list(expanded_list)== False:
                fringe.insert(0,child)

        # check if children nodes are in expanded_list, if yes, add it to the front from fringe
        for node in fringe:
            if node.is_in_expand_list(expanded_list)== True:
                fringe.remove(node)
                   
        # Corner case: fringe is empty after updating
        if (len(fringe) == 0 and current_node.is_number_equals(goal_value) == False):
            return current_node, expanded_list

        # To check if 1st node in fringe could be expanded
        current_node = fringe.pop(0)
        if (current_node.value in [node.value for node in expanded_list] and current_node.is_in_expand_list(expanded_list)== False):
            expanded_list.append(current_node)
        else:
            expanded_list.append(current_node)
    #-------------------------------------------------------------------------------	
    return current_node, expanded_list

############################################################################
# Hill-Climbing Search: Manhattan heuristic
############################################################################
# returns two variables: current_node, expanded_list
def hill_climb(start,goal,forbidden_list): 

    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    # After getting goal node, set heuristic
    start_value.set_h_value( calculate_manhattan_h(start_value, goal_value) )
    goal_value.set_h_value( calculate_manhattan_h(goal_value, goal_value) )

    expanded_list = []
    current_node = copy.deepcopy(start_value) 
    #-------------------------------------------------------------------------------
    while current_node.is_number_equals(goal_value)==False and len(expanded_list) < 1000: 
        # Hill climb is local optimal method, the fringe should be updated during each loop
        # no need to save fringe
        fringe = [] 
        expanded_list.append(current_node) 

        fringe_for_this_node = generate_heuristic_children_node(current_node, goal_value, forbidden_list)
  
        # loop all the children nodes, and put the smallest_h_val_node into the front of fringe
        # Add children of expanded node to fringe
        while len(fringe_for_this_node) != 0:
            child = fringe_for_this_node.pop(0)
            # regardless of if digit_flag is same in expanded_list, the fringe has to be sort from small h to large h
            if child.value in [node.value for node in expanded_list] and current_node.is_in_expand_list(expanded_list)== False :
                # The if-else below inserts the smaller h_val node from children in front of fringe
                if len(fringe) != 0:
                    for i in range(len(fringe)):
                        if fringe[i].h_val >= child.h_val:
                            fringe.insert(i, child)
                            break
                else:
                    fringe.append(child)

            if child.value not in [node.value for node in expanded_list]:
                # The if-else below inserts the smaller h_val node from children in front of fringe
                if len(fringe) != 0:
                    for i in range(len(fringe)):
                        if fringe[i].h_val >= child.h_val:
                            fringe.insert(i, child)
                            break
                else:
                    fringe.append(child)
        # after the for loop, fringe has a sequence from smallest h_val to largest h_val
        
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0: 
            return current_node, expanded_list
        
        # To check if 1st node in fringe could be expanded
        if current_node.h_val < fringe[0].h_val:
            return current_node, expanded_list
        else:
            current_node = fringe.pop(0)        
    #-------------------------------------------------------------------------------
    expanded_list.append(current_node)
    return current_node, expanded_list

############################################################################
# Greedy Search: Same as Hill-climb, use Heuristic h_n
############################################################################
# returns two variables: current_node, expanded_list
def greedy_search(start,goal,forbidden_list):

    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    start_value.set_h_value( calculate_manhattan_h(start_value, goal_value) )
    goal_value.set_h_value( calculate_manhattan_h(goal_value, goal_value) )

    expanded_list = []
    current_node = copy.deepcopy(start_value) 
    fringe = []
    #-------------------------------------------------------------------------------
    while current_node.is_number_equals(goal_value)==False and len(expanded_list) < 1000: 
        expanded_list.append(current_node) 
        fringe_for_this_node = generate_heuristic_children_node(current_node, goal_value, forbidden_list)
  
        for child in fringe_for_this_node:
            if (child.value in [node.value for node in expanded_list]) and (child.is_in_expand_list(expanded_list)== False):
                if len(fringe)==0:
                    fringe.append(child)
                else:
                    for i in range(len(fringe)):
                        node = fringe[i]
                        if node.h_val >= child.h_val:
                            fringe.insert(i,child)
                            break
                
            if (child.value not in [node.value for node in expanded_list]):
                if len(fringe)==0:
                    fringe.append(child)
                else:
                    for i in range(len(fringe)):
                        node = fringe[i]
                        if node.h_val >= child.h_val:
                            fringe.insert(i,child)
                            break    

        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and current_node.is_number_equals(goal_value)==False: 
            return current_node, expanded_list
        
        # To check if 1st node in fringe could be expanded
        current_node = fringe.pop(0)        
    #-------------------------------------------------------------------------------
    expanded_list.append(current_node)
    return current_node, expanded_list

############################################################################
# A* Search: f_n = Manhattan heuristic + depth_limit_cost
############################################################################
# returns two variables: current_node, expanded_list
def A_star_search(start,goal,forbidden_list): 
    
    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    # After getting goal node, set heuristic and f_value
    start_value.set_h_value( calculate_manhattan_h(start_value, goal_value) )
    goal_value.set_h_value( calculate_manhattan_h(goal_value, goal_value) )
    start_value.set_f_val()
    goal_value.set_f_val()

    expanded_list = []
    current_node = copy.deepcopy(start_value) 
    fringe = []

    #-------------------------------------------------------------------------------
    while current_node.is_number_equals(goal_value)==False and len(expanded_list) < 1000: 
        expanded_list.append(current_node) 
        fringe_for_this_node = generate_heuristic_children_node(current_node, goal_value, forbidden_list)
  
        for child in fringe_for_this_node:
            if (child.value in [node.value for node in expanded_list]) and (child.is_in_expand_list(expanded_list)== False):
                    
                if len(fringe)==0:
                    fringe.append(child)
                else:
                    for i in range(len(fringe)):
                        node = fringe[i]
                        if node.f_val >= child.f_val:
                            fringe.insert(i,child)
                            break
                
            if (child.value not in [node.value for node in expanded_list]):
                
                if len(fringe)==0:
                    fringe.append(child)
                else:
                    for i in range(len(fringe)):
                        node = fringe[i]
                        if node.f_val >= child.f_val:
                            fringe.insert(i,child)
                            break

        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and current_node.is_number_equals(goal_value)==False: 
            return current_node, expanded_list
        
        # To check if 1st node in fringe could be expanded
        current_node = fringe.pop(0)        
    #-------------------------------------------------------------------------------
    expanded_list.append(current_node)
    return current_node, expanded_list

############################################################################
# Now we can run the script
############################################################################  
if __name__ == '__main__':
    algorithm = sys.argv[1] # could be: B D I G A H
    filename = sys.argv[2]
    # start_state, goal_state,forbidden_states are int/int lists
    start_state, goal_state,forbidden_states = read_the_input(filename)
    
    # set the goal_node for use
    goal_node = Number(value=goal_state, digit_flag=-1,parent=None) 
    goal_node.set_1_2_3_digits_and_values( extract_digits_from_value(goal_state) )
    goal_node.set_h_value( calculate_manhattan_h(goal_node, goal_node) )
    goal_node.set_f_val()

    if algorithm == 'B':
        next_one, expanded_list = BFS(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            expanded_list = expanded_list[:-1]
            print_expanded_list(expanded_list)


    if algorithm == 'D':
        next_one, expanded_list = DFS(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            expanded_list = expanded_list[:-1]
            print_expanded_list(expanded_list)

    if algorithm == 'I':
        next_one, expanded_list = IDS(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            print_expanded_list(expanded_list)
            
    if algorithm == 'H':
        next_one, expanded_list = hill_climb(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            print_expanded_list(expanded_list)

    if algorithm == 'G':
        next_one, expanded_list = greedy_search(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            print_expanded_list(expanded_list)

    if algorithm == 'A':
        next_one, expanded_list = A_star_search(start_state, goal_state,forbidden_states)
        if next_one.is_number_equals(goal_node)==True:
            print_path(next_one)
            print_expanded_list(expanded_list)
        else: 
            print('No solution found.')
            print_expanded_list(expanded_list)
