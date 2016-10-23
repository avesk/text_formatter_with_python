#!/usr/bin/env

import sys
import fileinput


formatKeys = {"LW": 0, "LM": 0, "LS": 0, "FT": "on"}
charCount = 0
withoutNewline = False

def main():
        global withoutNewline
        idx = 0
        line = 0
        firstWord = True
        firstMargin = 0
        for line in fileinput.input():
            if(set_args(line)):
                if idx == 0 and formatKeys["LM"] > 0:
                    #print("LM ARGS: {}".format(formatKeys["LM"]))
                    lm_printer(formatKeys["LM"])
                    firstMargin = formatKeys["LM"]
                    idx +=1
                continue
            firstWord = format(line, firstWord, firstMargin)
            idx +=1
            firstMargin = 0 
    
        print()

def set_args(line):
    global formatKeys
    isCode = False
    
    if ".LW" in line: #Check if formatting command is in the line
        line = line.split() #Put the line into an array splitt on spaces
        if len(line) == 2: #Only add the formatting arguments if it is the only thing on the line
            formatKeys["LW"] = int(line[1]) #Add arguments from the line to the dictionary
            #print(formatKeys)
            isCode = True

    if ".LS" in line: 
        line = line.split()
        if len(line) == 2:
            formatKeys["LS"] = int(line[1])
           # print(formatKeys)
            isCode = True

    ## START LM ARG CHECKER ##
    if ".LM" in line: #This block of code checks for if the arguments of LM are adding margin
        if "+" in line: #This block of code checks for if the arguments of LM are adding margin
            tempLine = line.replace('+',' ') # using a templine, because I want to perserve the original line for subsequent if statements
            tempLine = tempLine.split()
            formatKeys["LM"] += int(tempLine[1])
            #print(formatKeys)
            isCode = True

        if "-" in line: #This block of code checks for if the arguments of LM are subtracting margin
            tempLine2 = line.replace('-',' ') # using a templine, because I want to perserve the original line for subsequent if statements
            tempLine2 = tempLine2.split()
            formatKeys["LM"] -= int(tempLine2[1])
            #print(formatKeys)
            isCode = True

                        
        if "-" not in line and "+" not in line:
            line = line.split()
            if len(line) == 2:
                formatKeys["LM"] = int(line[1])
                #print(formatKeys)
                isCode = True
    ### END LM argument checker ###

    if ".FT off" in line: 
        line = line.split()
        if len(line) == 2:
            formatKeys["FT"] = "off"
            #print(formatKeys)
            isCode = True

    if ".FT on" in line:
        line = line.split()
        if len(line) == 2:
            formatKeys["FT"] = "on"
            #print(formatKeys)
            isCode = True
    
    return isCode

def format(line, firstWord, firstMargin):
    global formatKeys
    global charCount
    global withoutNewline

    if formatKeys["FT"] is "on": #ensures that formatting is on
        
        if firstMargin !=0:
            charCount = formatKeys["LM"]

        if line == '\n':
            print('\n')
            ls_printer(formatKeys["LS"])
            ls_printer(formatKeys["LS"])
            lm_printer(formatKeys["LM"]) #call this function to add appropriate line spacing after the newline
            charCount = formatKeys["LM"] #set the margin to the charcount because the margin is the only string on the line
            firstWord = True
            return firstWord

        else:
            line = line.strip()
            words = line.split()
            words

        for x in words:
            #Adds the length of the current word plus one for anticipated space
            charCount += len(x)+1

            #dont print a space if it is the first word of the file
            if firstWord:
                print(x, end="")
                charCount -=1 # Because there is no space printed
                firstWord = False
                continue

            # If char count exceeded the max allowed, print a newline, reset counter, add back the length because we are now on
            # a fresh line. Proceed to the next iteration
            if charCount > formatKeys["LW"]: 
                print()
                ls_printer(formatKeys["LS"])
                lm_printer(formatKeys["LM"]) #call this function to add appropriate line spacing after the newline
                charCount = formatKeys["LM"] #set the margin to the charcount because the margin is the only string on the line
                charCount += len(x) #Add the length of the line to be printed to the charcount
                print(x, end="")
                firstWord = False
                continue

            # If char count is at exactly the limit print out the word, and then print a newline. No space is added because it
            # is the end of the line    
            if charCount == formatKeys["LW"]:
                print(" {}".format(x))
                ls_printer(formatKeys["LS"]) # Print out appropriate linespacing
                lm_printer(formatKeys["LM"]) #call this function to add appropriate line spacing after the newline
                charCount = formatKeys["LM"] #set the margin to the charcount because the margin is the only string on the line
                firstWord = True
                continue

            # if both of the above cases fail then the word will be printed out with no newline and a pre-space   
            print(" {}".format(x), end="")
            firstWord = False
    
    else:
        for x in line:
            print(x, end="")
            
    return firstWord                
 

def lm_printer(lmArgs):
    if lmArgs > 0: 
        for y in range(lmArgs):
            print(" ", end="")
    else:
        return 

def ls_printer(lsArgs):
    if lsArgs > 0: 
        for y in range(lsArgs):
            print()
    else:
        return      


if __name__=='__main__':
        main()