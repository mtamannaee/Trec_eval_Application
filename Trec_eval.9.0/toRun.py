import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import math
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
import os
import shutil
from tabulate import tabulate
import pyperclip
import clipboard

app = tk.Tk()


runfilenames=[]                                             #   TREC    #    +   #   Tab 1 :  Plot Type 1   #
numberRunfiles = tk.IntVar(app,tk.NONE)                     #   TREC    #    +   #   Tab 1 :  Plot Type 1   #
dirRel = tk.StringVar(app,tk.NONE)                          #   TREC    #
relfilename=tk.StringVar(app,tk.NONE)                       #   TREC    #
currentDir = tk.StringVar(app,tk.NONE)                      #   TREC    #
resultfilenames=[]                                          #   TREC    #    +   #   Tab 1 :  Plot Type 1   #

BBLnames_initOptions=("TREC Files",'--------------------')      #   Tab1    and     Tab2     : initial options for best and base baselines Optionmenu  #
BBLnames_TRECfilesOptions=()

bestBLfilename_P1=tk.StringVar(app,tk.NONE)                 #   Tab 1    :   Plot Type 1   best baseline  #         GLOBAL
meas_P1 = tk.StringVar(app, tk.NONE)                        #   Tab 1    :   Plot Type 1                  #         GLOBAL
baseBLfilename_P1 = tk.StringVar(app,tk.NONE)               #   Tab 1    :   Plot Type 2   base baseline #
Pcent_seq = tk.StringVar(app,tk.NONE)                       #   Tab 1    :   Plot Type 2                 #
allQ_ranked=[]                                              #   Tab 1    :   Plot Type 2   :   ranked queries based on IR MEAS value of baseBL     #         GLOBAL V      #

bestBLfilename_P2=tk.StringVar(app,tk.NONE)                 #   Tab 2    :   Plot Type 1    #         GLOBAL        #
baseBLfilename_P2=tk.StringVar(app,tk.NONE)                 #   Tab 2    :   Plot Type 1    #         GLOBAL
meas_P2 = tk.StringVar(app, tk.NONE)                        #   Tab 2    :   Plot Type 1    #
hardRange=tk.StringVar(app, tk.NONE)
hardQ=[]
hardQ_ranked=[]
Pcent_seq_P2 = tk.StringVar(app,tk.NONE)                    #   Tab 2    :   Plot Type 2    #




#       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #       #       Functions         #


def bestMenu_P1(value):
    global bestBLfilename_P1
    bestBLfilename_P1= bestBLfilename_P11.get()     #print(bestBLfilename_P1)
    bestBLmenu_P1.configure(fg="blue", width=8)
    plotTypeOneButton.configure(state="active")


def baseMenu_P1(value):
    global baseBLfilename_P1
    baseBLfilename_P1=baseBLfilename_P11.get()      #print(baseBLfilename_P1)
    baseBLmenu_p1.configure(fg="blue", width=8)
    plot2.configure(state="active")

def bestMenu_P2(value):
    global bestBLfilename_P2
    bestBLfilename_P2=bestBLfilename_P22.get()
    bestBLmenu_P2.configure(fg="blue", width=8)
    plot3.configure(state="active")
    print(bestBLfilename_P2)


def baseMenu_P2(value):
    global baseBLfilename_P2
    baseBLfilename_P2=baseBLfilename_P22.get()
    baseBLmenu_p2.configure(fg="blue", width=8)
    plot4.configure(state="active")                 #print(baseBLfilename_P2)

def showmeas1():
    with open("majorMeas.txt", "r") as f:
        new1 = tk.Tk()
        tk.Label(new1, text=f.read()).pack()
        new1.mainloop()


def runfileUpload():  # TREC    #
    global numberRunfiles
    global currentDir
    global resultfilenames
    global runfilenames

    srcDir = filedialog.askdirectory()
    currentDir = os.getcwd()

    dirFiles = os.listdir(srcDir)
    for file_name in dirFiles:
        if file_name.endswith('.adhoc'):
            full_file_name = os.path.join(srcDir, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, currentDir)

    for i in range(dirFiles.__len__()):
        if dirFiles[i].split(".")[1] == "adhoc":
            runfilenames.append(dirFiles[i])
            resultfilenames.append(dirFiles[i].split(".")[0] + "-TREC.txt")

    numberRunfiles = runfilenames.__len__()
    textString = ""
    for i in range(numberRunfiles):
        textString = textString + "{}\n".format(runfilenames[i])
    fileBrifLable.config(text=textString)



    print(runfilenames)
    print(resultfilenames)
    print(numberRunfiles)
    print(srcDir)


def relfileUpload():                            #   TREC    #
    global currentDir
    global dirRel
    global relfilename
    currentDir = os.getcwd()
    dirRel = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=( ("all files", "*.*"),("adhoc files", "*.ahdoc"),("text files", "*.txt")))
    relfilename = str(dirRel).split("/")[-1]
    shutil.copy(r'{}'.format(dirRel), currentDir)
    print("{} is seleceted to be uploaded.".format(relfilename))
    relBrifLable.config(text=relfilename)
    uploadRelButton.config(state="disabled")
    if str(uploadRelButton["state"])=="disabled":
        runTrecButton.config(state= "active")
        currentDirEntryVar.set(currentDir)

def runTrec():                                  #   TREC    #
    # PART A : RUNNING THE TREC EVAL .C CODE #
    print("Trec is running")
    global numberRunfiles
    global resultfilenames
    global runfilenames
    global relfilename

    commandlist = []
    commandTemp = './trec_eval -q  {} {} >> {}'

    textString2 = ""
    for x in range(numberRunfiles):
        commandlist.append(commandTemp.format(relfilename, runfilenames[x], resultfilenames[x]))

    for y in range(numberRunfiles):
        os.system(commandlist[y])
        textString2 = textString2 + "{}\n".format(resultfilenames[y])  # print(commandlist)

    # PART B : CONFIGURATION and INITIALAZATION #
    resultBrifLable.config(text=textString2)

    global BBLnames_TRECfilesOptions
    BBLnames_TRECfilesOptions = tuple(resultfilenames)

    bestBLmenu_P1['menu'].delete(2, 'end')
    bestBLmenu_P1.configure(state="active")

    baseBLmenu_p1['menu'].delete(2, 'end')
    baseBLmenu_p1.configure(state="active")

    bestBLmenu_P2['menu'].delete(2, 'end')
    bestBLmenu_P2.configure(state="active")

    baseBLmenu_p2['menu'].delete(2, 'end')
    baseBLmenu_p2.configure(state="active")

    for choice in BBLnames_TRECfilesOptions:
        bestBLmenu_P1['menu'].add_command(label=choice, command=tk._setit(bestBLfilename_P11, choice, bestMenu_P1))
        baseBLmenu_p1['menu'].add_command(label=choice, command=tk._setit(baseBLfilename_P11, choice, baseMenu_P1))
        bestBLmenu_P2['menu'].add_command(label=choice, command=tk._setit(bestBLfilename_P22, choice, bestMenu_P2))
        baseBLmenu_p2['menu'].add_command(label=choice, command=tk._setit(baseBLfilename_P22, choice, baseMenu_P2))
    print("Trec is done")


############################################################################################################################################################################################################################################################################################




############################################################################################################################################################################################################################################################################################

def irMeas_P1(value):                               #   Tab 1    :   Plot Type 1    #
    global meas_P1
    meas_P1 = measVar1.get()    #print(meas_P1)
    measMenu_P1.configure(fg="blue")

    plotTypeOneButton.config(state="active")
    plot2.configure(state="active")

############################################################################################################################################################################################################################################################################################

def irMeas_P2(value):                               #   Tab 2    :   Plot Type 2    #
    global meas_P2
    meas_P2 = measVar2.get()    #print(meas_P2)
    measMenu_P2.configure(fg="blue")
    findHardQueriesButton.configure(state="active")
    plot4.configure(state="active")
    plot3.configure(state="active")

############################################################################################################################################################################################################################################################################################


def plot1():                # pictures of the graphs : {}-PlotALL.png #
    print("plot type1")
    global bestBLfilename_P1
    global numberRunfiles   # from TREC #
    global resultfilenames  # from TREC #
    global meas_P1

    bLines = []
    bqueries = []

    with open(str(bestBLfilename_P1), "r") as bf:
        ballLines = bf.readlines()
        for bl in ballLines:
            if bl.split()[1] != "all" and bl.split()[0] == meas_P1:
                bqueries.append(bl.split()[1])
                bLines.append([bl.split()[1], bl.split()[2]])   #
                # print(bqueries)
    for x in range(numberRunfiles):
        with open(str(resultfilenames[x]), "r") as rf:
            diflines = []
            allLines = rf.readlines()
            for l in allLines:
                if l.split()[1] != "all" and l.split()[0] == meas_P1 and l.split()[1] in bqueries:
                    bindex = bqueries.index(l.split()[1])
                    diffrance = float(bLines[bindex][1]) - float(l.split()[2])
                    diflines.append([l.split()[1], diffrance])
            print(str(resultfilenames[x]))
            yz_setlistdict = dict(diflines)
            sorteddict_yz = OrderedDict(sorted(list(yz_setlistdict.items()), key=operator.itemgetter(1), reverse=True))

            fig = plt.figure(figsize=(12, 5.7))
            width=1
            plt.bar(list(range(len(list(sorteddict_yz.keys())))), list(sorteddict_yz.values()),width)
            plt.xticks(list(range(len(list(sorteddict_yz.keys())))), list(sorteddict_yz.keys()))
            plt.title("All Queries Representation \n \n{} : {} topics \n".format(str(resultfilenames[x]), diflines.__len__()))
            plt.ylabel(r'$\Delta$' + meas_P1 + "\n")
            plt.gca().axes.get_xaxis().set_visible(False)
            fig.savefig("{}-ALL.png".format(str(resultfilenames[x])), pad_inches=0.5)

############################################################################################################################################################################################################################################################################################

def Plot2():    # pictures of the graphs : {}-ALL%.png #
    print("plot 2 - All Queries %")
    global allQ_ranked
    global baseBLfilename_P1
    global meas_P1
    global resultfilenames
    global Pcent_seq
    global numberRunfiles
    global allQ_ranked

    Pcent_seq=Pcent_seq_l.get()
    with open('{}'.format(baseBLfilename_P1), "r")as fBase:
        yz_rankBaseBB = []
        baseBLlines = fBase.readlines()
        sorteddict = OrderedDict()
        for l in baseBLlines:
            if l.split()[0] == meas_P1 and l.split()[1] != 'all':
                yz_rankBaseBB.append((l.split()[1], l.split()[2]))
        sorteddict = OrderedDict(sorted(list(dict((list(set(yz_rankBaseBB)))).items()), key=operator.itemgetter(1),
                                        reverse=True))  # print(sorteddict)
        allQ_ranked = list(sorteddict)  # print(allQ_ranked)
    fBase.close()

    print("Packing with diffrent percentages is running")

    percentages = list(map(int, Pcent_seq.split(',')))
    Pack_C = percentages.__len__()
    totalQueryCount = allQ_ranked.__len__()

    packQueryCountList = []
    indxList = []

    counter = percentages.__len__()
    for i in percentages:
        factor = float(i) / 100.00
        packQueryCountList.append((percentages.__len__() - counter, int(totalQueryCount * factor)))
        counter -= 1
    print(("Packs : {}".format(packQueryCountList)))
    print("Total Number of Queris : {}".format(totalQueryCount))

    tuple_c = packQueryCountList.__len__() - 1  # print(tuple_c) : 3
    # indxList = []
    indxList.append(0)

    for item in packQueryCountList:
        #   print item[0] : 0,1,2,3
        #   print item[1] : 15,15,76,30

        #   index for the first tuple(i,j)= j = second number in the tuple
        if int(item[0]) == 0:
            indxList.append(item[1])
            # print item[0] : 0

        #   index for the first tuple(i,j)= j = second number in the tuple
        elif int(item[0]) == tuple_c:
            indxList.append(totalQueryCount)  # print item[0] : 3

        elif 0 <= int(item[0]) or int(item[0]) <= tuple_c:
            indx1 = item[0]  # print indx1 : 1, 2
            l2 = []
            l2_values = ()  # [(0, 15)] and [(0, 15), (1, 15)]
            for x in range(int(item[0]) + 1):
                l2.append(packQueryCountList[x])

            l2_values = list(zip(*l2))[1]   # print (l2_values) : (15,) and (15, 15)
            sum = 0
            for i in l2_values:
                sum = sum + int(i)
            # print sum
            indxList.append(sum)            #print(("Indexes :{}".format(indxList)))

    rankQpacksList = []     # [[int, [..]],[int,[]],..] : [[int,[indexes]],[int,[querynumber]]]   :   [[0, [...]], [1, [...]], [2, [...]], [3, [...]]]
    rankQPack2 = []         # [[],[],..]  :[[packnumber, querynumber],[],..]  :   [[0, '108'], [0, '142'], ..., [1, '117'], [1, '141'], .., [2, '119'], [2, '118'], .., [3, '110'], [3, '122'],..]
    for i in range(indxList.__len__() - 1):
        first_q_index = indxList[i]                         # print(start_indx)
        last_q_index = indxList[i + 1]                      # print(end_index)
        rankQPack = []
        for l_indx in range(first_q_index, last_q_index):
            rankQPack.append(allQ_ranked[l_indx])
            rankQPack2.append([i, allQ_ranked[l_indx]])     # print(rankQPack)
        rankQpacksList.append(rankQPack)
    #print(rankQpacksList)

    # print(rankQpacksList)      #   print(rankQPack2)

    print("Packing with diffrent percentages is done")      # rankQpacksLis[]
    packsAvrgList = []
    for pack in rankQpacksList:
        packNum = rankQpacksList.index(pack)
        for i in range(numberRunfiles):
            with open("{}".format(resultfilenames[i]), 'r') as rf:
                lines = rf.readlines()
                sum_val = 0.0000
                avg_val = 0.0000
                count = 0
                for q in pack:
                    for l in lines:
                        if l.split()[1] == str(q) and l.split()[0] == meas_P1 and l.split()[1] != "all":
                            sum_val = math.fsum([float(sum_val), float(l.split()[2])])
                            count = count + 1
                avg_val = sum_val / count
                name= str(runfilenames[i]).split('.')[0]
                packsAvrgList.append([packNum,name, avg_val])
        packsAvrgList.append([packNum, " ", 0.0])

    sorteeed = sorted(packsAvrgList, key=operator.itemgetter(0))
    op_av = [(x[1], float(x[2])) for x in sorteeed]

    fig = plt.figure(figsize=(12, 6))
    labels, ys = list(zip(*op_av))
    xs = np.arange(len(labels))
    width = 0.95

    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=70, fontsize=8)
    plt.title("All Queries Representation %")
    plt.savefig('{}-ALL%.png'.format(meas_P1), pad_inches=0.5)


############################################################################################################################################################################################################################################################################################


def plot3():    # pictures of the graphs : {}-Hard.png #
    global hardQ
    global hardQ_ranked
    global resultfilenames
    global runfilenames
    global numberRunfiles
    global hardRangeuperbound
    global bestBLfilename_P2
    global baseBLfilename_P2
    global meas_P2

    hardQ_val = []
    hardRangeuperbound=hardRRange.get()
    #  finding hard queries based on selected  output
    with open("{}".format(baseBLfilename_P2), "r")as f:
        lines = f.readlines()
        with open('S-HQ{}.txt'.format(meas_P2), "w") as HQ:
            HardQ_counter = 0
            for l in lines:
                if l.split()[1] != 'all' and str(l.split()[0]) == meas_P2 and float(l.split()[2]) <= float(hardRangeuperbound):
                    HQ.writelines("{}                   	{}\n".format('HQ-baseline:{}'.format(baseBLfilename_P2),
                                                                         l.split()[1]))
                    hardQ.append(l.split()[1])
                    hardQ_val.append((l.split()[1], float(l.split()[2])))

        HQ.close()
    f.close()

    sorteddict1 = OrderedDict(sorted(list(dict((list(set(hardQ_val)))).items()), key=operator.itemgetter(1),
                                    reverse=True))  # print(sorteddict)
    hardQ_ranked = list(sorteddict1)                # print(allQ_ranked)

    print("the function of Hard Queries values of All Runs vs Best is running ")
    lineTemp1 = '{}                   	{}	{}\n'
    lineTemp0 = '{}                   	{}\n'
    print(bestBLfilename_P2)
    with open("{}".format(bestBLfilename_P2), "r")as fBestH:
        with open('S-HQ{}.txt'.format(meas_P2), "r") as HQ:
            with open('BHQ-{}.txt'.format(meas_P2), "w") as BHQ:
                Blines = fBestH.readlines()
                HQlines = HQ.readlines()

                for Bline in Blines:
                    for HQline in HQlines:
                        if Bline.split()[1] != "all" and Bline.split()[0] == meas_P2 and Bline.split()[1] == \
                                HQline.split()[1]:
                            BHQ.writelines(lineTemp0.format(HQline.split()[1], float(Bline.split()[2])))
            BHQ.close()
        HQ.close()
    fBestH.close()
    print("BHQ file is created. ")
    # finding values of measurement of drived hard queries based on selected output and their value diffrence comparing with best output
    with open('BHQ-{}.txt'.format(meas_P2), "r") as BHQ:
        BHQlines = BHQ.readlines()
        for x in range(numberRunfiles):
            if bestBLfilename_P2 != resultfilenames[x]:
                with open('{}'.format(resultfilenames[x]), "r") as fx:
                    with open('H-{}-output{}'.format(meas_P2, x), "w") as fOutHQx:
                        fxlines = fx.readlines()
                        for fxline in fxlines:
                            for BHQline in BHQlines:
                                if fxline.split()[1] != 'all' and fxline.split()[0] == meas_P2 and fxline.split()[1] == BHQline.split()[0]:
                                    hard_val_diff = str(float(BHQline.split()[1]) - float(fxline.split()[2]))
                                    fOutHQx.writelines(
                                        lineTemp1.format(BHQline.split()[0], fxline.split()[2], hard_val_diff))
                    fOutHQx.close()
                fx.close()
        BHQ.close()

    for x in range(numberRunfiles):
        if resultfilenames[x] != bestBLfilename_P2:
            with open('H-{}-output{}'.format(meas_P2, x), "r") as fHard:
                hqd = []
                fHardlines = fHard.readlines()
                for fhline in fHardlines:
                    hqd.append((fhline.split()[0], float(fhline.split()[2])))

                hqd_dict = dict(list(set(hqd)))
                sorteddict_hqd = OrderedDict(sorted(list(hqd_dict.items()), key=operator.itemgetter(1), reverse=True))
                # sorteddict_yz_1 = OrderedDict(sorted(yz_dict.items(), key=lambda t: t[1], reverse=True))

                fig1 = plt.figure(figsize=(12, 5.7))
                width=0.95
                plt.bar(list(range(len(list(sorteddict_hqd.keys())))), list(sorteddict_hqd.values()),width, align='center')
                plt.xticks(list(range(len(list(sorteddict_hqd.keys())))), list(sorteddict_hqd.keys()))
                plt.xlabel("{}".format(resultfilenames[x]))
                plt.ylabel(r'$\Delta$' + meas_P2)
                #plt.show()
                graph_name='{}-Hard-{}.png'.format( resultfilenames[x],meas_P2)
                plt.savefig(graph_name, pad_inches=0.5)
                print("PLOT TYPE 3 :    The graph is saved in the directory under the following name : {}".format(graph_name))
            fHard.close()

############################################################################################################################################################################################################################################################################################

def plot4():    # pictures of the graphs : {}-Hard%.png #

    global Pcent_seq_P2
    global hardQ
    global hardQ_ranked
    global resultfilenames
    global runfilenames
    global numberRunfiles
    global hardRangeuperbound
    global bestBLfilename_P2
    global baseBLfilename_P2
    global meas_P2

    hardQ_val = []
    hardRangeuperbound=hardRRange.get()
    #  finding hard queries based on selected  output
    with open("{}".format(baseBLfilename_P2), "r")as f:
        lines = f.readlines()
        with open('S-HQ{}.txt'.format(meas_P2), "w") as HQ:
            HardQ_counter = 0
            for l in lines:
                if l.split()[1] != 'all' and str(l.split()[0]) == meas_P2 and float(l.split()[2]) <= float(hardRangeuperbound):
                    HQ.writelines("{}                   	{}\n".format('HQ-baseline:{}'.format(baseBLfilename_P2),
                                                                         l.split()[1]))
                    hardQ.append(l.split()[1])
                    hardQ_val.append((l.split()[1], float(l.split()[2])))

        HQ.close()
    f.close()

    sorteddict1 = OrderedDict(sorted(list(dict((list(set(hardQ_val)))).items()), key=operator.itemgetter(1),
                                    reverse=True))  # print(sorteddict)
    hardQ_ranked = list(sorteddict1)                # print(allQ_ranked)

    Pcent_seq_P2=Pcent_seq_l2.get()

    percentages = list(map(int, Pcent_seq_P2.split(',')))
    Pack_C = percentages.__len__()
    totalQueryCount = hardQ_ranked.__len__()

    packQueryCountList = []
    indxList = []

    counter = percentages.__len__()
    for i in percentages:
        factor = float(i) / 100.00
        packQueryCountList.append((percentages.__len__() - counter, int(totalQueryCount * factor)))
        counter -= 1
    #print(("Packs : {}".format(packQueryCountList)))
    print("Total Number of Queris : {}".format(totalQueryCount))

    tuple_c = packQueryCountList.__len__() - 1  #   print(tuple_c) : 3
    # indxList = []
    indxList.append(0)

    for item in packQueryCountList:
        #   print item[0] : 0,1,2,3             #   print item[1] : 15,15,76,30

        #   index for the first tuple(i,j)= j = second number in the tuple
        if int(item[0]) == 0:
            indxList.append(item[1])            #   print item[0] : 0

        #   index for the first tuple(i,j)= j = second number in the tuple
        elif int(item[0]) == tuple_c:
            indxList.append(totalQueryCount)    #   print item[0] : 3

        elif 0 <= int(item[0]) or int(item[0]) <= tuple_c:
            indx1 = item[0]                     #   print indx1 : 1, 2
            l2 = []
            l2_values = ()  # [(0, 15)] and [(0, 15), (1, 15)]
            for x in range(int(item[0]) + 1):
                l2.append(packQueryCountList[x])

            l2_values = list(zip(*l2))[1]       #   print (l2_values) : (15,) and (15, 15)
            sum = 0
            for i in l2_values:
                sum = sum + int(i)
            #   print sum
            indxList.append(sum)
    #   print(("Indexes :{}".format(indxList)))

    rankQpacksList = []  # [[int, [..]],[int,[]],..] : [[int,[indexes]],[int,[querynumber]]]   :   [[0, [...]], [1, [...]], [2, [...]], [3, [...]]]
    rankQPack2 = []  # [[],[],..]  :[[packnumber, querynumber],[],..]  :   [[0, '108'], [0, '142'], ..., [1, '117'], [1, '141'], .., [2, '119'], [2, '118'], .., [3, '110'], [3, '122'],..]
    for i in range(indxList.__len__() - 1):
        first_q_index = indxList[i]             #    print(start_indx)
        last_q_index = indxList[i + 1]          #   print(end_index)
        rankQPack = []
        for l_indx in range(first_q_index, last_q_index):
            rankQPack.append(hardQ_ranked[l_indx])
            rankQPack2.append([i, hardQ_ranked[l_indx]])
        # print(rankQPack)
        rankQpacksList.append(rankQPack)
    #print(rankQpacksList)

    # print(rankQpacksList)      #   print(rankQPack2)
    #print("PLOT TYPE 4 :    Packing with diffrent percentages is done")
    # rankQpacksLis[]
    packsAvrgList = []
    for pack in rankQpacksList:
        packNum = rankQpacksList.index(pack)
        for i in range(numberRunfiles):
            with open("{}".format(resultfilenames[i]), 'r') as rf:
                lines = rf.readlines()
                sum_val = 0.0000
                avg_val = 0.0000
                count = 0
                for q in pack:
                    for l in lines:
                        if l.split()[1] == str(q) and l.split()[0] == meas_P2 and l.split()[1] != "all":
                            sum_val = math.fsum([float(sum_val), float(l.split()[2])])
                            count = count + 1
                avg_val = sum_val / count
                name= str(runfilenames[i]).split('.')[0]
                packsAvrgList.append([packNum,name, avg_val])
        packsAvrgList.append([packNum, " ", 0.0])

    sorteeed = sorted(packsAvrgList, key=operator.itemgetter(0))
    op_av = [(x[1], float(x[2])) for x in sorteeed]

    fig = plt.figure(figsize=(12, 6))
    labels, ys = list(zip(*op_av))
    xs = np.arange(len(labels))
    width = 0.95

    plt.title("Hard Queries Representation %")
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=70, fontsize=8)
    # plt.yticks(ys) --> to get more precise values for y axis
    # plt.gca().axes.get_yaxis().set_visible(False) --> to eliminat the values on y axis
    #plt.show()
    graph_name= '{}-Hard%.png'.format(meas_P2)
    plt.savefig(graph_name, pad_inches=0.5)
    print("PLOT TYPE 4 :    The graph is saved in the directory under the following name : {}".format(graph_name))

###       LATEX   FUNCTIONS : { latex1, latex2 }       ###


def latex1():
    global resultfilenames  # from TREC #
    global meas_P1
    global numberRunfiles
    global runfilenames
    global bestBLfilename_P1

    print("latex1 is Running")
    fname_avg = []
    for i in range(numberRunfiles):
        with open("{}".format(resultfilenames[i]), "r")as f:
            lines = f.readlines()
            values = []
            for l in lines:
                if l.split()[0] == meas_P1 and l.split()[1] != "all":
                    values.append(float(l.split()[2]))
            suM = sum(values)
            avG = suM / values.__len__()
            fname_avg.append((resultfilenames[i], avG))
        f.close()

    h = []
    h.append("      ")
    h.append("All Queries ({})".format(meas_P1))

    allLAX = tabulate(fname_avg, headers=h, tablefmt='latex')
    #pyperclip.copy(allLAX)
    #app.clipboard_clear()
    #app.clipboard_append(str(allLAX))
    #command = 'echo ' + allLAX.strip() + '| clip'
    #os.system(command)
    #os.system("echo '%s' | pbcopy" % allLAX)
    #clipboard.copy(allLAX)
    app.clipboard_clear()
    app.clipboard_append(allLAX)
    print(allLAX)
    print("latex1 is Done")


def latex2():
    global resultfilenames  # from TREC #
    global meas_P2
    global numberRunfiles
    global runfilenames
    global hardQ
    print("latex2 is Running")
    fname_avg = []
    for i in range(numberRunfiles):
        with open("{}".format(resultfilenames[i]), "r")as f:
            lines = f.readlines()
            values = []
            for l in lines:
                if l.split()[0] == meas_P2 and l.split()[1] != "all" and l.split()[1] in hardQ:
                    values.append(float(l.split()[2]))
            suM = sum(values)
            avG = suM / values.__len__()
            fname_avg.append((runfilenames[i], avG))
        f.close()

    print(fname_avg)
    h = []
    h.append("      ")
    h.append("Hard Queries ({})".format(meas_P2))

    hardLAX = tabulate(fname_avg, headers=h, tablefmt='latex')
    #app.clipboard_clear()
    #app.clipboard_append(str(hardLAX))
    #command = 'echo ' + hardLAX.strip() + '| clip'
    #os.system(command)
    #os.system("echo '%s' | pbcopy" % hardLAX)
    #clipboard.copy(hardLAX)
    app.clipboard_clear()
    app.clipboard_append(hardLAX)
    print(hardLAX)
    print("latex2 is Done")


#         END   Functions         #       #       END   Functions         #       #       END   Functions         #       #       END   Functions         #       #       END   Functions         #       #       END   Functions         #









#       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #       #       GUI         #


#   main schema of GUI  #
app.geometry('770x880')
mainFrame= tk.Frame(app,bd=5,padx=2,pady=2, relief="ridge")
mainFrame.grid(row=1,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")

#   Frame (mainFrame) : {Label(x1), topFrame, botFrame, latexFrame}  #
tk.Label(mainFrame, text= "Welcome to The Trec Eval Application", font=(None, 15, "bold")).grid(row=0,columnspan=2,padx=10,pady=10,sticky="nwes")

topFrame= tk.Frame(mainFrame,bd=2,padx=5,pady=5, relief="sunken")
topFrame.grid(row=1,padx=5,pady=5,ipadx=2,ipady=2,sticky="nwes")
botFrame= tk.Frame(mainFrame,bd=2,padx=5,pady=5,relief="sunken")
botFrame.grid(row=2,padx=5,pady=5, ipadx=2,ipady=2, sticky="nwes")


#   Frame (topFrame) :  {leftTopFrame}  #
leftTopFrame=tk.Frame(topFrame,bd=2,padx=2,pady=2, relief="sunken")
leftTopFrame.grid(row=0,padx=2,pady=2,ipadx=2,ipady=2, sticky="nwes")

#   Frame (leftTopFrame) :  Trec :{ ..}    #
tk.Label(leftTopFrame, text="TREC", bd=2,padx=2,pady=2, font=(None, 11,"bold"), fg="maroon").grid(row=0,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="w")
tk.Label(leftTopFrame, text="Run Files :", bd=2,padx=2,pady=2, font=(None, 9)).grid(row=1,column=0,padx=2,pady=2, ipadx=2,ipady=2,sticky="w")
tk.Label(leftTopFrame, text="Relevance File :", bd=2,padx=2,pady=2, font=(None, 9)).grid(row=2,column=0,padx=2,pady=2, ipadx=2,ipady=2,sticky="w")

uploadRunButton = tk.Button(leftTopFrame, text="Upload ", command=runfileUpload,font=(None, 9),width=10)
uploadRunButton.grid(row=1, column=1, padx=2, pady=2,ipadx=2,ipady=2)
fileBrifLable = tk.Label(leftTopFrame, text="", fg="blue", font=(None, 9))
fileBrifLable.grid(row=1, column=2, padx=2, pady=2,ipadx=2,ipady=2)


uploadRelButton = tk.Button(leftTopFrame, text="Upload ", command=relfileUpload, font=(None, 9),width=10)
uploadRelButton.grid(row=2, column=1, padx=2, pady=2,ipadx=2,ipady=2)
relBrifLable = tk.Label(leftTopFrame, text="", fg="blue", font=(None, 9))
relBrifLable.grid(row=2, column=2, padx=2, pady=2,ipadx=2,ipady=2)

runTrecButton = tk.Button(leftTopFrame, text="Run Trec", command=runTrec, font=(None, 9), state="disabled",width=25)
runTrecButton.grid(row=3, column=2, padx=2, pady=2,ipadx=2,ipady=2, sticky='w')

tk.Label(leftTopFrame, text="TREC Result Files", bd=2,padx=2,pady=2, font=(None, 11,"bold"), fg="maroon").grid(row=0,column=3,padx=2,pady=2,sticky="w")

currentDirEntryVar=tk.StringVar(leftTopFrame)
tk.Label(leftTopFrame, textvariable=currentDirEntryVar, fg="dim gray", font=(None, 9)).grid(row=0, column=4,columnspan=2, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

resultBrifLable = tk.Label(leftTopFrame, text=" ", fg="blue", font=(None, 9))
resultBrifLable.grid(row=1, column=3,columnspan=2,rowspan=2, padx=2, pady=2,ipadx=2,ipady=2,sticky='N')



#   Frame (botFrame) : {Label(x1), Notebook (tabControl)   }  #
tk.Label(botFrame, text="Plot", font=(None, 11,'bold'),fg="maroon").grid(row=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="N")
tabControl = ttk.Notebook(botFrame, padding='0.02i')


#   Notebook (tabControl) : {tab1, tab2}  #
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='  All Queries  ')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='  Hard Queries  ')


#   Frame(tab1) : {tab1TopFrame,tab1ButFrame}  #
tab1TopFrame= tk.Frame(tab1,bd=2,padx=2,pady=2, relief="sunken")
tab1TopFrame.grid(row=1,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")
tab1ButFrame= tk.Frame(tab1,bd=2,padx=2,pady=2, relief="sunken")
tab1ButFrame.grid(row=2,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")


#   Frame(tab1TopFrame) : {...}  #
tk.Label(tab1, text="All Queries Relative Representation ", font=(None, 11,'bold'),fg="maroon").grid(row=0,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="ew")
tk.Label(tab1TopFrame, text="Plot Definition :  Plotting all queries improvement of selected IR measurement value on all queries over the best baseline.", font=(None, 10 ,'bold'),fg="IndianRed3").grid(row=0,column=0,columnspan=4,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
tk.Label(tab1TopFrame, text="IR Measurement : ", font=(None, 9)).grid(row=1,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

optionList = ("map" ,"gm_ap" ,"R-prec" ,"recip_rank" ,"ircl_prn.0.00","ircl_prn.0.10","ircl_prn.0.20","ircl_prn.0.30",
              "ircl_prn.0.40","ircl_prn.0.50","ircl_prn.0.60","ircl_prn.0.70", "ircl_prn.0.80","ircl_prn.0.90",
              "ircl_prn.1.00","P5","P10","P15","P20", "P30", "P100", "P200", "P500", "P1000")
measVar1 = tk.StringVar()
measVar1.set(optionList[0])
measMenu_P1 = tk.OptionMenu(tab1TopFrame, measVar1, *optionList, command=irMeas_P1)
measMenu_P1.config(width=7)
measMenu_P1.grid(row=1,column=1,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

showMeasButton_P1= tk.Button(tab1TopFrame, text="IR Measurements ", command=showmeas1,font=(None, 9),fg="IndianRed3",width=25)
showMeasButton_P1.grid(row=1, column=3, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab1TopFrame, text="Best Baseline Result File : ", font=(None, 9)).grid(row=3,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

bestBLfilename_P11=tk.StringVar(app,tk.NONE)
bestBLfilename_P11.set(BBLnames_initOptions[0])
bestBLmenu_P1= tk.OptionMenu(tab1TopFrame,bestBLfilename_P11,*BBLnames_initOptions, command= bestMenu_P1)
bestBLmenu_P1.config(state= tk.DISABLED, width=7)
bestBLmenu_P1.grid(row=3,column=1,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

plotTypeOneButton = tk.Button(tab1TopFrame, text="Plot", command=plot1, font=(None, 9),width=25, state="disabled")
plotTypeOneButton.grid(row=4, column=3, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
latexBut1 = tk.Button(tab1TopFrame, text="Generate Table in Latex ", command=latex1, font=(None, 9),fg="DeepSkyBlue4",width=25)
latexBut1.grid(row=5, column=3, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

#   Frame(tab1ButFrame) : {...}  #
tk.Label(tab1ButFrame, text="Plot Definition :  Plotting all queries mean retrieval effictiveness across baseline percentiles.", font=(None, 10 ,'bold'),fg="IndianRed3").grid(row=0,column=0,columnspan=4,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
tk.Label(tab1ButFrame, text="Base Baseline Result File : ", font=(None, 9)).grid(row=1,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

baseBLfilename_P11 = tk.StringVar(app,tk.NONE)
baseBLfilename_P11.set(BBLnames_initOptions[0])
baseBLmenu_p1= tk.OptionMenu(tab1ButFrame,baseBLfilename_P11,*BBLnames_initOptions, command= baseMenu_P1)
baseBLmenu_p1.config(state= tk.DISABLED, width=7)
baseBLmenu_p1.grid(row=1,column=2,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab1ButFrame, text="Percentages : %", font=(None, 9)).grid(row=3 ,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
Pcent_seq_l = tk.StringVar(None)
Pcent_seq_l.set("10,20,30,40")
Pcent_seq_ent = tk.Entry(tab1ButFrame, textvariable=Pcent_seq_l, fg="dim gray",width=14).grid(row=3, column=2,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab1ButFrame, text="                                                                                     ", font=(None, 9)).grid(row=4,column=2,padx=2, pady=2,ipadx=2,ipady=2,sticky="e")
tk.Label(tab1ButFrame, text="                     ", font=(None, 9)).grid(row=4,column=1,padx=2, pady=2,ipadx=2,ipady=2,sticky="e")


plot2 = tk.Button(tab1ButFrame, text="Plot", command=Plot2, font=(None, 9), state="disabled",width=25)
plot2.grid(row=4, column=3, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")


#   Frame(tab2) : {tab2TopFrame, tab2midFrame, tab2ButFrame, Label(x2)}
tab2TopFrame= tk.Frame(tab2,bd=2,padx=2,pady=2, relief="sunken")
tab2TopFrame.grid(row=1,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")
tab2midFrame= tk.Frame(tab2,bd=2,padx=2,pady=2, relief="sunken")
tab2midFrame.grid(row=3,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")
tab2butFrame= tk.Frame(tab2,bd=2,padx=2,pady=2, relief="sunken")
tab2butFrame.grid(row=4,column=0,padx=2,pady=2,ipadx=2,ipady=2,sticky="nwes")


tk.Label(tab2, text="Hard Queries Calculation and Specifications ", font=(None, 11,'bold'),fg="maroon").grid(row=0,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="ew")
tk.Label(tab2, text="Hard Queries Relative Representation :", font=(None, 11,'bold'),fg="maroon").grid(row=2, column=0, padx=2, pady=2,ipadx=2,ipady=2,sticky="ew")

#   Frame(tab2TopFrame) : {...}
tk.Label(tab2TopFrame, text="Hard Queries Definition and Specification  : ", font=(None, 8,'bold'),fg="IndianRed3").grid(row=0, column=0,columnspan=4,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
tk.Label(tab2TopFrame, text="IR Measurement : ", font=(None, 9)).grid(row=1,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

optionList = ("map" ,"gm_ap" ,"R-prec" ,"recip_rank" ,"ircl_prn.0.00","ircl_prn.0.10","ircl_prn.0.20","ircl_prn.0.30",
              "ircl_prn.0.40","ircl_prn.0.50","ircl_prn.0.60","ircl_prn.0.70", "ircl_prn.0.80","ircl_prn.0.90",
              "ircl_prn.1.00","P5","P10","P15","P20", "P30", "P100", "P200", "P500", "P1000")

measVar2 = tk.StringVar()
measVar2.set(optionList[0])
measMenu_P2 = tk.OptionMenu(tab2TopFrame, measVar2, *optionList, command=irMeas_P2)
measMenu_P2.config(width=7)
measMenu_P2.grid(row=1,column=2,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab2TopFrame, text="Base Baseline Result File : ", font=(None, 9)).grid(row=2,column=0,padx=2, pady=2,ipadx=2,ipady=2, sticky="w")

baseBLfilename_P22=tk.StringVar(app,tk.NONE)
baseBLfilename_P22.set(BBLnames_initOptions[0])
baseBLmenu_p2= tk.OptionMenu(tab2TopFrame,baseBLfilename_P22,*BBLnames_initOptions, command= baseMenu_P2)
baseBLmenu_p2.config(state= tk.DISABLED, width=7)
baseBLmenu_p2.grid(row=2,column=2,padx=2, pady=2,ipadx=2,ipady=2)

hardLimitrangeLabel = tk.Label(tab2TopFrame, text="Range Specification : ",font=(None, 9))
hardLimitrangeLabel.grid(row=3,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
hardRRange=tk.StringVar()
hardRRange.set("0.05")
hardlimitrangeEntry=tk.Entry(tab2TopFrame,textvariable=hardRRange ,width=10 ,fg="dim gray")
hardlimitrangeEntry.grid(row=3, column=2, padx=2, pady=2, ipadx=2, ipady=2,sticky="ew")

tk.Label(tab2TopFrame, text="             ").grid(row=4,column=1,padx=2, pady=2,ipadx=2,ipady=2,sticky="ew")

tk.Label(tab2TopFrame, text="               ").grid(row=4,column=3,padx=2, pady=2,ipadx=2,ipady=2,sticky="ew")

#   Frame(tab2midFrame) : {...}
tk.Label(tab2midFrame, text="Plot Definition :  Improvement of value of selected IR measurement on hard queries over the best baseline", font=(None, 10,'bold'),fg="IndianRed3").grid(row=0, column=0,columnspan=4,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab2midFrame, text="Best Baseline Result File : ", font=(None, 9)).grid(row=1, column=0, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
bestBLfilename_P22=tk.StringVar(app,tk.NONE)
bestBLfilename_P22.set(BBLnames_initOptions[0])
bestBLmenu_P2= tk.OptionMenu(tab2midFrame,bestBLfilename_P22,*BBLnames_initOptions, command= bestMenu_P2)
bestBLmenu_P2.config(state= tk.DISABLED, width=8)
bestBLmenu_P2.grid(row=1, column=1, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

plot3 = tk.Button(tab2midFrame, text="Plot", command=plot3, font=(None, 9), state="disabled",width=25)
plot3.grid(row=2, column=2, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

latexBut2 = tk.Button(tab2midFrame, text="Generate Table in Latex", command=latex2, font=(None, 9),fg="DeepSkyBlue4",width=25)
latexBut2.grid(row=3, column=2, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

#   Frame(tab2butFrame) : {...}
tk.Label(tab2butFrame, text="Plot Definition :  Plotting hard queries mean retrieval effictiveness across baseline percentiles.", font=(None, 10 ,'bold'),fg="IndianRed3").grid(row=0,column=0,columnspan=4,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")

tk.Label(tab2butFrame, text="Percentages : %", font=(None, 9)).grid(row=3 ,column=0,padx=2, pady=2,ipadx=2,ipady=2,sticky="w")
Pcent_seq_l2 = tk.StringVar(None)
Pcent_seq_l2.set("10,20,30,40")
Pcent_seq_ent_2 = tk.Entry(tab2butFrame, textvariable=Pcent_seq_l2, fg="dim gray",width=14).grid(row=3, column=1,padx=2, pady=2,ipadx=2,ipady=2,sticky="e")

plot4 = tk.Button(tab2butFrame, text="Plot", command=plot4, font=(None, 9), state="disabled",width=25)
plot4.grid(row=4, column=3, padx=2, pady=2,ipadx=2,ipady=2,sticky="w")





tabControl.grid(row=1, sticky='EW',padx=2, pady=2,ipadx=2,ipady=2)

app.mainloop()