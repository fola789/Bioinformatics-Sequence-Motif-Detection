from Bio import SeqIO
from Bio import ExPASy
from Bio import SwissProt
from tkinter import *
from tkinter import scrolledtext
import tkinter as tk
import re

def inspectArrangement(): #Method for user to input accession codes
    sct_result.delete('1.0', END)
    accession_codes  = txt_input_field.get("1.0",'end-1c')  #Stores user input into accession_codes
    accession_codes = accession_codes.replace(" ","")#Validation to remove spaces
    accession_codes  = accession_codes.split(",") #splits all inputted accession codes  
    for accession_code in accession_codes: #for every found accession code within the codes  
        sequence = sequenceRetrival(accession_code) #run the sequenceRetrival function and assign the  returned value to the sequence variable
        matchFinder(sequence, accession_code)#runs the matchfinder function with the sequence found

def sequenceRetrival(accession_code): #Method to retrieve sequence from accession codes
    handle = ExPASy.get_sprot_raw(accession_code)
    record = SwissProt.read(handle)
    handle.close()
    sequence = record.sequence
    return sequence 

def matchFinder(sequence, accession_code): #Method to inspect matches within each sequence
    matchs = re.finditer("(G|A)...(G)...(T|G)",str(sequence)) # Finds the matched regex within each fasta
    sct_result.insert(INSERT, accession_code + "\n")
    count = 0
    if matchs:
        for match in matchs:
            matchs_start = match.start()
            matchs_end = match.end()
            matchs_group = match.group()
            sct_result.insert(INSERT, "sequence: " + str(matchs_group) + "\n") 
            sct_result.insert(INSERT, "start: " + str(matchs_start) + "\n")
            sct_result.insert(INSERT, "end: " + str(matchs_end) + "\n")
            sct_result.insert(INSERT, "AT rich region from " + str(matchs_start) + " to " + str(matchs_end)+ "\n")
            count +=1
    if count == 0:    # if matches are empty responds with no matches found
        sct_result.insert(INSERT, "No matches found \n")   
    sct_result.insert(INSERT,"------------------------------------------------------ \n")   

if __name__ == '__main__': # Entry point for application
    window = tk.Tk() #Creates tkinter object

    window.title("Alzheimer’s Amyloid  Motif Detection Tool") # Settting up window and name
    window.geometry('750x500')
    window.configure(background = 'Grey')
    window.resizable(width=FALSE, height=FALSE)

    background_image = PhotoImage(file="background.png")
    background_label = Label(window, image=background_image)
    background_label.place(x=0,y=0, relwidth=1, relheight=1)

    lbl_instruction = Label(window, text="Input UniProt accession code below as comma seperated e.g. P012345,P012345:", font = ('articulat',13,'bold')) #Creates and places instruction label
    lbl_instruction.grid(column=0, row=1, padx=40, pady=10)

    txt_input_field = Text(window) #Creates and places input field
    txt_input_field.grid(column=0, row=2, padx=40, pady=10, sticky="W")
    txt_input_field.config(width=80, height = 6)

    sct_result = scrolledtext.ScrolledText(window) #Creates and plces result field
    sct_result.grid(column=0, row=4, padx=40, pady=10, sticky="W")
    sct_result.config(width=80, height=12)

    btn_run = Button(window, width=93, text="Find Motif", command=inspectArrangement) #Creates and places button and binds it to inspect arrangment method
    btn_run.grid(column=0, row=3, padx=0, pady=10)
    btn_run.config(width=64)

    window.mainloop() #Stops the window from closing