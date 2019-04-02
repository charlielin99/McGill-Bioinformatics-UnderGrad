# complete the program by writing your own code here

sequence = input("Enter a DNA sequence: ")
invalidSequence = False # set up Boolean expression used for printing
error = False # set up Boolean expression used for printing
compSequence = "" # creates empty variable
for index in range (0,len(sequence)) :
    if sequence[index] != "C" and sequence[index] != "G" and sequence[index] != "A" and sequence[index] != "T" : # stops program if invalid input
        error = True
        break # leave loop
if error == True :
    print("Invalid sequence")
else :
    for index in range (0,len(sequence)) : # adds nucleotides to compSequence based on Watson Crick base pairing
        if sequence[index] == "C" :
            compSequence = compSequence + "G"
        elif sequence[index] == "G" :
            compSequence = compSequence + "C"
        elif sequence[index] == "A" :
            compSequence = compSequence + "T"
        elif sequence[index] == "T" :
            compSequence = compSequence + "A"
    revSequence = compSequence[::-1] # reverse string
    index = 0 # extract index
    while index < len(sequence) :
        if sequence[index] == revSequence[index] : # looking for identical nucleotides to determine if palindromic
            index = index + 1 # update index
            invalidSequence = False
        else :
            invalidSequence = True
            print(sequence, "is not a palindromic sequence")
            break # leave loop
    if invalidSequence == False :
        print(sequence, "is a palindromic sequence")