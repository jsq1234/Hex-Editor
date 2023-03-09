#! /usr/bin/env python
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

label = "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F"

hex_string = {}

root = tk.Tk()
root.title("Hex Editor")
root.resizable(False,False)
ff = ('Ubuntu Mono',16)
offset_var = tk.StringVar()
# Frame Creation
frame = tk.Frame(root,padx=20, pady=5)
# Text Boxes
text_scroll = tk.Scrollbar(frame,width=28)
left = tk.Text(frame, font=ff, width=47,padx=10, pady=5,border=10, yscrollcommand=text_scroll.set)
right = tk.Text(frame, font= ff, width=16,padx=10, pady=5, border=10, yscrollcommand=text_scroll.set)
lbl_offset = tk.Text(frame,font=ff,width=8, pady=5 ,padx=10, border=10, yscrollcommand=text_scroll.set)

# Labels 
lbl_address = tk.Label(frame,font=ff,text="Address",justify=tk.LEFT)
lbl_hex_string = tk.Label(frame,font=ff,text=label)
lbl_last = tk.Label(frame,font=ff,text="Decoded Text")
var = tk.StringVar()
entry = tk.Entry(root,textvariable=var,font=ff)
# Creating a scroll bar


# Placing all the widgets to the application
entry.grid(row=0,column=0,sticky = tk.E + tk.W)
frame.grid(row=1,column=0, sticky=tk.N + tk.S)
lbl_address.grid(row=0,column=0)
lbl_hex_string.grid(row=0,column=1)
lbl_last.grid(row=0,column=2)


lbl_offset.grid(row=1,column=0,sticky=tk.N + tk.S)
left.grid(row=1,column=1,sticky=tk.N + tk.S)
right.grid(row=1,column=2,sticky=tk.N + tk.S)

right.tag_config('color',foreground='white', background='black')
left.tag_config('remove', foreground='red')
right.tag_config('remove', foreground='red')
# Events

        
def func(e : tk.Event):
    index = left.index(tk.INSERT)
    index1 = index.split('.')
    index2 = index1[0] + "." + str(int(int(index1[1])/3) + 1)

    if e.keysym.upper() == 'DOWN':
        index3 = str(int(index1[0])+1) + "." + str(int(int(index1[1])/3) + 1)
        right.tag_remove('color', ("%d.%d") % (int(index1[0]), 0), ("%d.%d") % (int(index1[0]),16))
        right.tag_add('color',index3 + '-1c',index3)
        
        
    elif e.keysym.upper() == "UP":
        index3 = str(int(index1[0])-1*( int(index1[0]) >= 2 )) + "." + str(int(int(index1[1])/3) + 1)
        right.tag_remove('color',("%d.%d") % (int(index1[0]), 0), ("%d.%d") % (int(index1[0]),16))
        right.tag_add('color',index3 + '-1c',index3)

    elif e.keysym.upper() == "RIGHT":
        j = int(int(index1[1])/3) + 1
        index3 = str(index1[0]) + "." + str(j + 1)
        left.mark_set(tk.INSERT,index + "+2c")

        if j == 16:
            right.tag_remove('color',("%d.%d") % (int(index1[0]), 0), ("%d.%d") % (int(index1[0]),17))
            index3 = str(int(index1[0])+1) + "." + "1"
            right.tag_add('color', index3 + '-1c', index3)
        else:
            right.tag_remove('color',("%d.%d") % (int(index1[0]), 0), ("%d.%d") % (int(index1[0]),j+1))
            right.tag_add('color', index3 + '-1c', index3)
    
    elif e.keysym.upper() == "LEFT":
        j = int(int(index1[1])/3)+1
        index3 = str(index1[0]) + "." + str(j-1)
        left.mark_set(tk.INSERT, index + "-2c")
        
        if j == 1:
            i = str(int(index1[0]) - 1) + ".16"
            right.tag_add('color',i + '-1c',i)
        right.tag_remove('color', ('%d.%d') % (int(index1[0]),j-1), ('%d.%d') % (int(index1[0]), 17))
        right.tag_add('color',index3 + '-1c', index3)
    
    elif e.keysym.upper() == "BACKSPACE":
        left.delete(index + "-2c", index)
        left.insert(index + "-2c","000")
        left.tag_add('remove',index + "-2c",index)
        right.delete(index2 + "-1c", index2)
        right.insert(index2 + "-1c", "R")
        right.tag_add("remove",index2 + "-1c",index2)
    
    else:
        return "break"
    
    

def func2(e : tk.Event):
    index = left.index(tk.INSERT)
    entry.focus()
    t = ""
    def getVar(ee : tk.Event):
        t = var.get()    
        int_t = int(t,base=16)

        if 0 <= int_t <= 255:
            t = t.upper()
            t = t.rstrip()
            left.focus()
            left.mark_set(tk.INSERT,index)
            left.replace(index + '-2c', index,t)

            index1 = index.split('.')
            index1 = index1[0] + "." + str(int(int(index1[1])/3) + 1)
            
            if 33 <= int_t <= 126 or chr(int_t) == ' ':
                
                right.replace(index1 + '-1c',index1,chr(int_t))
            else:
                right.replace(index1 + '-1c',index1,'@')
        else:
            messagebox.showerror(title="Invalid Range",message="The value entered should be in range 00-FF")



    entry.bind('<Return>',getVar)

left.bind('<Key>',func)
left.bind('<Control-slash>',func2)
text_scroll.grid(row=1,column=3, sticky=tk.N + tk.S)

# Configuring Scroll Bar
def multiple_yview(*args):
    t1, t2 = args
    left.yview(*args)
    right.yview(*args)
    lbl_offset.yview(*args)
    
    

text_scroll.config(command=multiple_yview)

left.delete('1.0',tk.END)
right.delete('1.0',tk.END)

filepath = filedialog.askopenfilename(initialdir = '/home/manan/files/', title='Select file',
                                    filetypes = (('text files','*.txt'),('all files','*')))

with open(filepath,'rb') as file: 
    offset = 0
    t = ""
    while True:
        bytestream = file.read(16)
        
        if len(bytestream) == 0: break

        str1 = ""
        str2 = ""

        t += hex(offset)[2:].zfill(8).upper()
        t += "\n"
        offset += 16
        
        for byte in bytestream:
            hex_val = hex(byte)[2:]
            if ( 33 <= byte and byte <= 126 ) or byte == ord(' '):
                str2 += chr(byte)
            else:
                str2 += "@"
            
            if len(hex_val) == 1:
                hex_val = '0' + hex_val
            hex_val = hex_val.upper()
            str1 += hex_val + " "
        
        str1 = str1.rstrip()
        str1 += "\n"
        str2 += "\n"
        left.insert(tk.INSERT,str1)
        right.insert(tk.INSERT,str2)
        hex_string[str1] = str2

    t = t.rstrip()
    lbl_offset.insert(tk.INSERT,t)
    lbl_offset.configure(state=tk.DISABLED)
    
    
left.focus()
left.mark_set(tk.INSERT,"1.2")
right.tag_add('color',"1.0","1.1")

root.mainloop()



