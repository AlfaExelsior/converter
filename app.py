import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from docx import Document
from youtube_transcript_api import YouTubeTranscriptApi

def docx_to_txt(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def pdf_to_txt(pdf_file):
    pdf = PdfReader(pdf_file)
    return "\n".join([page.extract_text() for page in pdf.pages])

def url_to_txt(url):
    if 'youtube.com' in url:
        video_id = url.split('=')[-1]  
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([t['text'] for t in transcript]) 
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.select('p')  
        text = '\n'.join(p.get_text() for p in paragraphs)  
    return text

def convert():
    file_path_or_url = entry.get()
    if not file_path_or_url:
        messagebox.showerror("Error", "Please enter a file path or URL")
        return

    try:
        if file_path_or_url.endswith('.docx'):
            text = docx_to_txt(file_path_or_url)
            output_file = file_path_or_url.replace('.docx', '.txt')
        elif file_path_or_url.endswith('.pdf'):
            text = pdf_to_txt(file_path_or_url)
            output_file = file_path_or_url.replace('.pdf', '.txt')
        elif file_path_or_url.startswith('http'):
            text = url_to_txt(file_path_or_url)
            output_file = 'output.txt'
        else:
            messagebox.showerror("Error", "Unsupported file type or URL")
            return

        with open(output_file, 'w') as f:
            f.write(text)

        messagebox.showinfo("Success", f"Text successfully written to {output_file}")
        entry.delete(0, tk.END) 
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Text Converter")
root.geometry("500x200")  
root.configure(bg='black')  

frame = tk.Frame(root, bg='black')
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Enter file path or URL:", bg='black', fg='green', font=("Courier", 16))
label.pack()

entry = tk.Entry(frame, width=50, font=("Courier", 14), fg='green', insertbackground='green')
entry.pack(padx=10, pady=10)

button = tk.Button(frame, text="Convert", command=convert, bg='green', fg='black', font=("Courier", 14), activebackground='darkgreen')
button.pack()

root.mainloop()
