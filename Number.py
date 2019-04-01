# python Number.py
class Number(object):
    def __init__(self, value=None,first=None,second=None,third=None, digit_flag=None, parent=None,h_val=0, depth=0,f_val=0):
        self.value = value
        if value >= 100 or value == None :
            self.first = first # 1st digit from left
            self.second = second
            self.third = third
        if value >=10 :
            self.first = 0
            self.second = second
            self.third = third			
        if value < 10 :
            self.first = 0
            self.second = 0
            self.third = value		
		
        self.parent = parent
        self.h_val = h_val
        self.digit_flag = digit_flag # -1:no change; 1:cannot change 1st digit; 2,3...
        self.depth = depth
        self.f_val = f_val

    def set_Heuristic_val(self,h_val):
        self.h_val = h_val
		
    def set_f_n(self,f_val):
        self.f_val = f_val
		
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
	    if self.first == n.first and self.second == n.second and self.third == n.third:
		    return True
	    else:
		    return False
	
	# This function tries to avoid the cycles
    def expand_equals(self,n):
	    return self.first == n.first and self.second == n.second and self.third == n.third \
	    and self.digit_flag == n.digit_flag
	
    def object_to_str(self): 
        s = str(self.first)+str(self.second)+str(self.third)
        return s
	
	
	
	
