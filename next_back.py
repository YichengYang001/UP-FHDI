#Description-----------------------------------------------------------------
#Forward to the next page or go back to the previous page in GUI
#
#
#Last modified date: Jan 21, 2023
#Python code written by Dr. Yang, and Dr. Li
#All rights reserved
#//-----------------------------------------------------------------


from tkinter import messagebox


def next_page(pages, page_name, 
var_UP_FHDI, cellmake_menu, collapsing_text, category_text, NonCollapsible_text, 
imputation_menu, donor_text, variance_menu, vartype_menu, merge_menu, memory_text, analysis_var1, analysis_var2, analysis_var3, Output_text, var_intermediate,
MPI_text, column):
    # move the first page to the end of the list,
    # then show the first page in the list

    Parameter_list = []

    if (page_name == "page2"):
        Parameter_list = [var_UP_FHDI.get()]
    if (page_name == "page3"):
        Parameter_list = [len(cellmake_menu.get()), len(collapsing_text.get()), len(category_text.get()),
                          len(NonCollapsible_text.get()), len(imputation_menu.get()),
                          len(donor_text.get()), len(variance_menu.get()), len(vartype_menu.get()),
                          len(merge_menu.get()), len(memory_text.get())]
    if(page_name == "page5"):
        parameter_sum = analysis_var1.get() + analysis_var2.get() + analysis_var3.get()
        Parameter_list = [len(Output_text.get()), var_intermediate.get(), parameter_sum]

    #print("Parameter_list: ", *Parameter_list)
    #print("next len is ", len(Parameter_list))

    flag = 1
    for x in Parameter_list:
        if x == 0:
            flag = 0

    if page_name == "page2":
        if int(MPI_text.get()) >= column.get():
            messagebox.showerror("showerror", "# MPI tasks must be less than the number of variables in input data. Please go back to input configuration page and reduce # MPI tasks!")
            return

    #print("next flag is ", flag)
    if (flag == 1):
        page = pages.pop(0)
        pages.append(page)
        pages[0].lift()
    else:
        messagebox.showerror("showerror", "Please fill in all parameters in the current page!")
        return



def next_first_page(pages, page_name,
var_miss, var_delimiter, Input_text, menu, separator_text, MPI_text, special_text, column, lablegrame_text):
    # move the first page to the end of the list,
    # then show the first page in the list
    #print("page_number after is ", page_name)
    Parameter_list = []
    if (page_name == "page1"):
        #print("var_delimiter is", var_delimiter.get())
        if (var_miss.get() != 4):
            if (var_delimiter.get() == 4):
                Parameter_list = [len(Input_text.get()), len(menu.get()), len(separator_text.get()), var_miss.get(),
                                  MPI_text.get()]
            if (var_delimiter.get() != 4):
                Parameter_list = [len(Input_text.get()), len(menu.get()), var_delimiter.get(), var_miss.get(),
                                  MPI_text.get()]
        if (var_miss.get() == 4):
            if (var_delimiter.get() == 4):
                Parameter_list = [len(Input_text.get()), len(menu.get()), len(separator_text.get()),
                                  len(special_text.get()), MPI_text.get()]
            if (var_delimiter.get() != 4):
                Parameter_list = [len(Input_text.get()), len(menu.get()), var_delimiter.get(), len(special_text.get()),
                                  MPI_text.get()]

    #print(*Parameter_list)
    #print("next len is ", len(Parameter_list))

    flag = 1
    for x in Parameter_list:
        if x == 0:
            flag = 0
        if x == "":
            flag = 0

    #print("next flag is ", flag)
    if (flag == 1):
        page = pages.pop(0)
        pages.append(page)
        pages[0].lift()
    else:
        messagebox.showerror("showerror", "Please fill in all parameters in the current page!")
        return

    if (var_delimiter.get() == 1):
        delimeter_temp = ','
    if (var_delimiter.get() == 2):
        delimeter_temp = '\t'
    if (var_delimiter.get() == 3):
        delimeter_temp = ' '
    if (var_delimiter.get() == 4):
        delimeter_temp = separator_text.get()

    try:
        file = open(Input_text.get())
    except IOError:
        print("Input directory is not accessible when finding the number of column!")
        return

    #print("here menu is ", menu.get())
    if (menu.get() == "Yes"):
        line1 = file.readline()
    line = file.readline()

    words = line.split(delimeter_temp)
    #print('words:' , words)
    column.set(len(words))
    #print("Recomd MPI_text is ", int(MPI_text.get()))
    #print("Recomd column is ", column.get())
    if MPI_text.get() == "":
        #print("I'm here!")
        return
    elif int(MPI_text.get()) > column.get():
        method_UP_FHDI = "P-FHDI"
        #print("Set ", method_UP_FHDI)
    else:
        method_UP_FHDI = "UP-FHDI"
        #print("Set ", method_UP_FHDI)

    message1 = " The number of variables in input data is " + str(column.get())
    message2 = " The number of requested MPI tasks is " + MPI_text.get()
    message3 = " Therefore, we recommand " + method_UP_FHDI + " to cure "
    message4 = " your incomplete data"
    message = message1 + '\n' + message2 + '\n' + '\n' + message3 + '\n' + message4
    lablegrame_text.set(message)
    file.close()





def prev_first_page(pages, PM):
    # move the last page in the list to the front of the list,
    # then show the first page in the list.
    PM.set(1)
    page = pages.pop(-1)
    pages.insert(0, page)
    pages[0].lift()

def prev_page(pages):
    # move the last page in the list to the front of the list,
    # then show the first page in the list.
    page = pages.pop(-1)
    pages.insert(0, page)
    pages[0].lift()



