#In this module I'm going to gather all of my universal applicable functions for scripting
#November 2022

#This function is used to create a Y/N promt in the terminal
def yesOrNo(question_str, default = "yes"):
    
    valid_inp = {"yes": True, "ye": True, "y": True, "no": False, "n": False}

    if default == None: template = "[y/n]"
    elif default.lower() == "yes": template = "[Y/n]"
    elif default.lower() == "no": template = "[y/N]"
    else: raise ValueError(f"Invalid default value passed: {default}")

    while True:
        #print(question_str + template)
        ans = input(question_str + template).lower()
        if default is not None and ans == "": return valid_inp[default.lower()]
        elif default.lower() in valid_inp: return valid_inp[ans]
        else: print("Please respond with 'yes'(y) or 'no'(n)")
