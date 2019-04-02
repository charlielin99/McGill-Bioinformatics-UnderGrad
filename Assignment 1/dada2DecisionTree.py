# complete the program by writing your own code here

def bodyTemperature () : # poses the body temp question
    bodyTemp = (input("Body temp (\u00B0C) "))
    try:
        bodyTemp = float(bodyTemp)
        if bodyTemp >= 38 : # poses pathogen mutation question
            ada2PathogenMutation = str(input("ADA2 pathogenic mutations (0 pathogenic mutation or 1 pathogenic mutation or 2 biallelic pathogenic mutation)? "))
            if ada2PathogenMutation == "0 pathogenic mutation":
                print("low-risk")
            elif ada2PathogenMutation == "1 pathogenic mutation":
                print("medium-risk")
            elif ada2PathogenMutation == "2 biallelic pathogenic mutation":
                print("high-risk")
            else:
                print("Invalid")            
        elif bodyTemp < 0 : # body temp cannot be lower so thus invalid input (theoretically lowest body temp recorded is 13\u00B0C)
            print("Invalid")
        elif bodyTemp < 38 and bodyTemp > 0 : # poses crp question
            crp = (input("CRP (mg/dL) "))
            try: # poses crp question and runs through conditionals
                crp = float(crp)
                if crp >= 5 : # poses pathogen mutation question
                    ada2PathogenMutation = str(input("ADA2 pathogenic mutations (0 pathogenic mutation or 1 pathogenic mutation or 2 biallelic pathogenic mutation)? "))
                    if ada2PathogenMutation == "0 pathogenic mutation":
                        print("low-risk")
                    elif ada2PathogenMutation == "1 pathogenic mutation":
                        print("medium-risk")
                    elif ada2PathogenMutation == "2 biallelicic pathogen mutation":
                        print("high-risk")
                    else:
                        print("Invalid")
                elif crp < 5 and crp > 0:
                    print("low-risk")
                elif crp < 0 or ValueError: # crp value cannot be negative
                    print("Invalid")
            except ValueError: # if value error occurs input is invalid
                print("Invalid")
    except ValueError:
        print("Invalid")
liveSkinRash = input("Livedoid skin rash (Yes or No)? ")
if liveSkinRash == "Yes" :
    bodyTemperature() # asks body temp question
elif liveSkinRash == "No" :
    neuroDisorder = input("Neurological disorder (Yes or No)? ")
    if neuroDisorder == "Yes" :
        bodyTemperature() # asks body temp question
    elif neuroDisorder == "No" :
        print("low-risk")
    else:
        print("Invalid")
else: # initial input is invalid
    print("Invalid")