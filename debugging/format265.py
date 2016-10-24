#!/usr/bin/env

import sys
import fileinput


formatKeys = {"LW": 0, "LM": 0, "LS": 0, "FT": "on"}
charCount = 0
#noNewline = False
setNewParaflg = False
newlinesInaRow = False
lastLs = formatKeys["LS"]
def main():
        global noNewline
        line = 0
        firstWord = True
        firstWordWithMargin = True
        firstMargin = 0
        lastline = is_last_newline() #Get the length of the file
        idx = 0 # Keep track of the current length of the file
        filesFirstWord = 0 # Keep track of the file's very first word, and print margin for it

        for line in fileinput.input():
            idx+=1 #Increment to the current index in the file

            if(set_args(line)): # Only evaluate this if there was an argument processed

                if firstWordWithMargin and formatKeys["LM"] > 0 and filesFirstWord == 0: # For adding margin to the first line

                    lm_printer(formatKeys["LM"])
                    firstMargin = formatKeys["LM"]
                    firstWordWithMargin = False
                    
                continue
            firstWord = format(line, firstWord, firstMargin, idx, lastline) #Set the truth value of format's return value to firstWord
            firstMargin = 0 
            filesFirstWord = 1
        if "on" in formatKeys["FT"]: 
        #if not noNewline: #Only print a new line if FT is off
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
            isCode = True

        if "-" in line: #This block of code checks for if the arguments of LM are subtracting margin
            tempLine2 = line.replace('-',' ') # using a templine, because I want to perserve the original line for subsequent if statements
            tempLine2 = tempLine2.split()
            formatKeys["LM"] -= int(tempLine2[1])
            isCode = True

                        
        if "-" not in line and "+" not in line:
            line = line.split()
            if len(line) == 2:
                #print("I JUST DID AN LM A REGULAR LM: Formatkeys: {}".format(formatKeys["LM"]))
                formatKeys["LM"] = int(line[1])
                #print("I JUST DID AN LM A REGULAR LM: Formatkeys: {}".format(formatKeys["LM"]))
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

def format(line, firstWord, firstMargin, idx, lastline):
    global formatKeys
    global charCount
    global noNewline
    global setNewParaflg 
    global newlinesInaRow
    global lastLs

    if formatKeys["FT"] is "on": #ensures that formatting is on
        
        if firstMargin !=0:
            charCount = formatKeys["LM"]

        if line == '\n':

            if newlinesInaRow: # this if will be evaluated true when there are two or more newlines in the file
                print()
                setNewParaflg = True
                firstWord = True
                return firstWord

            newlinesInaRow = True # This signals that the last line was a newline, and if another newline occurs, only one line will be printed
            
            if idx != lastline: # The only case where this will not be printed is if the last line is a newline. This is to preserve the bottom of the file
                print()

            print()
            setNewParaflg = True
            firstWord = True
            return firstWord

        else: #Evaluated if the line is anything but a newline
            newlinesInaRow = False
            #line = line.strip()
            words = line.split()
            words

        for x in words:
            #Adds the length of the current word plus one for anticipated space
            charCount += len(x)

            #dont print a space if it is the first word of the file
            if firstWord:
                if lastLs != formatKeys["LS"]:
                    ls_printer(lastLs)
                    ls_printer(lastLs)
                    lastLs = formatKeys["LS"]
                    lm_printer(formatKeys["LM"])
                    charCount = formatKeys["LM"]
                    print(x, end="")
                    charCount += len(x)
                    firstWord = False
                    continue

                if setNewParaflg:
                    ls_printer(formatKeys["LS"])
                    ls_printer(formatKeys["LS"])
                    lm_printer(formatKeys["LM"])
                    charCount = formatKeys["LM"]
                    charCount += len(x)
                    setNewParaflg = False

                print(x, end="")
                firstWord = False
                continue

            # If char count exceeded the max allowed, print a newline, reset counter, add back the length because we are now on
            # a fresh line. Proceed to the next iteration
            if charCount+1 > formatKeys["LW"]: 
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
            charCount +=1
    
    else:
        for x in line:
            print(x, end="")
        #noNewline = True
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

def is_last_newline():
    index = 0

    for line in fileinput.input():
        lastline = line
        index +=1

    if lastline == '\n':
        #print("INDEX OF LAST LINE, and its a newline: {}".format(idx))
        return index  

    else:
        return 0

if __name__=='__main__':
        main()