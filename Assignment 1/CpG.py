# complete the program by writing your own code here

sequence = input("Enter a DNA sequence: ")
invalidSequence = False # setting up Boolean expression to account for exceptions
isMethylated = False
for index in range (0,len(sequence)) :
    if sequence[index] != "C" and sequence[index] != "G" and sequence[index] != "A" and sequence[index] != "T" : # accounting for inputs that are not nucleotides
        invalidSequence = True
        break # exit for loop if invalid input
if invalidSequence == True :
    print("Invalid sequence")
else :
    index = 0 # extract index
    while index < len(sequence) :
        if sequence[index : index + 2] == "CG" : # scanning for CpG islands
            isMethylated = True
            print("CpG site is detected at position", index, "of the sequence")
        index = index + 1 # update index
    if not isMethylated : # when Boolean is false
        print("No CpG site is detected in the input sequence.")