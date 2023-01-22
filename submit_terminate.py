#Description-----------------------------------------------------------------
# Interact with HPC via GUI
# 1. prepare required input files for the back-end application and submit MPI jobs to HPC
# 2. terminate the submitted MPI job
#
#
#Last modified date: Jan 21, 2023
#Python code written by Dr. Yang, and Dr. Li
#All rights reserved
#//-----------------------------------------------------------------


import math
import os
from tkinter import messagebox
from tinydb import TinyDB, Query
import shutil
import struct



def submit(Facility_text, MPI_text, Jobname_text, Node_text, Time_text, sbatch_text,
PM, db, add_text, Input_text, menu, var_delimiter, separator_text, var_miss, special_text, var_UP_FHDI,
cellmake_menu, collapsing_text, category_text, NonCollapsible_text, imputation_menu, donor_text, variance_menu, vartype_menu,
merge_menu, memory_text, Output_text, var_intermediate, analysis_var1, analysis_var2, analysis_var3,
load_text, User, column, pages, framebox_text):
    if (Facility_text.get() != "Others"):
        Parameter_list = [len(Facility_text.get()), len(Jobname_text.get()), len(Node_text.get()),
                          len(MPI_text.get()), len(Time_text.get())]
    if (Facility_text.get() == "Others"):
        Parameter_list = [len(sbatch_text.get())]

    for x in Parameter_list:
        if(x == 0):
            messagebox.showerror("showerror", "Please fill in all parameters in the current page!")
            return

    if (PM.get() == 1):
        db.insert({
            "Project": add_text.get(),
            "Input directory": Input_text.get(),
            "Header": menu.get(),
            "Delimiter": var_delimiter.get(),
            "Special delimiter": separator_text.get(),
            "Symbols for Missingness": var_miss.get(),
            "Special symbols for missingness": special_text.get(),
            "# MPI tasks": MPI_text.get(),

            "Methods": var_UP_FHDI.get(),

            "i_cellmake": cellmake_menu.get(),
            "i_collapsing": collapsing_text.get(),
            "# category": category_text.get(),
            "NonCollapsible_categorical": NonCollapsible_text.get(),
            "i_imputation": imputation_menu.get(),
            "i_donor": donor_text.get(),
            "i_variance": variance_menu.get(),
            "i_var_type": vartype_menu.get(),
            "i_merge": merge_menu.get(),
            "memory": memory_text.get(),

            "Facility": Facility_text.get(),
            "Job script directory": sbatch_text.get(),
            "Job name": Jobname_text.get(),
            "# Node": Node_text.get(),
            "Maximum runtime": Time_text.get(),

            "Output directory": Output_text.get(),
            "Save files": var_intermediate.get(),
            "Imputation results": analysis_var1.get(),
            "Mean and variance estimates": analysis_var2.get(),
            "None of above": analysis_var3.get()
        })
    elif (PM.get() == 2):
        db.update({"Input directory": Input_text.get(),
                   "Header": menu.get(),
                   "Delimiter": var_delimiter.get(),
                   "Special delimiter": separator_text.get(),
                   "Symbols for Missingness": var_miss.get(),
                   "Special symbols for missingness": special_text.get(),
                   "# MPI tasks": MPI_text.get(),

                   "Methods": var_UP_FHDI.get(),

                   "i_cellmake": cellmake_menu.get(),
                   "i_collapsing": collapsing_text.get(),
                   "# category": category_text.get(),
                   "NonCollapsible_categorical": NonCollapsible_text.get(),
                   "i_imputation": imputation_menu.get(),
                   "i_donor": donor_text.get(),
                   "i_variance": variance_menu.get(),
                   "i_var_type": vartype_menu.get(),
                   "i_merge": merge_menu.get(),
                   "memory": memory_text.get(),

                   "Facility": Facility_text.get(),
                   "Job script directory": sbatch_text.get(),
                   "Job name": Jobname_text.get(),
                   "# Node": Node_text.get(),
                   "Maximum runtime": Time_text.get(),

                   "Output directory": Output_text.get(),
                   "Save files": var_intermediate.get(),
                   "Imputation results": analysis_var1.get(),
                   "Mean and variance estimates": analysis_var2.get(),
                   "None of above": analysis_var3.get()
                   },
                  User.Project == load_text.get())
    else:
        print("Big ERROR! Current project is not successfully updated to database!!!!!")

    # print("Input directory: ", Input_text.get())
    # print("Header: ", menu.get())
    # print("Seperator: ", separator_text.get())
    # print("Missing symbol: ", var_miss.get())
    # print("Special symbol: ", special_text.get())
    # print("Output directory: ", Output_text.get())
    # print("Method: ", var_UP_FHDI.get())

    root_folder = ""
    if(PM.get() == 1):
        root_folder = add_text.get()
        #print("I am asked to cretae this directory firstly and root_folder is " + root_folder)
        os.mkdir('./'+ add_text.get())
        os.mkdir('./'+ add_text.get() + '/Temp')
        os.mkdir('./'+ add_text.get() + '/Post')
    else:
        root_folder = load_text.get()
        #print("I am asked to delete this directory firstly and root_folder is " + root_folder)
        shutil.rmtree('./'+ load_text.get())
        os.mkdir('./'+ load_text.get())
        os.mkdir('./'+ load_text.get() + '/Temp')
        os.mkdir('./'+ load_text.get() + '/Post')
        # os.system("rm -r ./" + load_text.get() + "/Output.txt")
        # os.system("rm -r ./" + load_text.get() + "/Temp/*")
        # os.system("rm -r ./" + load_text.get() + "/Post/*")

    #start1 = time.time()
    try:
        file = open(Input_text.get(), "r")
        script = open(Output_text.get() + "Temp/run.sbatch", "w", newline='\n')
        input_file = open(Output_text.get() + "Temp/input.txt", "w")
    except IOError:
        print("Output directory is not accessible when submit!")
        return

    if var_miss.get() == 1:
        Symbol = ' '
    if var_miss.get() == 2:
        Symbol = 'NA'
    if var_miss.get() == 3:
        Symbol = '0'
    if var_miss.get() == 4:
        Symbol = special_text.get()

    if (var_delimiter.get() == 1):
        delimeter_temp = ','
    if (var_delimiter.get() == 2):
        delimeter_temp = '\t'
    if (var_delimiter.get() == 3):
        delimeter_temp = ' '
    if (var_delimiter.get() == 4):
        delimeter_temp = separator_text.get()
    #print("delimeter_temp in submit is ", delimeter_temp)

    daty = []
    datr = []

    if menu.get() == "Yes":
        Header_line = file.readline()

    for line in file:
        raw_line = line.split(delimeter_temp)
        # print(raw_line)
        d_out = []
        i_out = []
        # If symbol is NA or na
        if var_miss.get() == 2:
            for c in raw_line:
                if (c == Symbol or c == Symbol.lower()):
                    i_out.append('0')
                    d_out.append('0.0')
                elif (c == (Symbol + '\n') or c == (Symbol.lower() + '\n')):
                    i_out.append('0')
                    d_out.append('0.0\n')
                else:
                    i_out.append('1')
                    d_out.append(c)
        # Otherwsie, no lowercase required
        else:
            for c in raw_line:
                if (c == Symbol):
                    i_out.append('0')
                    d_out.append('0.0')
                elif (c == (Symbol + '\n')):
                    i_out.append('0')
                    d_out.append('0.0\n')
                else:
                    i_out.append('1')
                    d_out.append(c)

        # print(i_out)
        daty.append(d_out)
        datr.append(i_out)

    #start2 = time.time()

    if (var_UP_FHDI.get() == 1):
        try:
            daty_file = open(Output_text.get() + "Temp/daty.txt", 'w')
            datr_file = open(Output_text.get() + "Temp/datr.txt", "w")
        except IOError:
            print("Output directory is not accesible when creating data files!")
            return

        daty_file.write("daty\n")
        for line1 in daty:
            # print(line1)
            daty_file.write('\t'.join(line1))

        datr_file.write("datr\n")
        for line2 in datr:
            datr_file.write('\t'.join(line2))
            datr_file.write('\n')
        daty_file.close()
        datr_file.close()

    if (var_UP_FHDI.get() == 2):
        # print(datr)
        datr_final = [list(map(int, i)) for i in datr]
        # print(datr_final[1])
        # print(daty)
        daty_final = [list(map(float, j)) for j in daty]
        # print(daty_final[1])

        daty_column = []
        for i in range(len(daty_final[0])):
            for j in daty_final:
                daty_column.append(j[i])

        daty_row = []
        for k in daty_final:
            for t in k:
                daty_row.append(t)

        datr_column = []
        for i in range(len(datr_final[0])):
            for j in datr_final:
                datr_column.append(j[i])

        try:
            file_daty_column = open(Output_text.get() + "Temp/daty_column_binary.bin", 'wb')
            file_daty_row = open(Output_text.get() + "Temp/daty_row_binary.bin", 'wb')
            file_datr_column = open(Output_text.get() + "Temp/datr_column_binary.bin", 'wb')
        except IOError:
            print("Output directory is not accesible when creating binary data files!")
            return

        buf1 = bytes()
        buf2 = bytes()
        buf3 = bytes()

        for i in daty_column:
            buf1 += struct.pack('d', i)
        for i in daty_row:
            buf2 += struct.pack('d', i)
        for i in datr_column:
            buf3 += struct.pack('i', i)
        file_daty_column.write(buf1)
        file_daty_row.write(buf2)
        file_datr_column.write(buf3)

        file_daty_column.close()
        file_daty_row.close()
        file_datr_column.close()
    

    ###################################
    script.write("#!/bin/bash\n")
    script.write("#SBATCH --job-name=" + Jobname_text.get() + '\n')
    script.write("#SBATCH --nodes=" + Node_text.get() + '\n')
    script.write("#SBATCH --ntasks=" + MPI_text.get() + '\n')
    script.write("#SBATCH --time=" + Time_text.get() + '\n')
    script.write("#SBATCH --output=BATCH_OUTPUT\n")
    script.write("#SBATCH --error=BATCH_ERROR\n")
    script.write("module load intel/18.3\n")
    script.write("mpirun -np " + MPI_text.get() + " ./main_MPI " + root_folder)

    ########################################

    if (var_UP_FHDI.get() == 1):
        i_option_ultra = '0'
    else:
        i_option_ultra = '1'

    if (imputation_menu.get() == "FEFI"):
        i_option_imputation = '1'
    else:
        i_option_imputation = '2'

    if (variance_menu.get() == "Yes"):
        i_option_variance = '1'
    else:
        i_option_variance = '0'

    if (merge_menu.get() == "Yes"):
        i_option_merge = '0'
    else:
        i_option_merge = '1'

    if (cellmake_menu.get() == "Cell Collapsing"):
        i_option_cellmake = '1'
    else:
        i_option_cellmake = '2'

    if (vartype_menu.get() == "Jackknife"):
        i_option_var_type = '1'
    else:
        i_option_var_type = '2'

    if(var_intermediate.get() == 1):
        i_option_save = '1'
    else:
        i_option_save = '0'

    if (analysis_var3.get() == 1):
        i_analysis_imputation = '0'
        i_analysis_mean = '0'
    else:
        i_analysis_imputation = str(analysis_var1.get())
        i_analysis_mean = str(analysis_var2.get())

    input_file.write("INPUT INFORMATION\n")
    input_file.write("i_option_read_data\t" + '1\n')
    input_file.write("i_option_ultra\t" + i_option_ultra + '\n')
    input_file.write("i_option_perform\t" + '1\n')
    input_file.write("nrow\t" + str(len(daty)) + '\n')
    input_file.write("ncol\t" + str(column.get()) + '\n')
    input_file.write("i_option_imputation\t" + i_option_imputation + '\n')
    input_file.write("i_option_variance\t" + i_option_variance + '\n')
    input_file.write("i_option_merge\t" + i_option_merge + '\n')
    input_file.write("i_donor\t" + donor_text.get() + '\n')
    input_file.write("i_user_defined_datz\t" + '0\n')
    input_file.write("i_option_collapsing\t" + collapsing_text.get() + '\n')
    input_file.write("i_option_SIS_type\t" + '3\n')
    input_file.write("top_correlation\t" + '100\n')
    input_file.write("i_option_cellmake\t" + i_option_cellmake + '\n')
    input_file.write("i_option_var_type\t" + i_option_var_type + '\n')
    input_file.write("memory\t" + memory_text.get() + '\n')
    input_file.write("i_option_save\t" + i_option_save + '\n')
    input_file.write("i_analysis_imputation\t" + i_analysis_imputation + '\n')
    input_file.write("i_analysis_mean\t" + i_analysis_mean + '\n')
    input_file.write("END INPUT INFORMATION \n\n")

    input_file.write("category\n")
    if (len(category_text.get()) == 1):
        for x in range(len(daty)):
            input_file.write(category_text.get() + '  ')
    else:
        category_list = list(category_text.get().split(','))
        for x in category_list:
            input_file.write(str(x) + '  ')

    input_file.write("\n")
    input_file.write("NonCollapsible_categorical\n")
    if (len(NonCollapsible_text.get()) == 1):
        for x in range(len(daty)):
            input_file.write(NonCollapsible_text.get() + '  ')
    else:
        NonCollapsible_list = list(NonCollapsible_text.get().split(','))
        for x in NonCollapsible_list:
            input_file.write(str(x) + '  ')

    input_file.write("\n")
    input_file.write("weight\n")
    for x in range(len(daty)):
        input_file.write('1\n')

    input_file.write("END DATA INPUT")

    file.close()
    script.close()
    input_file.close()

    os.system("sbatch " + Output_text.get() + "Temp/run.sbatch")
    
    #========================
    # Estimate running time
    #========================

    size_GB = (column.get()*len(daty)*8)/(10**9)
    #print("size_GB is ", size_GB)
    time_lower = 0
    time_upper = 0
    residual = 0

    #For small data
    if len(daty) <= 10000 and column.get() <= 2000:
        message_f2 = "less than an hour"
    else:
        #For large data
        if i_option_variance == '0': # no variance estimation
             residual = 43.62
             time_lower = math.floor((5.9177 * size_GB + 25.391 - residual)/(int(MPI_text.get())))
             time_upper = math.ceil((5.9177 * size_GB + 25.391 + residual)//(int(MPI_text.get())))
        else:
            if i_option_var_type == '1': #Jackknife
                residual = 38.95
                time_lower = math.floor((43.878 * size_GB + 79.25 - residual)/(int(MPI_text.get())))
                time_upper = math.ceil((43.878 * size_GB + 79.25 + residual)/(int(MPI_text.get())))
            else: #Linearization
                residual = 42.99
                time_lower = math.floor((9.6222 * size_GB + 24.56 - residual)/(int(MPI_text.get())))
                time_upper = math.ceil((9.6222 * size_GB + 24.56 + residual)/(int(MPI_text.get())))
        
        #Generate time message
        #print("time_lower is ", time_lower)
        if(time_lower < 0):
            time_lower = 0
        #print("time_upper is ", time_upper)

        if(time_upper <= 1):
            message_f2 = "less than an hour"
        else:
            if(time_lower > 0):
                message_f2 = str(time_lower) + "hr ~ " + str(time_upper) + "hr"
            else:
                message_f2 = "less than " + str(time_upper) + "hr"
        
    message_f1 = " Estimated exection time: " + message_f2
    message_f3 = " Reults will be automatically returned to output "
    message_f31 = " directory when UP-FHDI successfully finishes "
    message_f4 = " Please feel free to close this window if you will "
    message_f41 = " not terminate the task."
    message_final = message_f1 + '\n\n' + message_f3 + '\n' + message_f31 + '\n\n' + message_f4 + '\n' + message_f41
    framebox_text.set(message_final)

    page = pages.pop(0)
    pages.append(page)
    pages[0].lift()




def terminate(root):
    os.system("squeue -u $USER | awk '{print $1}' | tail -n+2 | xargs scancel")
    root.destroy()