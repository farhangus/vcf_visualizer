# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:40:52 2023

@author: HGSC
"""
import matplotlib.pyplot as plt
import numpy as np
from vcf_line_parser import VCFLineSV
from vcf_line_parser import VCFLineSVPopulation
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


def genome_bar_chart(*arges):
    data=arges[0][0]
    data1=arges[1][0]
    label_1=arges[0][1]
    label_2=arges[1][1]
    counts_data0 = [data.count("0/0"), data.count("0/1"), data.count("1/1")]
    counts_data1 = [data1.count("0/0"), data1.count("0/1"), data1.count("1/1")]

    
    # Define the x-axis labels and positions
    labels = ["0/0", "0/1", "1/1"]
    x = np.arange(len(labels))

    # Define the width of each bar
    width = 0.2

    # Create the grouped bar plot
    plt.bar(x - width, counts_data0, width=width, label=label_1)
    plt.bar(x, counts_data1, width=width, label=label_2)
    # Add labels and title
    plt.xlabel("Genotype",size=6)
    plt.ylabel("Count",size=6)
    plt.title("Genotype_Frequency")

    # Set the x-axis tick labels
    plt.xticks(x, labels)

    # Add a legend
    plt.legend()
    plt.savefig(arges[-1],dpi=800)

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
    f=open(input_vcf_file)
    lines=f.readlines()
    DEL, DEL_GENOTYPE = [], []
    INS, INS_GENOTYPE = [], []
    DUP, DUP_GENOTYPE = [], []
    INV, INV_GENOTYPE = [], []
    BND, BND_GENOTYPE = [], []
    for line in lines:
        if line[0] != "#":
            obj=VCFLineSV(line)
            if obj.SVTYPE=="DEL":
                DEL.append(abs(obj.SVLEN))
                DEL_GENOTYPE.append(obj.GENOTYPE)
            elif obj.SVTYPE=="INS":
                INS.append(obj.SVLEN)
                INS_GENOTYPE.append(obj.GENOTYPE)
            elif obj.SVTYPE=="INV":
                INV.append(obj.SVLEN)
                INV_GENOTYPE.append(obj.GENOTYPE)
            elif obj.SVTYPE=="DUP":
                DUP.append(obj.SVLEN)
                DUP_GENOTYPE.append(obj.GENOTYPE)
            elif obj.SVTYPE=="BND":
                BND.append(obj.SVLEN)
                BND_GENOTYPE.append(obj.GENOTYPE)
    return DEL,DEL_GENOTYPE,INS,INS_GENOTYPE,DUP,DUP_GENOTYPE,INV,INV_GENOTYPE,BND,BND_GENOTYPE

def allele_frequency_chart_genrator(input_file_path,output_file_path):
    
    DEL_LIST = []
    INS_LIST = []
    INV_LIST = []

    with open(input_file_path, "r") as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith("#"):
                continue
            obj = VCFLineSVPopulation(line)
            print(obj.ID)
            if obj.SVTYPE == "DEL":
                DEL_LIST.append(obj.samples_AF)
            elif obj.SVTYPE == "INS":
                INS_LIST.append(obj.samples_AF)
            elif obj.SVTYPE == "INV":
                INV_LIST.append(obj.samples_AF)
    NUMBER_SAMPLES=len(DEL_LIST[0][:8])
    AF_single_sample_flag = int(NUMBER_SAMPLES == 1)

    for i in range(NUMBER_SAMPLES):
        tmp_list_name_del="del_AF_"+str(i)
        tmp_list_name_del=[]
        tmp_list_name_del=separate_lists(DEL_LIST,i)
        tmp_list_name_ins="ins_AF_"+str(i)
        tmp_list_name_ins=[]
        tmp_list_name_ins=separate_lists(INS_LIST,i)
        tmp_list_name_inv="inv_AF_"+str(i)
        tmp_list_name_inv=[]
        tmp_list_name_inv=separate_lists(INV_LIST,i)
        bin_size = 0.04
        num_bins = int(1 / bin_size)
    
        plt.hist([tmp_list_name_del, tmp_list_name_ins, tmp_list_name_inv], bins=num_bins, range=(0, 1), label=['DEL', 'INS', 'INV'],
                  alpha=0.7, edgecolor='black')
    
        plt.yscale('log')
        x_label = 'AF_sample_' + str(i+1) if not AF_single_sample_flag else 'AF'
        plt.xlabel(x_label) 
        plt.ylabel('Count (log)')
        plt.title('Site Frequency Spectrum')
        plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), prop={'size': 5})
    
        plt.savefig(output_file_path+"AF_"+str(i), dpi=800)
        plt.close()
            
    

