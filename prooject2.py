from tkinter import *
from tkinter import ttk
from transformers import MarianMTModel, MarianTokenizer
import torch

# Load the model and tokenizer only once
model_name = 'Helsinki-NLP/opus-mt-ru-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

root = Tk()
root.geometry("650x600")
root.title("Russian to English Translator")
root.config(bg='#0A192F')  # Dark navy background

# Title Label
tittle = Label(root, text='Russian to English Translator', bd=8, relief=GROOVE,
               font=("times new roman", 28, "bold"), bg='#112240', fg='#64FFDA')  # Deep space blue with neon text
tittle.pack(side=TOP, fill=X)

# Frame for Input/Output
in_frame = Frame(root, bd=3, relief=RIDGE, bg='#233554')  # Darker slate blue
in_frame.place(x=10, y=70, width=630, height=520)

# Russian Text Label
label1 = Label(in_frame, text='Enter Russian Text', font=("times new roman", 20, "bold"),
               bg='#233554', fg='#64FFDA')
label1.pack()

# Russian Input Text Box
input_text = Text(in_frame, width=50, height=4, font=("times new roman", 15),
                  bd=5, relief=GROOVE, bg='#F0F0F0', fg='black')
input_text.pack()


# Translation Logic
def translate_text():
    russian_text = input_text.get("1.0", END).strip()
    if russian_text:
        inputs = tokenizer(russian_text, return_tensors="pt", padding=True)
        with torch.no_grad():
            translated = model.generate(**inputs)
        english_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        output_text.delete("1.0", END)
        output_text.insert(END, english_text)

# Clear Logic
def clear_text():
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)

# Translate Button
translate_btn = Button(in_frame, text='TRANSLATE', command=translate_text,
                       font=("times new roman", 15, "bold"), bg='#64FFDA', fg='#0A192F',
                       activebackground='#52e0c4', activeforeground='#0A192F')
translate_btn.place(x=160, y=250)

# Clear Button
clear_btn = Button(in_frame, text='CLEAR', command=clear_text,
                   font=("times new roman", 15, "bold"), bg='#64FFDA', fg='#0A192F',
                   activebackground='#52e0c4', activeforeground='#0A192F')
clear_btn.place(x=340, y=250)

# English Translation Label
label3 = Label(in_frame, text='English Translation', font=("times new roman", 20, "bold"),
               bg='#233554', fg='#64FFDA')
label3.place(x=200, y=320)

# Output Text Box
output_text = Text(in_frame, width=46, height=4, font=("arial", 15),
                   bd=5, relief=GROOVE, pady=10, bg='#F0F0F0', fg='black')
output_text.place(x=50, y=360)

root.mainloop()
