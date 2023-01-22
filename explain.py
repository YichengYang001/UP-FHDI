#Description-----------------------------------------------------------------
# Explain UP-FHDI parameters in detail by clicking question-mark buttons
#
#
#Last modified date: Jan 21, 2023
#Python code written by Dr. Yang, and Dr. Li
#All rights reserved
#//-----------------------------------------------------------------

from tkinter import messagebox

details_cellmake = 'Users can either adopt the cell collapsing method to generate artificial donors or the k-nearest neighbor (KNN) method to find deficient donors in cell construction'
details_collapsing = 'Users can activate the sure independent screening (SIS) by a user-defined number of selected variables. ' \
                     'i_collapsing > 0 activates SIS to reduce all variables to a user-defined number of selected variables. Otherwise, SIS is turned off by setting i_option_collaspsing = 0.'
details_category = 'A vector indicates the number of total categories per variable. The maximum number of categories is 35 due to nine integers (1-9) and twenty-six alphabet letters (a-z).'
details_noncollapsible = 'A vector indicates non-collapsible categorical variables. Zero indicates a variable is collapsible categorical, or continuous. One indicates a variable is non-collapsible and categorical.'
details_imputation = 'Users can perform the fully-efficient fractional imputation (FEFI) or the fractional hot-deck imputation (FHDI)'
details_donor = 'Users can adopt a user-defined integer as the number of donors used to fill in each missing item. The past literature recommends five as the default value after detailed case studies.'
details_variance = 'Users can perform variance estimation or skip it'
details_var_type = 'Users can adopt the Jackknife variance estimation or the linearized variance estimation'
details_merge = 'Users can turn on the fixed seed for reproducible results or turn on the standard random seed generator'
details_memory = 'Available memory in gigabyte per MPI task = Total memory in gigabyte per node / Number of MPI tasks per node.'


def explain(details):
    MsgBox = messagebox.showinfo('Explanations', details)