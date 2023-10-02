import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Text, messagebox, END, Button, Entry, Label

def scrape_website():
    url = url_entry.get()
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Get all text from the website
            data = soup.get_text()
            
            text_w.delete(1.0, END)
            text_w.insert(END, data)
        else:
            messagebox.showerror("Error!", f"Failed to fetch data. Status code: {response.status_code}")

    except Exception as e:
        messagebox.showerror("Error!", str(e))

# Setup GUI
root = Tk()
root.title("Universal Web Scraper")
root.geometry("600x500")

Label(root, text="Enter Website URL:").pack(pady=10)
url_entry = Entry(root, width=50)
url_entry.pack(pady=10)

Button(root, text="Scrape!", command=scrape_website).pack(pady=10)

text_w = Text(root, wrap="word")
text_w.pack(pady=10, padx=10, fill="both", expand=True)

root.mainloop()
