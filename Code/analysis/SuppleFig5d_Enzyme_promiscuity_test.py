#!/usr/bin/python
# coding: utf-8

# Author: LE YUAN

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy import stats
import seaborn as sns
import pandas as pd
from scipy.stats import ranksums


def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
   
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def main() :

    with open('../../Data/enzyme_promiscuity/test_preferred_alternative_random.txt', 'r') as infile :
        lines = infile.readlines()

        alldata = dict()
        alldata['type'] = list()
        alldata['value'] = list()
        preferred_substrates = list()
        alternative_substrates = list()
        random_substrates = list()
        for line in lines[1:] :
            data = line.strip().split('\t')
            order, value, substrate_type = data[0], data[1], data[2]

            if substrate_type == 'Preferred' :
                preferred_substrates.append(float(value))
                alldata['type'].append('Preferred')
                alldata['value'].append(float(value))
            if substrate_type == 'Alternative' :
                alternative_substrates.append(float(value))
                alldata['type'].append('Alternative')
                alldata['value'].append(float(value))
            if substrate_type == 'Random' :
                random_substrates.append(float(value))
                alldata['type'].append('Random')
                alldata['value'].append(float(value))

    p_value_1 = ranksums(preferred_substrates, alternative_substrates)[1]
    p_value_2 = ranksums(preferred_substrates, random_substrates)[1]
    p_value_3 = ranksums(alternative_substrates, random_substrates)[1]
    print('The amount of preferred_substrates:', len(preferred_substrates))
    print('The amount of alternative_substrates:', len(alternative_substrates))
    print('The amount of random_substrates:', len(random_substrates))
    print('The median value of preferred_substrates: %.4f' % median(preferred_substrates))
    print('The median value of alternative_substrates: %.4f' % median(alternative_substrates))
    print('The median value of random_substrates: %.4f' % median(random_substrates))
    print('The real value of preferred substrates: %.2f' % pow(10, median(preferred_substrates)))
    print('The real value of alternative substrates: %.2f' % pow(10, median(alternative_substrates)))
    print('The real value of random substrates: %.2f' % pow(10, median(random_substrates)))
    print('P value between preferred_substrates and alternative_substrates is: %s' % p_value_1)
    print('P value between preferred_substrates and random_substrates is: %s' % p_value_2)
    print('P value between alternative_substrates and random_substrates is: %s' % p_value_3)

    # The amount of preferred_substrates: 95
    # The amount of alternative_substrates: 142
    # The amount of random_substrates: 95
    # The median value of preferred_substrates: 1.0115
    # The median value of alternative_substrates: 0.6959
    # The median value of random_substrates: 0.3928
    # The real value of preferred substrates: 10.27
    # The real value of alternative substrates: 4.97
    # The real value of random substrates: 2.47
    # P value between preferred_substrates and alternative_substrates is: 0.01430651489756451
    # P value between preferred_substrates and random_substrates is: 5.267302868022526e-05
    # P value between alternative_substrates and random_substrates is: 0.02299337746277678

    # Plot the boxplot figures between the Alternative and Preferred
    allData = pd.DataFrame(alldata)
    # print(type(allData))

    plt.figure(figsize=(1.5,1.5))

    # To solve the 'Helvetica' font cannot be used in PDF file
    # https://stackoverflow.com/questions/59845568/the-pdf-backend-does-not-currently-support-the-selected-font
    rc('font',**{'family':'serif','serif':['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42

    plt.axes([0.12,0.12,0.83,0.83])
    
    plt.tick_params(direction='in')
    plt.tick_params(which='major',length=1.5)
    plt.tick_params(which='major',width=0.4)
    plt.tick_params(which='major',width=0.4)

    # rectangular box plot
    palette = {"Random": '#FF8C00', "Alternative": '#2166ac', "Preferred": '#b2182b'}

    # for ind in allData.index:
    #     allData.loc[ind,'entry'] = '${0}$'.format(allData.loc[ind,'entry'])

    ax = sns.boxplot(data=alldata, x="type", y="value", order = ["Random", "Alternative", "Preferred"],
            palette=palette, showfliers=False, linewidth=0.5, width=0.5)  # boxprops=dict(alpha=1.0)

    ax = sns.stripplot(data=alldata, x="type", y="value", order = ["Random", "Alternative", "Preferred"],
            palette=palette, size=0.7)  # boxprops=dict(alpha=1.0)

    # https://stackoverflow.com/questions/58476654/how-to-remove-or-hide-x-axis-label-from-seaborn-boxplot
    # plt.xlabel(None) will remove the Label, but not the ticks. 
    ax.set(xlabel=None)

    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.3))

    # print(ax.artists)
    # print(ax.lines)
    # print(len(ax.lines))
    # https://cduvallet.github.io/posts/2018/03/boxplots-in-python
    for i, artist in enumerate(ax.artists):
        # print(i)

        if i % 3 == 0:
            col = '#FF8C00'
        if i % 3 == 1:
            col = '#2166ac'
        if i % 3 == 2:
            col = '#b2182b' 

        # This sets the color for the main box
        artist.set_edgecolor(col)

        # Each box has 5 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        for j in range(i*5,i*5+5):
            # print(j)
            line = ax.lines[j]
            line.set_color(col)
            line.set_mfc(col)
            line.set_mec(col)
    handles = [ax.artists[0], ax.artists[1]]

    # for tick in ax.get_xticklabels() :
    #     tick.set_rotation(30)

    plt.rcParams['font.family'] = 'Helvetica'

    plt.ylabel("Predicted $k$$_\mathregular{cat}$ value [log10]", fontname='Helvetica', fontsize=7)

    # plt.xticks(rotation=30,ha='right')
    # plt.yticks([-2, -1, 0, 1, 2, 3, 4])

    plt.yticks([-2, 0, 2, 4, 6])

    plt.xticks(fontsize=7, rotation=30, ha='right')
    plt.yticks(fontsize=6)

    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)

    plt.savefig("../../Results/figures/SuppleFig5d.pdf", dpi=400, bbox_inches = 'tight')


if __name__ == '__main__' :
    main()
