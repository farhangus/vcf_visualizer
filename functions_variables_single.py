# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:40:52 2023

@author: HGSC
"""
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from vcf_line_parser import VCFLineSV
from vcf_line_parser import VCFLineSVPopulation
from upsetplot import plot
from matplotlib import pyplot
from upsetplot import from_memberships
from DataClasses import *
from dataclasses import dataclass

ranges = [(50, 100), (100,200),(200,300),(300,400),(400,600),(600,800),(800,1000),(1000,2500),(2500,5000),(5000,10000000)]
x_labels = ['50-100', '100-200', '200-300','300-400','400-600','600-800','800-1k','1k-2.5k','2.5k-5k','>5k']

def separate_lists(lst,num):
    elements = [item[num] for item in lst]
    return elements


def count_numbers_in_ranges(numbers, ranges):
    counts = [0] * len(ranges)
    for number in numbers:
        for i, range_ in enumerate(ranges):
            if range_[0] <= number <= range_[1]:
                counts[i] += 1
                break
    return counts


def genome_bar_chart(output_file_path,labels,*bars:GenomeChartData):
    x = np.arange(len(labels))
    # Define the width of each bar
    width = 0.2
    # Create the grouped bar plot
    plt.bar(x - width, bars[0].count(labels), width=width, label=bars[0].legend)
    plt.bar(x, bars[1].count(labels), width=width, label=bars[1].legend)
    # Add labels and title
    plt.xlabel("Genotype",size=6)
    plt.ylabel("Count",size=6)
    plt.title("Genotype_Frequency")
    # Set the x-axis tick labels
    plt.xticks(x, labels)
    # Add a legend
    plt.legend()
    plt.savefig(output_file_path,dpi=800)

def sv_size_type_chart(l1,l2,label_1,label_2,path_2_chart):
    fig, ax = plt.subplots()
    x = np.arange(len(l1))
    # Width of each bar
    bar_width = 0.40
   # Creating the bar plots
    plt.bar(x, l1, width=bar_width, label=label_1)
    plt.bar(x + bar_width, l2, width=bar_width, label=label_2)
#    plt.bar(x + 2*bar_width, l3, width=bar_width, label='DUP')
#    plt.bar(x + 3*bar_width, l4, width=bar_width, label='INV')
#    plt.bar(x + 4*bar_width, l5, width=bar_width, label='BND')

    # Adding labels and title
    plt.xlabel('SizeBin')
    plt.ylabel('Count')
    plt.title('SV Size/Type Distribution')
    plt.xticks(x + bar_width/5, x)
    ax.set_xticklabels(x_labels,rotation=45)
    plt.tight_layout()  # Adjust the padding to accommodate all labels
    plt.legend(title='svtype')
    # Displaying the plot
    plt.savefig(path_2_chart,dpi=800)
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


def lenght_var_count_chart(output_name,del_flag,v_s_list,min_val,max_value,chart_pos,ytick_flag,xtick_locs_list,plt_titl,subplt_title):

    plt.subplot(1,6, chart_pos)
    plt.subplots_adjust(wspace=0.05, hspace=0.05,bottom=0.3)

    minimum = min_val
    maximum = max_value
    selected_values = [x for x in v_s_list if minimum <= x <= maximum]
    # Determine the bin size
    bin_size = round((max(selected_values) - min(selected_values))/100)
    # Create bins based on the bin size
    bins = np.arange(min(selected_values), max(selected_values) + bin_size, bin_size)
    # Count the number of values that fall into each bin
    bin_counts, _ = np.histogram(selected_values, bins)
    # Display the bin plot

    plt.bar(bins[:-1], bin_counts, width=bin_size, align='edge')

    xtick_labels = [str(x) for x in xtick_locs_list]

    plt.xticks(xtick_locs_list, xtick_labels,rotation=90)
    if chart_pos==1:
        plt.ylabel('Counts')
    if chart_pos==3:
        plt.xlabel('\n\n        Lenght of Variants')

    plt.yscale('log')
    if ytick_flag:
        plt.yticks([1,10, 100,1000,10000])
    else:
        plt.yticks([1,10,100,1000,10000])
        plt.yticks([])
    plt.title(subplt_title,size=5)
    if del_flag:
        plt.gca().invert_xaxis()

    plt.savefig(output_name,dpi=1000)




def vcf_number_variants(input_vcf_file):
    with open(input_vcf_file,"r") as f:
        lines=f.readlines()
        vcf_variables=VcfVariables.new()

        for line in lines:
            if line[0] != "#":
                obj=VCFLineSV(line)
                # specify the type of a  file (single/multi)
                # obj_supp_vec = VCFLineSVPopulation(line)
                # print(obj_supp_vec.SUPP_VEC+"\n")
                if obj.SVTYPE=="DEL":
                    vcf_variables.DEL.append(abs(obj.SVLEN))
                    vcf_variables.DEL_GENOTYPE.append(obj.GENOTYPE)
                    vcf_variables.DEL_AF.append(obj.AF)
                elif obj.SVTYPE=="INS":
                    vcf_variables.INS.append(obj.SVLEN)
                    vcf_variables.INS_GENOTYPE.append(obj.GENOTYPE)
                    vcf_variables.INS_AF.append(obj.AF)
                elif obj.SVTYPE=="INV":
                    vcf_variables.INV.append(obj.SVLEN)
                    vcf_variables.INV_GENOTYPE.append(obj.GENOTYPE)
                    vcf_variables.INV_AF.append(obj.AF)
                elif obj.SVTYPE=="DUP":
                    vcf_variables.DUP.append(obj.SVLEN)
                    vcf_variables.DUP_GENOTYPE.append(obj.GENOTYPE)
                    vcf_variables.DEL_AF.append(obj.AF)
                elif obj.SVTYPE=="BND":
                    vcf_variables.BND.append(obj.SVLEN)
                    vcf_variables.BND_GENOTYPE.append(obj.GENOTYPE)
                    vcf_variables.BND_AF.append(obj.AF)
    return vcf_variables



