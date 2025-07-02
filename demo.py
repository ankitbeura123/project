# Importing required modules
from tkinter import *                 # For GUI components
from tkinter import ttk              # For themed widgets like Combobox
from transformers import MarianMTModel, MarianTokenizer  # For pre-trained translation models
import torch                         # For model inference and tensor operations

# Load Russian to English model and tokenizer
model_name_ru_en = 'Helsinki-NLP/opus-mt-ru-en'
tokenizer_ru_en = MarianTokenizer.from_pretrained(model_name_ru_en)
model_ru_en = MarianMTModel.from_pretrained(model_name_ru_en)

# Load English to Russian model and tokenizer
model_name_en_ru = 'Helsinki-NLP/opus-mt-en-ru'
tokenizer_en_ru = MarianTokenizer.from_pretrained(model_name_en_ru)
model_en_ru = MarianMTModel.from_pretrained(model_name_en_ru)

# Initialize main application window
root = Tk()
root.geometry("650x600")                 # Set size of the window
root.title("Translator")                 # Set window title
root.config(bg='#0A192F')                # Set background color

# Title label at the top
tittle = Label(root, text='Translator', bd=8, relief=GROOVE,
                font=("times new roman", 28, "bold"), bg='#112240', fg='#64FFDA')
tittle.pack(side=TOP, fill=X)           # Pack title label at the top filling X-axis

# Frame to hold input/output and controls
in_frame = Frame(root, bd=3, relief=RIDGE, bg='#233554')
in_frame.place(x=10, y=70, width=630, height=520)

# Label for translation direction selection
direction_label = Label(in_frame, text='Select Translation Direction:', 
                        font=("times new roman", 14, "bold"),
                        bg='#233554', fg='#64FFDA')
direction_label.pack(pady=5)

# Dropdown (Combobox) to choose translation direction
translation_direction = StringVar()
translation_direction.set("Russian to English")  # Default selection

direction_chooser = ttk.Combobox(in_frame, textvariable=translation_direction,
                                 values=["Russian to English", "English to Russian"],
                                 font=("times new roman", 12), state="readonly")
direction_chooser.pack(pady=5)

# Function to update UI labels based on translation direction
def update_labels(*args):
    current_direction = translation_direction.get()
    if current_direction == "Russian to English":
        label1.config(text='Enter Russian Text')
        label3.config(text='English Translation')
    else:
        label1.config(text='Enter English Text')
        label3.config(text='Russian Translation')
    clear_text()  # Clear text boxes when direction changes

# Automatically update labels when dropdown value changes
translation_direction.trace_add('write', update_labels)

# Label above input text area
label1 = Label(in_frame, text='Enter Russian Text', font=("times new roman", 20, "bold"),
                bg='#233554', fg='#64FFDA')
label1.pack()

# Input text box
input_text = Text(in_frame, width=50, height=4, font=("times new roman", 15),
                  bd=5, relief=GROOVE, bg='#F0F0F0', fg='black')
input_text.pack()

# Function to perform translation using selected direction
def translate_text():
    text_to_translate = input_text.get("1.0", END).strip()  # Read input
    if text_to_translate:
        current_direction = translation_direction.get()

        # Select appropriate model and tokenizer based on direction
        if current_direction == "Russian to English":
            tokenizer = tokenizer_ru_en
            model = model_ru_en
        else:
            tokenizer = tokenizer_en_ru
            model = model_en_ru

        # Tokenize input text
        inputs = tokenizer(text_to_translate, return_tensors="pt", padding=True)
        # Perform translation (inference) without computing gradients
        with torch.no_grad():
            translated = model.generate(**inputs)
        # Decode output tokens into human-readable text
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        # Display translated text in output box
        output_text.delete("1.0", END)
        output_text.insert(END, translated_text)

# Function to clear both input and output text areas
def clear_text():
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)

# Button to trigger translation
translate_btn = Button(in_frame, text='TRANSLATE', command=translate_text,
                        font=("times new roman", 15, "bold"), bg='#64FFDA', fg='#0A192F',
                        activebackground='#52e0c4', activeforeground='#0A192F')
translate_btn.place(x=160, y=290)

# Button to clear text boxes
clear_btn = Button(in_frame, text='CLEAR', command=clear_text,
                    font=("times new roman", 15, "bold"), bg='#64FFDA', fg='#0A192F',
                    activebackground='#52e0c4', activeforeground='#0A192F')
clear_btn.place(x=340, y=290)

# Label above output text area
label3 = Label(in_frame, text='English Translation', font=("times new roman", 20, "bold"),
                bg='#233554', fg='#64FFDA')
label3.place(x=200, y=360)

# Output text box
output_text = Text(in_frame, width=46, height=4, font=("arial", 15),
                    bd=5, relief=GROOVE, pady=10, bg='#F0F0F0', fg='black')
output_text.place(x=50, y=400)

# Initialize labels based on default direction
update_labels()

# Start the main GUI loop
root.mainloop()
