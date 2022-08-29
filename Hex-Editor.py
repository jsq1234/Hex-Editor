
from tkinter import *
from tkinter import filedialog
import tkinter

ACCEPTED = [
    '0', '1', '2','3','4','5','6','7','8','9','a','b','c','d','e','f'
]
 
# Event Handler
buffer = ''
def handle_input(s):
    right.configure(state = tkinter.NORMAL)
    global buffer
    if s.char in set(ACCEPTED) or s.keysym.lower() == 'space':
        buffer += s.char
        
    elif s.keysym.lower() in {"delete"}:
        right.delete(
            left.index(tkinter.INSERT) + "-1c" * (s.keysym.lower() == "backspace"))

    elif s.keysym.lower() in {"left","down","right","up"}:
        pass

    # This is the part I'm missing.
    else:
        print(s.keysym.lower())
        if(len(buffer) == 2):
            right.insert(left.index(tkinter.INSERT),buffer)
            buffer = ''
        return "break"

    right.configure(state = tkinter.DISABLED)

count = 0
def handle_remove(e):
    global count 
    right.configure(state = tkinter.NORMAL)
    
    

IndexDict = {}
def open_file():
    global IndexDict
    left.configure(state=tkinter.NORMAL)
    right.configure(state=tkinter.NORMAL)
    left.delete('1.0',END)
    right.delete('1.0',END)

    filepath = filedialog.askopenfilename(initialdir = '/home/manan/Desktop', title='Select file',
                                    filetypes = (('text files','*.txt'),('all files','*.*')))
    bytes_count = 0
    with open(filepath,'rb') as f1:
        charList = []
        line1 = 1
        char1 = 0
        char2 = 0
        while True:
            byte = f1.read(1)
            if len(byte) == 0:
                break
            bytes_count += 1
            ASCII = ord(byte)

            key = str(line1) + '.' + str(char1)
            value = str(line1) + '.' + str(char2)
            IndexDict[key] = value
            char1 += 3
            char2 += 1

            if(bytes_count==16):
                line1 +=1
                char1 = 0
                char2 = 0
                left.insert(key, f"{ASCII:02x}\n")
                right.insert(value, byte)
                right.insert(END,'\n')
                bytes_count = 0
            else:
                left.insert(key, f"{ASCII:02x} ")
                right.insert(value, byte)
    right.config(state=tkinter.DISABLED)
    left.config(state=tkinter.DISABLED)

            


root = Tk()

root.maxsize(550,500)
root.resizable(False,False)

#Widgets
frame = Frame(root, width = 16*3 + 50, height = 30, borderwidth=1, relief='solid')
left = Text(frame, width=16*3 - 1, height=25, bg='brown', fg = 'white', insertwidth=5, state = tkinter.DISABLED)
right = Text(frame, width=16, height=25, bg='brown', fg='white', state=tkinter.DISABLED)
hex_text = '00  01  02  03  04  05  06  07  08  09  0A  0B  0C  0D  0E  0F'
hex_label = Label(frame, text= hex_text, width=16*3, anchor='w')
decoded_label = Label(frame, text='Decoded Text')

#Menu Bar
menu_bar = Menu(root, font = ('Arial', 11) )

file = Menu(menu_bar, tearoff= 0)
menu_bar.add_cascade(label='File',menu = file)
file.add_command(label='Open', command = open_file)
file.add_command(label='Exit', command = root.destroy)

#Putting Widgets On Screen

frame.grid(row=1, column=0)
hex_label.grid(row=0, column=0)
decoded_label.grid(row=0, column=1)
left.grid(row=1, column=0, rowspan=4)
right.grid(row=1, column=1, rowspan=4)


#Binding Events With Widget
left.bind('<BackSpace>', handle_remove)        
left.bind('<Key>', handle_input)

root.config(menu= menu_bar)
root.mainloop()