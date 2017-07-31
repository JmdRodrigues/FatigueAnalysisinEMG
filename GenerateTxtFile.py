def generateTxtFile (txt_data):
    # Txt file creation.
    file = open('txtReport.txt', mode='w')

    # Writing Phase.
    for i in range(0, len(txt_data)): # Access to the data of each line of txt file.
        for j in range(0, len(txt_data[i])): # Access to the data of each column of txt file.
            file.write(str(txt_data[i][j]))
            file.write('\t')
        file.write('\n')

    file.close()

# Provisional Version of 16th of July of 2017 :) *-* (: ª-ª