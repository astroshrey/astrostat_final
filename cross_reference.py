#!/Users/Shrey/anaconda2/bin/python

#first, we read in the McQuillan data into a dictionary
mcq_file = "McQuillan_data/McQuillan.dat"
f = open(mcq_file, "r")

all_stars = {}
for line in f:
    data = line.split()
    all_stars[data[0]] = data[1:] + [0,0,0]
f.close()


#then, we create a dictionary of the Mathur data
math_file = "Mathur_data/Mathur.dat"
math_params = {}
g = open(math_file, "r")
for line in g:
    data = line.split()
    math_params[data[0]] = data[1:]
g.close()

#because we have dictionaries, we can look up key matches in O(1) time
#which allows for efficient cross-referencing
for key in all_stars:
    if math_params[key] is not None:
        #replacing Mcquillan data for Mathur data
        all_stars[key][0] = math_params[key][0] #Teff
        all_stars[key][1] = math_params[key][3] #logg
        all_stars[key][2] = math_params[key][9] #mass
        #adding the Mathur data for FeH, rad, and rho
        all_stars[key][10] = math_params[key][6] #FeH
        all_stars[key][11] = math_params[key][12] #rad
        all_stars[key][12] = math_params[key][15] #rho

#now we can structure this all in arrays and write back out
all_stars =[[key] + all_stars[key] for key in all_stars]

#writing out our cross-referenced text file
f = open("crossref.txt", 'w')
for arr in all_stars:
    for element in arr:
        f.write(element)
        f.write(' ')
    f.write('\n')
f.close()
