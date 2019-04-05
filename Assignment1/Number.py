# python Number.py
class Number(object):
    def __init__(self, value=1,first=1,second=1,third=5, digit_flag=None, parent=None,h_val=0, depth=0,f_val=0):
        self.value = value
       
        self.first = first # 1st digit from left
        self.second = second
        self.third = third

        self.parent = parent
        self.h_val = h_val
        self.digit_flag = digit_flag # -1:no change; 1:cannot change 1st digit; 2,3...
        self.depth = depth
        self.f_val = f_val

    def set_h_value(self,h_val):
        self.h_val = h_val

    def set_1_2_3_digits_and_values(self,a_list): # int list, a_list = [first, second, third]
        self.first = a_list[0] # 1st digit from left
        self.second = a_list[1]
        self.third = a_list[2]
        self.value = a_list[0]*100  + a_list[1]*10 + a_list[2]
	 
    def set_f_val(self):
        self.f_val = self.depth + self.h_val
             
    def get_value(self):
	    return self.value
    def get_digit_flag(self):
	    return self.digit_flag
    def get_first_digit(self):
	    return self.first
    def get_second_digit(self):
	    return self.second
    def get_third_digit(self):
	    return self.third
	
    def get_parent(self):
	    return self.parent	

    def get_Heuristic_val(self):
        return self.h_val
	
    def is_number_equals(self,n):
	    return (self.first == n.first and self.second == n.second and self.third == n.third)

	# This function tries to avoid the cycles
    def is_in_expand_list(self,expanded_list):
        if len(expanded_list)==0:
            return False
        
        for node in expanded_list:
           if self.first == node.first and self.second == node.second and self.third == node.third and self.digit_flag == node.digit_flag:
               return True
           else:
               continue
        return False

    def object_to_str(self): 
        s = str(self.first)+str(self.second)+str(self.third)
        return s
