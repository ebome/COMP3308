# Yang Gao 450614082 
# When run:  python 3308.py B puzzle.txt
import sys
from Number import Number


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

################################################
# To do search, the search list must be quene (FIFO) 
# not stack (LIFO)
################################################
def print_path(value):
	temp = []
	parent = value.get_parent()
	while parent != None:
		temp = temp.append( parent.object_to_str() )
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

def is_in_forbidden(value, forbidden_list): # forbidden_list is int list
	if len(forbidden_list)== 0:
		return False
	
	value_str = value.object_to_str()
	value_int = int(value_str)
	for i in range(0,len(forbidden_list)):
	    if value_int == forbidden_list[i]:
             return True

# BFS will return the value and expanded_list for printing
def BFS(start,goal,forbidden_list):
	start_value = Number(value=start, digit_flag=-1,parent=None) # parent of it: is None
	goal_value = Number(value=start, digit_flag=-1,parent=None) # parent: is None
	
	expanded_list = []
	fringe = []
	
	expanded_list.append(start_value)
	next_one = start_value # Intialize next_one, later it will change
	fringe.append(next_one)
	
	#-------------------------------------------------------------------------------
	counter = 0
	while counter<1000:
		
		'''
		# Corner case: fringe is empty
		if len(fringe)==0: # if fringe is empty list
			print_path(next_one) # For Tree, each child ONLY has 1 parent
			print_expanded_list(expanded_list)
			break
		'''
		
		# Corner case: we reach the goal
		if next_one.is_number_equals(goal_value):
			print_path(next_one) 
			print_expanded_list(expanded_list)
			break

		# Corner case: if next_one is in expanded list (already expanded before)
		for x in range(0,len(expanded_list)):
			if next_one.expand_equals(expanded_list[x]): 
				# if the next one is the same as expanded_list, then to avoid cycles, 
				# this next_one will not add to expanded_list				
				fringe.remove(next_one)
			else:
				pass
		
		# normal case: chech if the same digit is changed in successive moves
		#------------------------------------------------------------------------
		# get_digit_flag()=1: cannot change first digit
		if next_one.get_digit_flag()!=1:
			
			# check if 0 or 9 at this digit
			if next_one.get_first_digit()!=0:
				new_node = Number(first = next_one.get_first_digit()-1,\
								  second = next_one.get_second_digit(), \
								  third = next_one.get_third_digit(), \
								  digit_flag=1, parent = next_one)
				# if the new_node is not in forbidden list, we add it to fringe (not expanded_list)
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)
			elif next_one.get_first_digit()!=9:
				new_node = Number(first = next_one.get_first_digit()+1,\
								  second = next_one.get_second_digit(), \
								  third = next_one.get_third_digit(), \
								  digit_flag=1, parent = next_one)		
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)
		    		
		#------------------------------------------------------------------------
		# get_digit_flag()=2: cannot change second digit
		if next_one.get_digit_flag()!=2:
			
			# check if 0 or 9 at this digit
			if next_one.get_second_digit()!=0:
				new_node = Number(first = next_one.get_first_digit(),\
								  second = next_one.get_second_digit()-1, \
								  third = next_one.get_third_digit(), \
								  digit_flag=2, parent = next_one)
				# if the new_node is not in forbidden list, we add it to fringe (not expanded_list)
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)
			elif next_one.get_second_digit()!=9:
				new_node = Number(first = next_one.get_first_digit(),\
								  second = next_one.get_second_digit()+1, \
								  third = next_one.get_third_digit(), \
								  digit_flag=2, parent = next_one)		
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)

		#------------------------------------------------------------------------
		# get_digit_flag()=3: cannot change third digit
		if next_one.get_digit_flag()!=3:
			
			# check if 0 or 9 at this digit
			if next_one.get_third_digit()!=0:
				new_node = Number(first = next_one.get_first_digit(),\
								  second = next_one.get_second_digit(), \
								  third = next_one.get_third_digit()-1, \
								  digit_flag=3, parent = next_one)
				# if the new_node is not in forbidden list, we add it to fringe (not expanded_list)
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)
			elif next_one.get_third_digit()!=9:
				new_node = Number(first = next_one.get_first_digit(),\
								  second = next_one.get_second_digit(), \
								  third = next_one.get_third_digit()+1, \
								  digit_flag=3, parent = next_one)		
				if is_in_forbidden(new_node,forbidden_list) == False:
					fringe.append(new_node)		
		
		# once we assign new_node to next_one, the new_node should be removed from fringe list
		next_one = fringe.pop(0) 
		
		counter = counter+1
		'''
		# after 1000 loops, if no solution found, print the results
		print('No Solution found')
		print_expanded_list(expanded_list)
		'''
	#-------------------------------------------------------------------------------	
    # after 1000 loop, no path is found, then






################################################
# Now we can run the script
################################################
filename = 'puzzle.txt'
start_state, goal_state,forbidden_states = read_the_input(filename)
BFS(start_state,goal_state,forbidden_states)






















