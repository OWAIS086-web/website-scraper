import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Text, messagebox, Button, Entry, Label, Scrollbar, Canvas
import threading
from random import choice

USER_AGENTS = [
    # List of user agents. Add more if needed.
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
]


def get_random_user_agent():
    return choice(USER_AGENTS)


def scrape_website():
    def worker():
        base_url = url_entry.get()
        headers = {
            'User-Agent': get_random_user_agent()
        }

        try:
            # Empty the text widget
            text_w.delete(1.0, "end")

            response = requests.get(base_url, headers=headers)
            if response.status_code != 200:
                messagebox.showerror("Error!", f"Failed to fetch data. Status code: {response.status_code}")
                return

            soup = BeautifulSoup(response.content, "html.parser")

            # Get navbar links
            navbar = soup.find('nav')
            if navbar:
                page_links = [link['href'] for link in navbar.find_all('a', href=True) if link['href']]
            else:
                page_links = [base_url]

            for link in page_links:
                if not link.startswith("http"):
                    link = base_url + link

                response = requests.get(link, headers=headers)
                if response.status_code != 200:
                    continue

                page_soup = BeautifulSoup(response.content, "html.parser")

                # Extract all text from the page
                data = page_soup.get_text()
                text_w.insert("end", f"--- Data from {link} ---\n")
                text_w.insert("end", data + "\n\n")

                # Extract image URLs
                for img_tag in page_soup.find_all('img'):
                    img_url = img_tag.get('src')
                    if not img_url.startswith("http"):
                        img_url = base_url + img_url

                    text_w.insert("end", f"Image URL: {img_url}\n")

        except Exception as e:
            messagebox.showerror("Error!", str(e))

    thread = threading.Thread(target=worker)
    thread.start()


# Setup GUI
root = Tk()
root.title("Universal Web Scraper")
root.geometry("900x700")

Label(root, text="Enter Website URL:").pack(pady=10)
url_entry = Entry(root, width=50)
url_entry.pack(pady=10)

Button(root, text="Scrape!", command=scrape_website).pack(pady=10)

text_w = Text(root, wrap="word", cursor="arrow")
text_w.pack(pady=10, padx=10, fill="both", expand=True)

scroll_y = Scrollbar(root, orient="vertical", command=text_w.yview)
scroll_y.pack(side="right", fill="y")
text_w.config(yscrollcommand=scroll_y.set)

root.mainloop()
