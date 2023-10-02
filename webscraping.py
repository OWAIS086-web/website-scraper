import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Text, messagebox, END, Button, Entry, Label, Toplevel
import webbrowser

def open_link(event):
    webbrowser.open(event.widget.cget("text"))

def scrape_website():
    url = url_entry.get()
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Get all text from the website
            data = soup.get_text()
            
            # Find all image tags and get their 'src' attribute (i.e., URL)
            images = soup.find_all('img')
            image_urls = [img['src'] for img in images if 'src' in img.attrs]
            
            text_w.delete(1.0, END)
            text_w.insert(END, "TEXT CONTENT:\n" + data)
            text_w.insert(END, "\n\nIMAGE URLS:\n")

            for image_url in image_urls:
                text_w.insert(END, image_url + '\n', 'link')

            # Configuring tag 'link' for URLs to make them clickable
            text_w.tag_configure("link", foreground="blue", underline=True)
            text_w.tag_bind("link", "<Button-1>", open_link)

        else:
            messagebox.showerror("Error!", f"Failed to fetch data. Status code: {response.status_code}")

    except Exception as e:
        messagebox.showerror("Error!", str(e))

# Setup GUI
root = Tk()
root.title("Universal Web Scraper")
root.geometry("800x600")

Label(root, text="Enter Website URL:").pack(pady=10)
url_entry = Entry(root, width=50)
url_entry.pack(pady=10)

Button(root, text="Scrape!", command=scrape_website).pack(pady=10)

text_w = Text(root, wrap="word", cursor="arrow")  # cursor="arrow" to prevent text widget from being editable
text_w.pack(pady=10, padx=10, fill="both", expand=True)

root.mainloop()
