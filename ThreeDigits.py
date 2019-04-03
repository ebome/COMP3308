# Yang Gao 450614082 
# When run:  python 3308.py B puzzle.txt
from Number import Number
import copy
   

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


def generate_BFS_children_node(next_one, forbidden_list):
    
    # next_one is the node that we want to get its children by following constraints
    # BFS adds fringes node like a queue
    
    fringe_for_this_node = []
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
            
            new_node = Number(digit_flag=1, parent = next_one)
            new_node.set_1_2_3_digits_and_values(a_list)
            
            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_first_digit() !=9:
            first = next_one.get_first_digit() + 1
            second = next_one.get_second_digit()
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=1, parent = next_one)
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
            
            new_node = Number(digit_flag=2, parent = next_one)
            new_node.set_1_2_3_digits_and_values(a_list)
            
            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_second_digit() != 9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit() + 1
            third = next_one.get_third_digit()
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=2, parent = next_one)
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
            
            new_node = Number(digit_flag=3, parent = next_one)
            new_node.set_1_2_3_digits_and_values(a_list)
            
            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)	

        if next_one.get_third_digit() !=9:
            first = next_one.get_first_digit()
            second = next_one.get_second_digit()
            third = next_one.get_third_digit() + 1
            a_list=[first,second,third]
            
            new_node = Number(digit_flag=3, parent = next_one)
            new_node.set_1_2_3_digits_and_values(a_list)
            
            if is_in_forbidden(new_node,forbidden_list) == False:
                fringe_for_this_node.append(new_node)
    #------------------------------------------------------------------------
    return fringe_for_this_node 


def generate_DLS_children_node(next_one, forbidden_list):
    # similar to generate_BFS_children_node, but the depth need to be changed
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


# For h_val, if n_node is goal_node, then of course h_val=0
def calculate_manhattan_h(n_node, goal_node):
    a = abs(n_node.getFirstDigit() -goal_node.getFirstDigit())
    b = abs(n_node.getSecondDigit()-goal_node.getSecondDigit())
    c = abs(n_node.getThirdDigit() -goal_node.getThirdDigit())
    return a + b + c

###################################################################
# Breath-first search
###################################################################
# returns two variables: next_one, expanded_list
def BFS(start,goal,forbidden_list):
    '''
    start, goal are int
    '''
    start_value = Number(value=start, digit_flag=-1,parent=None) # parent of it: is None
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) # parent: is None
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    fringe = []
    next_one = copy.deepcopy(start_value) # next_one is a different object from start_value
    #-------------------------------------------------------------------------------
    while next_one.is_number_equals(goal_value)==False: 
        expanded_list.append(next_one) # NOTE: before next loop, we need remove next_one from fringe
    
        # Corner Case: if after 1000 loop, no path is found, then just stop
        if len(expanded_list) == 1000:
            return next_one, expanded_list

		# Normal case: get the children nodes for current node next_one,        
        # and add all the possible nodes into fringe   
        fringe_for_this_node = generate_BFS_children_node(next_one, forbidden_list)
        # Now we can add the fringe_for_this_node (i.e. children for this node) to the total fringe list
        # NOTE: add the fringe_for_this_node at the end of fringe --> this is how BFS works
        fringe = fringe + fringe_for_this_node 
        '''
        print([node.value for node in fringe])
        break
        '''
        
        # now the fringe is: [x1,x2,x3,...], we assume x1 as next_one, but also need to check if this is true
        next_one = fringe[0] # assign x1 to next_one
		# Corner case: if next_one is in expanded list (already expanded before), delete it from fringe, AND assign next_one the new value        
        for each_node in expanded_list:
            if next_one.expand_equals(each_node)==True: # if x1 is in expanded_list
                del fringe[0] # delete x1
                next_one = fringe[0] # assign x2 to next_one
                break
            else:
                pass
        # If no repetitive node in fringe after the for loop, just delete x1
        del fringe[0] 
    
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and next_one.is_number_equals(goal_value)==False: 
            return next_one, expanded_list

    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    if next_one.is_number_equals(goal_value):
        # it means next_one is goal, but in expand_list the goal is not included
        expanded_list.append(next_one)
        #print([node.value for node in expanded_list])
        return next_one, expanded_list

##############################################################################
# Ddpth-First Search
##############################################################################
# returns two variables: next_one, expanded_list
def DFS(start,goal,forbidden_list): # start, goal are int
    
    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    fringe = []
    next_one = copy.deepcopy(start_value) 
    #-------------------------------------------------------------------------------
    while next_one.is_number_equals(goal_value)==False: 
        expanded_list.append(next_one) # NOTE: before next loop, we need remove next_one from fringe
    
        # Corner Case: if after 1000 loop, no path is found, then just stop
        if len(expanded_list) == 1000:
             return next_one, expanded_list

        fringe_for_this_node = generate_BFS_children_node(next_one, forbidden_list)
        # different from BFS, the children node should be in the front in DFS
        fringe = fringe_for_this_node + fringe
        
        # now the fringe is: [x1,x2,x3,...], we assume x1 as next_one, but also need to check if this is true
        next_one = fringe[0] # assign x1 to next_one
		# Corner case: if next_one is in expanded list (already expanded before), delete it from fringe, AND assign next_one the new value        
        for each_node in expanded_list:
            if next_one.value == each_node.value and next_one.digit_flag != each_node.digit_flag : # if x1 is in expanded_list
                del fringe[0] # delete x1
                next_one = fringe[0] # assign x2 to next_one
                break
            else:
                pass
        # If no repetitive node in fringe after the for loop, just delete x1
        del fringe[0] 
    
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and next_one.is_number_equals(goal_value)==False: 
            return next_one, expanded_list

    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    if next_one.is_number_equals(goal_value):
        expanded_list.append(next_one)
        return next_one, expanded_list

############################################################################
# Iterative Deepening Search
# From lecture: deep-limit search impose a cut-off on maximal depth,
# So IDS is the loop of DLS until solution is found
############################################################################
# returns two variables: next_one, expanded_list
def IDS(start,goal,forbidden_list): # start, goal are int

    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )
    expanded_list = []
    
    #-------------------------------------------------------------------------------	
    depth_limit = 0
    max_len_of_expanded_list = 1000 # 1000 nodes allowed
    while len(expanded_list) < 1000:
        # do deep-limit search on given depth
        dls_next_one, deep_limit_list = DLS(start,goal,forbidden_list,max_len_of_expanded_list,depth_limit)
        # after one DLS check, we will add the depth limit
        depth_limit = depth_limit + 1
        # Get the dls expanded_list, and add it to the current expanded_list        
        expanded_list = expanded_list + deep_limit_list
        # loop should less than 1000, but if 1000 loops are finished --> cannot find solution yet
        max_len_of_expanded_list = max_len_of_expanded_list - len(deep_limit_list)
        if max_len_of_expanded_list <= 0:
            return dls_next_one, expanded_list
        # If we find goal, just return the results
        if dls_next_one.is_number_equals(goal_value):
            return dls_next_one, expanded_list
    #-------------------------------------------------------------------------------	
    
    # After some time, the while loop condition is false --> we find the goal
    return dls_next_one, expanded_list

'''
# Why adding max_len_of_expanded_list as input? since cut-off is 1000 nodes
def DLS(start,goal,forbidden_list,max_len_of_expanded_list,depth_limit): 

    start_value = Number(value=start, digit_flag=-1,parent=None,depth=0) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    expanded_list.append(start_value) # Initialize expanded_list with start value!
    fringe = []
    next_one = copy.deepcopy(start_value) 
    
    # Corner case: just search level = 0
    if depth_limit == 0:
        return start_value, expanded_list
    
    #-------------------------------------------------------------------------------	
    while next_one.is_number_equals(goal_value) == False:
        
        # Corner case: more than 1000 nodes
        if len(expanded_list) == max_len_of_expanded_list:
            return next_one, expanded_list
         
        # Corner case: the next_node is in forbidden list, and fringe still has some nodes
        # Discard the current next_one, and take the first node from fringe as new next_one
        if is_in_forbidden(next_one,forbidden_list) == True and len(fringe) != 0:
            next_one = fringe.pop(0)

        
        # Normal case: the node is not in forbidden list, and the deep limit is not reached,
        # so the loop will start to expand the fringe_list
        fringe_for_this_node=[]
        if is_in_forbidden(next_one,forbidden_list) == False:
            if next_one.depth < depth_limit:
                # fringe_for_this_node can guarantee that children nodes are not in forbidden list
                fringe_for_this_node = generate_DLS_children_node(next_one, forbidden_list)

        # Add the children nodes to fringe, make sure the added children are not in expanded_list
        fringe_for_this_node_copy = copy.deepcopy(fringe_for_this_node)
        for each_child in fringe_for_this_node_copy:               
            for each_node in expanded_list:
                if each_child.expand_equals(each_node)== True:
                    fringe_for_this_node.remove(each_child)
                else:
                    pass
                
        fringe = fringe_for_this_node + fringe 
        # print([node.value for node in fringe])
        
        # Corner case: No solution is found
        if len(fringe) == 0:
            return next_one, expanded_list   

        # Update the new next_one node
        next_one = fringe.pop(0)
        for each_node in expanded_list:
            if next_one.expand_equals(each_node)== False:
                expanded_list.append(next_one)

    #-------------------------------------------------------------------------------	
    return next_one, expanded_list
'''


############################################################################
# Hill-Climbing Search: Manhattan heuristic
############################################################################
# returns two variables: next_one, expanded_list
def hill_climb(start,goal,forbidden_list): # start, goal are int
    
    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    fringe = []
    next_one = copy.deepcopy(start_value) 
    #-------------------------------------------------------------------------------
    while next_one.is_number_equals(goal_value)==False: 
        expanded_list.append(next_one) # NOTE: before next loop, we need remove next_one from fringe
    
        # Corner Case: if after 1000 loop, no path is found, then just stop
        if len(expanded_list) == 1000:
            return next_one, expanded_list

        fringe_for_this_node = generate_BFS_children_node(next_one, forbidden_list)
        # different from BFS, the children node should be in the front in DFS
        fringe = fringe_for_this_node + fringe
        
        # now the fringe is: [x1,x2,x3,...], we assume x1 as next_one, but also need to check if this is true
        next_one = fringe[0] # assign x1 to next_one
		# Corner case: if next_one is in expanded list (already expanded before), delete it from fringe, AND assign next_one the new value        
        for each_node in expanded_list:
            if next_one.value == each_node.value and next_one.digit_flag != each_node.digit_flag : # if x1 is in expanded_list
                del fringe[0] # delete x1
                next_one = fringe[0] # assign x2 to next_one
                break
            else:
                pass
        # If no repetitive node in fringe after the for loop, just delete x1
        del fringe[0] 
    
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and next_one.is_number_equals(goal_value)==False: 
            return next_one, expanded_list

    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    if next_one.is_number_equals(goal_value):
        expanded_list.append(next_one)
        return next_one, expanded_list

############################################################################
# Greedy Search: same as Hill-climb, use Heuristic h_n
############################################################################
# returns two variables: next_one, expanded_list
def greedy_search(start,goal,forbidden_list): # start, goal are int
    
    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    fringe = []
    next_one = copy.deepcopy(start_value) 
    #-------------------------------------------------------------------------------
    while next_one.is_number_equals(goal_value)==False: 
        expanded_list.append(next_one) # NOTE: before next loop, we need remove next_one from fringe
    
        # Corner Case: if after 1000 loop, no path is found, then just stop
        if len(expanded_list) == 1000:
            return next_one, expanded_list

        fringe_for_this_node = generate_BFS_children_node(next_one, forbidden_list)
        # different from BFS, the children node should be in the front in DFS
        fringe = fringe_for_this_node + fringe
        
        # now the fringe is: [x1,x2,x3,...], we assume x1 as next_one, but also need to check if this is true
        next_one = fringe[0] # assign x1 to next_one
		# Corner case: if next_one is in expanded list (already expanded before), delete it from fringe, AND assign next_one the new value        
        for each_node in expanded_list:
            if next_one.value == each_node.value and next_one.digit_flag != each_node.digit_flag : # if x1 is in expanded_list
                del fringe[0] # delete x1
                next_one = fringe[0] # assign x2 to next_one
                break
            else:
                pass
        # If no repetitive node in fringe after the for loop, just delete x1
        del fringe[0] 
    
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and next_one.is_number_equals(goal_value)==False: 
            return next_one, expanded_list

    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    if next_one.is_number_equals(goal_value):
        expanded_list.append(next_one)
        return next_one, expanded_list



############################################################################
# A* Search: f_n = Manhattan heuristic + depth_limit_cost
############################################################################
# returns two variables: next_one, expanded_list
def A_star_search(start,goal,forbidden_list): # start, goal are int
    
    start_value = Number(value=start, digit_flag=-1,parent=None) 
    start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
    goal_value = Number(value=goal, digit_flag=-1,parent=None) 
    goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )

    expanded_list = []
    fringe = []
    next_one = copy.deepcopy(start_value) 
    #-------------------------------------------------------------------------------
    while next_one.is_number_equals(goal_value)==False: 
        expanded_list.append(next_one) # NOTE: before next loop, we need remove next_one from fringe
    
        # Corner Case: if after 1000 loop, no path is found, then just stop
        if len(expanded_list) == 1000:
            return next_one, expanded_list

        fringe_for_this_node = generate_BFS_children_node(next_one, forbidden_list)
        # different from BFS, the children node should be in the front in DFS
        fringe = fringe_for_this_node + fringe
        
        # now the fringe is: [x1,x2,x3,...], we assume x1 as next_one, but also need to check if this is true
        next_one = fringe[0] # assign x1 to next_one
		# Corner case: if next_one is in expanded list (already expanded before), delete it from fringe, AND assign next_one the new value        
        for each_node in expanded_list:
            if next_one.value == each_node.value and next_one.digit_flag != each_node.digit_flag : # if x1 is in expanded_list
                del fringe[0] # delete x1
                next_one = fringe[0] # assign x2 to next_one
                break
            else:
                pass
        # If no repetitive node in fringe after the for loop, just delete x1
        del fringe[0] 
    
        # Corner case: fringe is empty but we still cannot find solution
        if len(fringe)==0 and next_one.is_number_equals(goal_value)==False: 
            return next_one, expanded_list

    #-------------------------------------------------------------------------------	
    # After some time, the while loop condition is false --> we find the goal
    if next_one.is_number_equals(goal_value):
        expanded_list.append(next_one)
        return next_one, expanded_list




############################################################################
# Now we can run the script
############################################################################



filename = 'puzzle.txt'
start, goal,forbidden_list = read_the_input(filename)

max_len_of_expanded_list=1000;depth_limit=2

start_value = Number(value=start, digit_flag=-1,parent=None,depth=0) 
start_value.set_1_2_3_digits_and_values( extract_digits_from_value(start) )
goal_value = Number(value=goal, digit_flag=-1,parent=None) 
goal_value.set_1_2_3_digits_and_values( extract_digits_from_value(goal) )


#---------------------------------------------------------------
expanded_list = []
expanded_list.append(start_value) # Initialize expanded_list with start value!
fringe = []
next_one = copy.deepcopy(start_value) 

while next_one.is_number_equals(goal_value) == False:
                   
    fringe_for_this_node=[]
    if is_in_forbidden(next_one,forbidden_list) == False:
        if next_one.depth < depth_limit:
            fringe_for_this_node = generate_DLS_children_node(next_one, forbidden_list)

        # Add the children nodes to fringe, make sure the added children are not in expanded_list
    fringe_for_this_node_copy = copy.deepcopy(fringe_for_this_node)
    for each_child in fringe_for_this_node_copy:               
        for each_node in expanded_list:
            if each_child.expand_equals(each_node)== True:
                fringe_for_this_node.remove(each_child)
            else:
                pass
                
    fringe = fringe_for_this_node + fringe 
    
    print('fringe nodes',[node.value for node in fringe])
        
    # Update the new next_one node
    next_one = fringe.pop(0)
    print('next_one that is not in fringe:',next_one.value)
    
    fringe_copy = copy.deepcopy(fringe)
    print('fringe_copy:',[node.value for node in fringe_copy])
    
    for each_node in fringe_copy:
        if next_one.depth == depth_limit and next_one.is_number_equals(goal_value) == False:
            expanded_list.append(next_one)
            print('expanded_list:',[node.value for node in expanded_list])
            
            next_one = copy.deepcopy(each_node)
            print('next_one in for loop:',next_one.value)
            print('-----------------')
            
            #fringe.remove(next_one)
            print('fringe nodes aaaaaaaaaaaaaaaaaaaaaaaaaaaa',[node.value for node in fringe])

            

    expanded_list.append(next_one)
#---------------------------------------------------------------


        if next_one.depth == depth_limit and next_one.is_number_equals(goal_value) == True:
            break # return next_one, expanded_list
        break
    
        if next_one.depth != depth_limit:
            break


next_one, expanded_list = IDS(start,goal,forbidden_states)
print(next_one.value)
print([node.value for node in expanded_list])


print_path(next_one)
print_expanded_list(expanded_list)





