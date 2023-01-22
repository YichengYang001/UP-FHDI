#-----------------------------------------------------------------
#GUI for UP-FHDI
#
#A general-purpose, assumption-free imputation software for curing incomplete datasets
# 
#Version: 1.0
#Last release date: Jan 21, 2023
#Developers: Yicheng Yang and Qi Li (Iowa State University)
#Contact: icho@iastate.edu
#//-----------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import tkinter.font as font
# import codecs #to decode raw strings \t, \n, \r to normal strings
#import struct
from tinydb import TinyDB, Query
#import os
import shutil
#import math
#import time

from explain import *
from next_back import *
from submit_terminate import *

root = tk.Tk()
root.title("Welcome to UP-FHDI")
root.geometry("400x510+200+200")


def varName(p):
    for k, v in globals().items():
        if id(p) == id(v):
            return k


pages = []
db = TinyDB('UP_FHDI_DB.json')
User = Query()
PM = tk.IntVar()
PM.set(1)


def PM_call_back(var, index, mode):
    #Set all parameters as empty
    if(PM.get() == 1):
        #print("PM Changed to ", PM.get())
        Input_text.set("./raw.txt")
        menu.set("")
        var_delimiter.set(0)
        var_miss.set(0)
        MPI_text.set('4')
        var_UP_FHDI.set(0)

        cellmake_menu.set('')
        collapsing_text.set('4')
        category_text.set('3')
        NonCollapsible_text.set('0')
        imputation_menu.set('')
        donor_text.set('5')
        variance_menu.set('')
        vartype_menu.set('')
        merge_menu.set('')
        memory_text.set('8')

        Facility_text.set("Condo2017")
        sbatch_text.set("./run.sbatch")
        Jobname_text.set("UP-FHDI")
        Node_text.set('1')
        Time_text.set("00:00:10")

        Output_text.set("./" + add_text.get() + '/')
        var_intermediate.set(0)
        analysis_var1.set(0)
        analysis_var2.set(0)
        analysis_var3.set(0)

    #Load existing project parameters
    if(PM.get() == 2):
        #print("PM Changed to ", PM.get())
        LPM = db.search(User.Project == load_text.get())
        #print(LPM)
        Input_text.set(LPM[0].get('Input directory'))
        menu.set(LPM[0].get('Header'))
        var_delimiter.set(LPM[0].get('Delimiter'))
        separator_text.set(LPM[0].get('Special delimiter'))
        var_miss.set(LPM[0].get('Symbols for Missingness'))
        special_text.set(LPM[0].get('Special symbols for missingness'))
        MPI_text.set(LPM[0].get('# MPI tasks'))

        var_UP_FHDI.set(LPM[0].get('Methods'))

        cellmake_menu.set(LPM[0].get('i_cellmake'))
        collapsing_text.set(LPM[0].get('i_collapsing'))
        category_text.set(LPM[0].get('# category'))
        NonCollapsible_text.set(LPM[0].get('NonCollapsible_categorical'))
        imputation_menu.set(LPM[0].get('i_imputation'))
        donor_text.set(LPM[0].get('i_donor'))
        variance_menu.set(LPM[0].get('i_variance'))
        vartype_menu.set(LPM[0].get('i_var_type'))
        merge_menu.set(LPM[0].get('i_merge'))
        memory_text.set(LPM[0].get('memory'))

        Facility_text.set(LPM[0].get('Facility'))
        sbatch_text.set(LPM[0].get('Job script directory'))
        Jobname_text.set(LPM[0].get('Job Name'))
        Node_text.set(LPM[0].get('# Node'))
        Time_text.set(LPM[0].get('Maximum runtime'))

        Output_text.set(LPM[0].get('Output directory'))
        var_intermediate.set(LPM[0].get('Save files'))
        analysis_var1.set(LPM[0].get('Imputation results'))
        analysis_var2.set(LPM[0].get('Mean and variance estimates'))
        analysis_var3.set(LPM[0].get('None of above'))

    #Delete an existing project
    if(PM.get() ==3):
        #print("PM Changed to ", PM.get())
        for x in range(len(load_list)):
            if (load_list[x].get() == 1):
                db.remove(User.Project == load_name[x])
                shutil.rmtree('./'+load_name[x])


PM.trace_add('write', PM_call_back)
##############################################
##############################################
# Page 0
##############################################
##############################################
page0 = tk.Frame(root)
page0.configure(background='#822433')
yellow_btn= PhotoImage(file='Yellow_Button.png')
resize_yellow_btn = yellow_btn.subsample(2, 2)
font_0 = ('Times New Roman', 12, 'bold')

page0.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
instructions_p0 = tk.Label(page0, text="Project Management", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions_p0.place(x=110, y=30)


######################################################
def call_add_text(var, index, mode):
    Output_text.set("./" + add_text.get() + '/')

def ok_project(inner_root,add_text):
    PM.set(1)
    textbox_input["state"] = tk.NORMAL  # Loading a new project unlock input directory

    if(db.contains(User.Project == add_text.get())):
        messagebox.showerror("showerror", "The entered project name exists, please name a new one!")
    else:
        inner_root.destroy()
        page = pages.pop(0)
        pages.append(page0)
        pages[0].lift()


def add_project():
    inner_root = tk.Toplevel()
    inner_root.title("")

    inner_instructions = tk.Label(inner_root, text="Type your project name")
    inner_instructions.pack()
    add_widget = tk.Entry(inner_root, textvariable=add_text, width=30, justify='center')
    add_widget.pack()

    ok_button = tk.Button(inner_root, text="OK", command=lambda: ok_project(inner_root, add_text))
    ok_button.pack()
    tk.mainloop()


add_text = tk.StringVar()
add_text.trace_add('write', call_add_text)
p0_add = tk.Button(page0, text="Add a new project", font=font_0, image = resize_yellow_btn, compound="center", bd=0, highlightthickness=0, bg='#822433', activebackground="#822433", activeforeground="snow", command=lambda: add_project())
p0_add.place(x=120, y=110)


###########################################
def ok_load_project(inner_load, load_text):
    sum_temp = 0
    for x in range(len(load_list)):
        sum_temp = sum_temp + load_list[x].get()
        if(load_list[x].get() == 1):
            load_text.set(load_name[x])

    if(sum_temp == 0):
        messagebox.showerror("showerror", "Please select an existing project to load!")
        return

    textbox_input["state"] = tk.DISABLED # Loading an existing project locks input directory
    PM.set(2)
    inner_load.destroy()
    page = pages.pop(0)
    pages.append(page0)
    pages[0].lift()
    messagebox.showwarning("warning", "Results of the last run in this project will be overwritten! Please add a new project if you wish to save results!")

def delete_load_project(inner_load):
    sum_temp = 0
    for x in load_list:
        sum_temp = sum_temp + x.get()

    if(sum_temp == 0):
        messagebox.showerror("showerror", "Please select at least a project to delete!")
        return

    PM.set(3)
    inner_load.destroy()

def load_project():

    def call_back_load(var, index, mode):
        sum_temp = 0
        #print("load_list is ", load_list)
        if(len(load_list) != len(db)):
            print("ERROR!!! Load_list is incorrect !!!")

        for x in load_list:
            sum_temp = sum_temp + x.get()
        #print("sum_temp is ", sum_temp)
        if (sum_temp == 1 or sum_temp == 0):
            ok_load_button['state'] = tk.NORMAL
        else:
            ok_load_button['state'] = tk.DISABLED

    def call_back_select(var, index, mode):
        if (select_temp.get() == 1):
            for x in load_list:
                x.set(1)
            for y in button_list:
                y['state'] = tk.DISABLED

            if (len(load_list) > 1):
                ok_load_button['state'] = tk.DISABLED

            # R_ok['state'] = tk.DISABLED

        if (select_temp.get() == 0):
            for x in load_list:
                x.set(0)
            for y in button_list:
                y['state'] = tk.NORMAL
            ok_load_button['state'] = tk.NORMAL

    if (len(db) == 0):
        messagebox.showerror("showerror", "No existing projects!")
        return
    inner_load = tk.Toplevel()
    inner_load.title("")

    load_instructions = tk.Label(inner_load, text="Select an existing project")
    load_instructions.pack()


    load_list.clear()
    load_name.clear()
    button_list.clear()

    for x in db:
        db_temp = tk.IntVar()
        db_temp.trace_add('write', call_back_load)
        load_list.append(db_temp)
        load_name.append(x['Project'])
        R_ok = tk.Checkbutton(inner_load, text = x['Project'], variable= db_temp)
        button_list.append(R_ok)
        R_ok.pack()

    select_temp = tk.IntVar()
    select_temp.set(0)
    select_temp.trace_add('write', call_back_select)
    R_select = tk.Checkbutton(inner_load, text='Select all', variable=select_temp)
    R_select.pack()


    ok_load_button = tk.Button(inner_load, text = "Load", command = lambda: ok_load_project(inner_load, load_text))
    ok_load_button.pack(side = tk.LEFT, padx = 20)

    delete_load_button = tk.Button(inner_load, text = "Delete", command = lambda: delete_load_project(inner_load))
    delete_load_button.pack(side = tk.LEFT)
    tk.mainloop()


load_list = []  # List to show if a project is selected (1) or not (0)
load_name = []  # List to hold all projects' names
button_list = [] # List to hold all project buttons

load_text = tk.StringVar()
p0_load = tk.Button(page0, text="Load a project", font=font_0, image = resize_yellow_btn, compound="center", bd=0, highlightthickness=0, bg='#822433', activebackground="#822433", activeforeground="snow", command=lambda: load_project())
p0_load.place(x=120, y=230)


###############################
def clear_project():
    for y in db:
         shutil.rmtree('./'+ y['Project'])
    db.truncate()


p0_delete = tk.Button(page0, text="Clear all projects", font=font_0, image = resize_yellow_btn, compound="center", bd = 0, highlightthickness=0, bg='#822433', activebackground="#822433", activeforeground="snow", command=lambda: clear_project())
p0_delete.place(x=120, y=360)
pages.append(page0)

##############################################
##############################################
# Page 1
##############################################
##############################################
page1 = tk.Frame(root)
page1.configure(background='#822433')

font_1 = ('Times New Roman', 11, 'bold')

page1.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions = tk.Label(page1, text="Input Configurations", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions.place(x=110, y=10)

################
Input_label = tk.Label(page1, text="Input directory", font = font_1, bg = '#822433', fg="snow")
Input_label.place(x=50, y=50)

Input_text = tk.StringVar()
#print('NIMA', len(Input_text.get()))
Input_text.set("./raw.txt")
textbox_input = tk.Entry(page1, textvariable=Input_text, width=27, bd=0, highlightthickness=0, justify='center', disabledbackground="gray")
textbox_input.place(x=160, y=50)

#################
Input_label = tk.Label(page1, text="Header", font = font_1, bg = '#822433', fg="snow")
Input_label.place(x=50, y=85)

menu = tk.StringVar(page1)
options_list = ["Yes", "No"]
# Create a dropdown Menu
drop = tk.OptionMenu(page1, menu, *options_list)
drop.configure(font = font_1, width=30, bd=0, highlightthickness=0, justify='center', bg = 'snow')
drop.place(x=105, y=83)

drop_list = root.nametowidget(drop.menuname)  # Get menu widget.
drop_list.config(font=font_1)  # Set the dropdown menu's font

###############
delimiter_label = tk.Label(page1, text="Delimiter", font = font_1, bg = '#822433', fg="snow")
delimiter_label.place(x=50, y=120)
var_delimiter = tk.IntVar()

D1 = tk.Radiobutton(page1, text="Comma", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_delimiter, value=1)
D1.place(x=50, y=155)
D2 = tk.Radiobutton(page1, text="Tab", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_delimiter, value=2)
D2.place(x=210, y=155)

D3 = tk.Radiobutton(page1, text="Space", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_delimiter, value=3)
D3.place(x=50, y=190)
D4 = tk.Radiobutton(page1, text="Others",  font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray",variable=var_delimiter, value=4)
D4.place(x=210, y=190)

################
separator_label = tk.Label(page1, text="Special delimiter", font = font_1, bg = '#822433', fg="snow")
separator_label.place(x=50, y=225)

separator_text = tk.StringVar()
textbox_separator = tk.Entry(page1, textvariable=separator_text, width=25, bd=0, highlightthickness=0, disabledbackground="gray", justify='center', state=tk.DISABLED)
textbox_separator.place(x=170, y=225)


def call_back_delimiter(var, index, mode):
    if var_delimiter.get() == 4:
        textbox_separator["state"] = tk.NORMAL
        separator_text.set(";")
    if var_delimiter.get() != 4:
        textbox_separator["state"] = tk.DISABLED
        separator_text.set("")


var_delimiter.trace_add('write', call_back_delimiter)

###############
miss_label = tk.Label(page1, text="Symbols for missingness", font = font_1, bg = '#822433', fg="snow")
miss_label.place(x=50, y=260)
var_miss = tk.IntVar()

R1 = tk.Radiobutton(page1, text="Space", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_miss, value=1)
R1.place(x=50, y=295)
R2 = tk.Radiobutton(page1, text="NA/na", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_miss, value=2)
R2.place(x=210, y=295)

R3 = tk.Radiobutton(page1, text="0", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_miss, value=3)
R3.place(x=50, y=330)
R4 = tk.Radiobutton(page1, text="Others", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=var_miss, value=4)
R4.place(x=210, y=330)

##################
Input_label = tk.Label(page1, text="Special missingess symbol", font = font_1, bg = '#822433', fg="snow")
Input_label.place(x=50, y=365)

special_text = tk.StringVar()
textbox_special = tk.Entry(page1, textvariable=special_text, width=17, bd=0, highlightthickness=0, disabledbackground="gray", justify='center', state=tk.DISABLED)
textbox_special.place(x=230, y=365)


def call_back(var, index, mode):
    if var_miss.get() == 4:
        textbox_special["state"] = tk.NORMAL
        special_text.set("$")
    if var_miss.get() != 4:
        special_text.set("")
        textbox_special["state"] = tk.DISABLED


var_miss.trace_add('write', call_back)

################
MPI_label = tk.Label(page1, text="# MPI tasks", font = font_1, bg = '#822433', fg="snow")
MPI_label.place(x=50, y=400)

MPI_text = tk.StringVar()
MPI_text.set('4')

textbox_MPI = tk.Entry(page1, textvariable=MPI_text, width=28, bd=0, highlightthickness=0, justify='center')
textbox_MPI.place(x=150, y=400)

##################
column = tk.IntVar()


def p1_set_default():
    menu.set("No")
    var_delimiter.set(2)
    var_miss.set(2)
    MPI_text.set(16)


Back_p1 = tk.Button(page1, text = "< Back", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: prev_first_page(pages, PM))
Back_p1.place(x=55, y=445)


Default_p1 = tk.Button(page1, text = "Set default", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: p1_set_default())
Default_p1.place(x=160, y=445)

#print("page_name before is ", varName(page1))
Next_p1 = tk.Button(page1, text = "Next >", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: next_first_page(pages, varName(page1),
var_miss, var_delimiter, Input_text, menu, separator_text, MPI_text, special_text, column, lablegrame_text))
Next_p1.place(x=285, y=445)

pages.append(page1)


##############################################
##############################################
# Page 5
##############################################
##############################################
page5 = tk.Frame(root)
page5.configure(background='#822433')
page5.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions_p5 = tk.Label(page5, text="Output Configurations", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions_p5.place(x=110, y=10)

################
Output_label = tk.Label(page5, text="Output directory", font = font_1, bg = '#822433', fg="snow")
Output_label.place(x=50, y=50)

Output_text = tk.StringVar()
#Output_text.set("./nima" + add_text.get())
textbox_output = tk.Entry(page5, textvariable=Output_text, width=25, bd=0, highlightthickness=0, justify='center')
textbox_output.place(x=170, y=50)

##################
intermediate_label = tk.Label(page5, text="Save intermediate files?", font = font_1, bg = '#822433', fg="snow")
intermediate_label.place(x=50, y=106)
var_intermediate = tk.IntVar()
var_intermediate.set(0)

R1_intermediate = tk.Radiobutton(page5, text="Yes", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable = var_intermediate, value=1)
R1_intermediate.place(x=70, y=162)
R2_intermediate = tk.Radiobutton(page5, text="No", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable = var_intermediate, value=2)
R2_intermediate.place(x=250, y=162)


#######################
instructions_p5 = tk.Label(page5, text="Post analysis", font=font_1 , fg="snow", bg = '#822433')
instructions_p5.place(x=50, y=218)

#####################
analysis_var1 = tk.IntVar()
analysis_var2 = tk.IntVar()
analysis_var3 = tk.IntVar()


def call_back_analysis(var, index, mode):
    if analysis_var3.get() == 0:
        analysis1["state"] = tk.NORMAL
        analysis2["state"] = tk.NORMAL
    if analysis_var3.get() == 1:
        analysis1["state"] = tk.DISABLED
        analysis2["state"] = tk.DISABLED
        analysis_var1.set(0)
        analysis_var2.set(0)


analysis_var3.trace_add('write', call_back_analysis)
fs = font.Font(size=13)
analysis1 = tk.Checkbutton(page5, text="Imputation results", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=analysis_var1)
#analysis1['font'] = fs
analysis1.place(x=60, y=274)

analysis2 = tk.Checkbutton(page5, text="Mean and variance estimates", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=analysis_var2)
#analysis2['font'] = fs
analysis2.place(x=60, y=330)

analysis3 = tk.Checkbutton(page5, text="None of above", font = font_1, bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray", variable=analysis_var3)
#analysis3['font'] = fs
analysis3.place(x=60, y=386)

####################
def p5_set_default():
    var_intermediate.set(2)
    analysis_var3.set(1)



Back_p5 = tk.Button(page5, text="< Back ", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: prev_page(pages))
Back_p5.place(x=55, y=445)

Default_p5 = tk.Button(page5, text = "Set default", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: p5_set_default())
Default_p5.place(x=160, y=445)

Submit_p5 = tk.Button(page5, text="Next >", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: next_page(pages, varName(page5),
var_UP_FHDI, cellmake_menu, collapsing_text, category_text, NonCollapsible_text,
imputation_menu, donor_text, variance_menu, vartype_menu, merge_menu, memory_text, analysis_var1, analysis_var2, analysis_var3, Output_text, var_intermediate,
MPI_text, column))
Submit_p5.place(x=285, y=445)

pages.append(page5)


##############################################
##############################################
# Page 2
##############################################
##############################################
page2 = tk.Frame(root)
page2.configure(background='#822433')
page2.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions_p2 = tk.Label(page2, text="UP-FHDI Configurations", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions_p2.place(x=100, y=10)

####################
lablegrame_text = tk.StringVar()

labelframe_widget = tk.LabelFrame(page2, text="Notes", fg="snow", font = font_1, bg='#822433')
label_widget = tk.Label(labelframe_widget, textvariable=lablegrame_text, justify='left', font= font_1, bd=0, highlightthickness=0, bg='#822433')
labelframe_widget.place(x=57, y=80)
label_widget.pack()


#################
def UP_FHDI_callback(var, index, mode):
    cellmake_menu.set('')
    cellmake_drop['menu'].delete(0, 'end')
    imputation_menu.set('')
    imputation_drop['menu'].delete(0, 'end')
    vartype_menu.set('')
    vartype_drop['menu'].delete(0, 'end')

    if var_UP_FHDI.get() == 1:
        new_choices = ("KNN", "Cell Collapsing")
        for choice in new_choices:
            cellmake_drop['menu'].add_command(label=choice, command=tk._setit(cellmake_menu, choice))
        new_choices = ("FHDI", "FEFI")
        for choice in new_choices:
            imputation_drop['menu'].add_command(label=choice, command=tk._setit(imputation_menu, choice))
        choice = ("Jackknife")
        vartype_drop['menu'].add_command(label=choice, command=tk._setit(vartype_menu, choice))
    else:
        choice = ("KNN")
        cellmake_drop['menu'].add_command(label=choice, command=tk._setit(cellmake_menu, choice))
        choice = ("FHDI")
        imputation_drop['menu'].add_command(label=choice, command=tk._setit(imputation_menu, choice))
        new_choices = ("Jackknife", "Linearization")
        for choice in new_choices:
            vartype_drop['menu'].add_command(label=choice, command=tk._setit(vartype_menu, choice))


var_UP_FHDI = tk.IntVar()
var_UP_FHDI.trace_add('write', UP_FHDI_callback)
UP_FHDI_R1 = tk.Radiobutton(page2, text="P-FHDI", variable=var_UP_FHDI, value=1, font = ('Times New Roman', 15, 'bold'), bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray",)
UP_FHDI_R1.place(x=150, y=250)
UP_FHDI_R2 = tk.Radiobutton(page2, text="UP-FHDI", variable=var_UP_FHDI, value=2, font = ('Times New Roman', 15, 'bold'), bg = '#822433', bd=0, highlightthickness=0, activebackground="#822433", activeforeground="dim gray",)
UP_FHDI_R2.place(x=150, y=350)


####################
Back_p2 = tk.Button(page2, text="< Back ", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: prev_page(pages))
Back_p2.place(x=70, y=445)
Next_p2 = tk.Button(page2, text="Next >", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: next_page(pages, varName(page2),
var_UP_FHDI, cellmake_menu, collapsing_text, category_text, NonCollapsible_text,
imputation_menu, donor_text, variance_menu, vartype_menu, merge_menu, memory_text, analysis_var1, analysis_var2, analysis_var3, Output_text, var_intermediate,
MPI_text, column))
Next_p2.place(x=250, y=445)

pages.append(page2)

##############################################
##############################################
# Page 3
##############################################
##############################################
page3 = tk.Frame(root)
page3.configure(background='#822433')
page3.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions = tk.Label(page3, text="UP-FHDI Configurations", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions.place(x=100, y=10)

#################
cellmake_label = tk.Label(page3, text="i_cellmake", font = font_1, bg = '#822433', fg="snow")
cellmake_label.place(x=53, y=50)

cellmake_menu = tk.StringVar(page3)
cellmake_options_list = ["Empty"]
# Create a dropdown Menu
cellmake_drop = tk.OptionMenu(page3, cellmake_menu, *cellmake_options_list)
cellmake_drop.configure(font = font_1, width=5, bd=0, highlightthickness=0, justify='center', bg = 'snow')
cellmake_drop.place(x=130, y=48)

cellmake_drop_list = root.nametowidget(cellmake_drop.menuname)
cellmake_drop_list.config(font=font_1)

cellmake_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                             command=lambda: explain(details_cellmake))
cellmake_explain.place(x=202, y=48)
######################
collapsing_label = tk.Label(page3, text="i_collapse", font = font_1, bg = '#822433', fg="snow")
collapsing_label.place(x=228, y=50)

collapsing_text = tk.StringVar()
collapsing_text.set(4)

textbox_collapasing = tk.Entry(page3, textvariable=collapsing_text, width=7, bd=0, highlightthickness=0, justify='center')
textbox_collapasing.place(x=298, y=52)

collapsing_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                               command=lambda: explain(details_collapsing))
collapsing_explain.place(x=338, y=48)
######################
category_label = tk.Label(page3, text="#category", font = font_1, bg = '#822433', fg="snow")
category_label.place(x=53, y=110)

category_text = tk.StringVar()
category_text.set('3')

textbox_category = tk.Entry(page3, textvariable=category_text, width=28, bd=0, highlightthickness=0, justify='center')
textbox_category.place(x=123, y=110)

category_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                             command=lambda: explain(details_category))
category_explain.place(x=320, y=108)
######################
NonCollapsible_label = tk.Label(page3, text="NonCollapsible", font = font_1, bg = '#822433', fg="snow")
NonCollapsible_label.place(x=53, y=180)

NonCollapsible_text = tk.StringVar()
NonCollapsible_text.set('0')

textbox_NonCollapsible = tk.Entry(page3, textvariable=NonCollapsible_text, width=24, bd=0, highlightthickness=0, justify='center')
textbox_NonCollapsible.place(x=160, y=180)

NonCollapsible_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                                   command=lambda: explain(details_noncollapsible))
NonCollapsible_explain.place(x=330, y=178)
#################
imputation_label = tk.Label(page3, text="i_imputation", font = font_1, bg = '#822433', fg="snow")
imputation_label.place(x=53, y=250)

imputation_menu = tk.StringVar(page3)
imputation_options_list = ["FHDI", "FEFI"]
# Create a dropdown Menu
imputation_drop = tk.OptionMenu(page3, imputation_menu, *imputation_options_list)
imputation_drop.configure(font = font_1, width=4, bd=0, highlightthickness=0, justify='center', bg = 'snow')
imputation_drop.place(x=140, y=250)

imputation_drop_list = root.nametowidget(imputation_drop.menuname)
imputation_drop_list.config(font=font_1)

imputation_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                               command=lambda: explain(details_imputation))
imputation_explain.place(x=200, y=250)

######################
donor_label = tk.Label(page3, text="i_donor", font = font_1, bg = '#822433', fg="snow")
donor_label.place(x=230, y=250)

donor_text = tk.StringVar()
donor_text.set(5)

textbox_donor = tk.Entry(page3, textvariable=donor_text, width=7, bd=0, highlightthickness=0, justify='center')
textbox_donor.place(x=284, y=250)

donor_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                          command=lambda: explain(details_donor))
donor_explain.place(x=330, y=248)
#################
variance_label = tk.Label(page3, text="i_var", font = font_1, bg = '#822433', fg="snow")
variance_label.place(x=50, y=320)

variance_menu = tk.StringVar(page3)
variance_options_list = ["Yes", "No"]
# Create a dropdown Menu
variance_drop = tk.OptionMenu(page3, variance_menu, *variance_options_list)
variance_drop.configure(font = font_1, width=4, bd=0, highlightthickness=0, justify='center', bg = 'snow')
variance_drop.place(x=90, y=320)

variance_drop_list = root.nametowidget(variance_drop.menuname)
variance_drop_list.config(font=font_1)

variance_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                             command=lambda: explain(details_variance))
variance_explain.place(x=150, y=320)
#################
vartype_label = tk.Label(page3, text="i_var_type", font = font_1, bg = '#822433', fg="snow")
vartype_label.place(x=180, y=320)

vartype_menu = tk.StringVar(page3)
vartype_options_list = ["Jackknife", "Linearization"]
# Create a dropdown Menu
vartype_drop = tk.OptionMenu(page3, vartype_menu, *vartype_options_list)
vartype_drop.configure(font = font_1, width=12, bd=0, highlightthickness=0, justify='center', bg = 'snow')
vartype_drop.place(x=255, y=320)

vartype_drop_list = root.nametowidget(vartype_drop.menuname)
vartype_drop_list.config(font=font_1)


vartype_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                            command=lambda: explain(details_var_type))
vartype_explain.place(x=345, y=320)

#################
merge_label = tk.Label(page3, text="i_merge", font = font_1, bg = '#822433', fg="snow")
merge_label.place(x=53, y=390)

merge_menu = tk.StringVar(page3)
merge_options_list = ["Yes", "No"]
# Create a dropdown Menu
merge_drop = tk.OptionMenu(page3, merge_menu, *merge_options_list)
merge_drop.configure(font = font_1, width=5, bd=0, highlightthickness=0, justify='center', bg = 'snow')
merge_drop.place(x=110, y=390)

merge_drop_list = root.nametowidget(merge_drop.menuname)
merge_drop_list.config(font=font_1)

merge_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433", 
                          command=lambda: explain(details_merge))
merge_explain.place(x=177, y=390)

######################
memory_label = tk.Label(page3, text="memory", font = font_1, bg = '#822433', fg="snow")
memory_label.place(x=210, y=390)

memory_text = tk.StringVar()
memory_text.set(8)

textbox_memory = tk.Entry(page3, textvariable=memory_text, width=10, bd=0, highlightthickness=0, justify='center')

textbox_memory.place(x=270, y=390)

memory_explain = tk.Button(page3, text="?", font = font_1, compound="center", highlightthickness=0, bd=0, bg='#822433', activebackground="#822433",
                           command=lambda: explain(details_memory))
memory_explain.place(x=330, y=388)


####################
def p3_set_default():
    if var_UP_FHDI.get() == 1:
        cellmake_menu.set("KNN")
        collapsing_text.set('4')
        category_text.set('3')
        NonCollapsible_text.set('0')
        imputation_menu.set("FHDI")
        donor_text.set('5')
        variance_menu.set("Yes")
        vartype_menu.set("Jackknife")
        merge_menu.set("Yes")
        memory_text.set('8')
    else:
        cellmake_menu.set("KNN")
        collapsing_text.set('4')
        category_text.set('3')
        NonCollapsible_text.set('0')
        imputation_menu.set("FHDI")
        donor_text.set('5')
        variance_menu.set("Yes")
        vartype_menu.set("Linearization")
        merge_menu.set("Yes")
        memory_text.set('8')


Back_p3 = tk.Button(page3, text="< Back ", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: prev_page(pages))
Back_p3.place(x=55, y=445)
Default_p3 = tk.Button(page3, text="Set Default", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: p3_set_default())
Default_p3.place(x=160, y=445)
Next_p3 = tk.Button(page3, text="Next >", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: next_page(pages, varName(page3),
var_UP_FHDI, cellmake_menu, collapsing_text, category_text, NonCollapsible_text,
imputation_menu, donor_text, variance_menu, vartype_menu, merge_menu, memory_text, analysis_var1, analysis_var2, analysis_var3, Output_text, var_intermediate,
MPI_text, column))
Next_p3.place(x=285, y=445)

pages.append(page3)

##############################################
##############################################
# Page 4
##############################################
##############################################
page4 = tk.Frame(root)
page4.configure(background='#822433')
page4.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions_p4 = tk.Label(page4, text="HPC Job Script", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions_p4.place(x=140, y=10)


######################
def Facility_call_back(var, index, mode):
    if Facility_text.get() == "Others":
        Jobname_input["state"] = tk.DISABLED
        Node_input["state"] = tk.DISABLED
        MPI_input["state"] = tk.DISABLED
        Time_input["state"] = tk.DISABLED
        sbatch_input["state"] = tk.NORMAL
        messagebox.showinfo('Warning',
                            'Please make sure you provide a directory to the job script that follows formats of other HPC facilities!')
    else:
        Jobname_input["state"] = tk.NORMAL
        Node_input["state"] = tk.NORMAL
        MPI_input["state"] = tk.NORMAL
        Time_input["state"] = tk.NORMAL
        sbatch_input["state"] = tk.DISABLED


Facility_label = tk.Label(page4, text='Facility', font = font_1, bg = '#822433', fg="snow")
Facility_label.place(x=70, y=50)

Facility_text = tk.StringVar(page4)
Facility_text.set("Condo2017")
Facility_text.trace_add('write', Facility_call_back)
Facility_options_list = ["Condo2017", "Others"]
# Create a dropdown Menu
Facility_drop = tk.OptionMenu(page4, Facility_text, *Facility_options_list)
Facility_drop.configure(font = font_1, width=20, bd = 0, highlightthickness=0, justify='center', bg = 'snow')
Facility_drop.place(x=135, y=48)

Facility_list = root.nametowidget(Facility_drop.menuname)
Facility_list.config(font = font_1)


######################
sbatch_label = tk.Label(page4, text="Job script diretory", font = font_1, bg = '#822433', fg="snow")
sbatch_label.place(x=70, y=116)

sbatch_text = tk.StringVar()
sbatch_text.set("./run.sbatch")
sbatch_input = tk.Entry(page4, textvariable=sbatch_text, width=17, bd = 0, highlightthickness=0, state=tk.DISABLED, justify='center', disabledbackground= 'gray')
sbatch_input.place(x=195, y=116)

######################
Job_label = tk.Label(page4, text="Job name", font = font_1, bg = '#822433', fg="snow")
Job_label.place(x=70, y=182)

Jobname_text = tk.StringVar()
Jobname_text.set("UP-FHDI")
Jobname_input = tk.Entry(page4, textvariable=Jobname_text, width=24, bd = 0, highlightthickness=0, justify='center')
Jobname_input.place(x=145, y=182)

######################
Node_label = tk.Label(page4, text="# Node", font = font_1, bg = '#822433', fg="snow")
Node_label.place(x=70, y=248)

Node_text = tk.StringVar()
Node_text.set('1')
Node_input = tk.Entry(page4, textvariable=Node_text, width=24, bd = 0, highlightthickness=0, justify='center')
Node_input.place(x=145, y=248)

######################
MPI_label = tk.Label(page4, text="# MPI tasks", font = font_1, bg = '#822433', fg="snow")
MPI_label.place(x=70, y=314)

MPI_input = tk.Entry(page4, textvariable=MPI_text, width=21, bd = 0, highlightthickness=0, justify='center')
MPI_input.place(x=162, y=314)

######################
Time_label = tk.Label(page4, text="Maximum runtime", font = font_1, bg = '#822433', fg="snow")
Time_label.place(x=70, y=380)

Time_text = tk.StringVar()
Time_text.set("00:00:10")
Time_input = tk.Entry(page4, textvariable=Time_text, width=16, bd = 0, highlightthickness=0, justify='center')
Time_input.place(x=198, y=380)

####################
Back_p4 = tk.Button(page4, text="< Back ", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: prev_page(pages))
Back_p4.place(x=70, y=445)
Next_p4 = tk.Button(page4, text="Submit", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: submit(
Facility_text, MPI_text, Jobname_text, Node_text, Time_text, sbatch_text,
PM, db, add_text, Input_text, menu, var_delimiter, separator_text, var_miss, special_text, var_UP_FHDI,
cellmake_menu, collapsing_text, category_text, NonCollapsible_text, imputation_menu, donor_text, variance_menu, vartype_menu,
merge_menu, memory_text, Output_text, var_intermediate, analysis_var1, analysis_var2, analysis_var3,
load_text, User, column, pages, framebox_text))
Next_p4.place(x=250, y=445)

pages.append(page4)


##############################################
##############################################
# Page final
##############################################
##############################################
page_final = tk.Frame(root)
page_final.configure(background='#822433')
page_final.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

instructions_final1 = tk.Label(page_final, text="Congratulations!", font=('Times New Roman', 16, 'bold'), fg="snow", bg = '#822433')
instructions_final1.place(x=120, y=10)

instructions_final2 = tk.Label(page_final, text="Your job has been successfully submitted!", font = font_1, bg = '#822433', fg="snow")
instructions_final2.place(x=70, y=73)

framebox_text = tk.StringVar()
framebox_widget = tk.LabelFrame(page_final, text="Notes", fg="snow", font = font_1, bg='#822433')
frame_widget = tk.Label(framebox_widget, textvariable=framebox_text, justify='left', font= font_1, bd=0, highlightthickness=0, bg='#822433')
framebox_widget.place(x=55, y=130)
frame_widget.pack()

cancel_p_final = tk.Button(page_final, text="Terminate the task", font = font_1, compound="center", bg='#fdc82f', bd=0, highlightthickness=0, activebackground="goldenrod4", command=lambda: terminate(root))
cancel_p_final.place(x=130, y=445)

pages.append(page_final)



##############################################
##############################################
# Main
##############################################
##############################################
pages[0].lift()
tk.mainloop()
