import requests
from bs4 import BeautifulSoup
import threading
from tkinter import (Tk, Text, messagebox, Button, Entry, Label, Scrollbar,
                     Listbox, Toplevel, ttk, StringVar, IntVar, Checkbutton)
import random

class AdvancedWebScraper:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Web Scraper")
        self.root.geometry("1200x800")
        self.setup_ui()

    def setup_ui(self):
        # URL Entry
        Label(self.root, text="Enter Website URL:").pack(pady=10)
        self.url_entry = Entry(self.root, width=50)
        self.url_entry.pack(pady=10)

        # User Agent Dropdown
        self.user_agent_var = StringVar(self.root)
        self.user_agent_var.set(self.USER_AGENTS[0])
        self.dropdown = ttk.Combobox(self.root, textvariable=self.user_agent_var, values=self.USER_AGENTS, width=100)
        self.dropdown.pack(pady=10)

        # Checkbuttons
        self.scrape_images = IntVar()
        Checkbutton(self.root, text="Scrape Images URLs", variable=self.scrape_images).pack(pady=5)
        
        self.scrape_links = IntVar()
        Checkbutton(self.root, text="Scrape External Links", variable=self.scrape_links).pack(pady=5)

        # Depth Level
        Label(self.root, text="Depth Level (How many levels deep to scrape from the starting page):").pack(pady=10)
        self.depth_spinbox = ttk.Spinbox(self.root, from_=1, to=5, width=5)
        self.depth_spinbox.pack(pady=10)

        # Load Navigation & Scrape Button
        Button(self.root, text="Load Navigation", command=self.load_navigation).pack(pady=10)
        self.nav_list = Listbox(self.root)
        self.nav_list.pack(pady=10, fill="both", expand=True)
        Button(self.root, text="Scrape Selected Page", command=self.scrape_website).pack(pady=10)

        # Results Tab
        self.notebook = ttk.Notebook(self.root)
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Results")
        self.notebook.pack(pady=10, fill="both", expand=True)

        self.text_w = Text(self.results_tab, wrap="word", cursor="arrow")
        self.text_w.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar_y = Scrollbar(self.results_tab, orient="vertical", command=self.text_w.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.text_w.config(yscrollcommand=scrollbar_y.set)

    def load_navigation(self):
        base_url = self.url_entry.get()
        headers = {'User-Agent': self.user_agent_var.get()}

        try:
            response = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            self.nav_list.delete(0, "end")

            for link in soup.find_all('a'):
                title = link.text
                href = link.get('href')
                if href:
                    self.nav_list.insert("end", (title, href))

        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def scrape_website(self):
        selected_item = self.nav_list.curselection()
        if not selected_item:
            messagebox.showerror("Error!", "Please select a page from the navigation list to scrape.")
            return

        _, link = self.nav_list.get(selected_item)
        base_url = self.url_entry.get()
        if not link.startswith(("http", "www")):
            link = base_url + link

        depth_level = int(self.depth_spinbox.get())
        self.scrape_selected_url(link, depth_level)

    def scrape_selected_url(self, url, depth):
        headers = {'User-Agent': self.user_agent_var.get()}

        def worker():
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                data = soup.get_text()
                self.text_w.delete(1.0, 'end')
                self.text_w.insert("end", data + "\n")

                # Scrape image URLs
                if self.scrape_images.get():
                    self.text_w.insert("end", "=== Image URLs ===\n")
                    for img_tag in soup.find_all('img'):
                        img_url = img_tag.get('src')
                        self.text_w.insert("end", img_url + "\n")

                # Scrape external links
                if self.scrape_links.get():
                    self.text_w.insert("end", "=== External Links ===\n")
                    for a_tag in soup.find_all('a'):
                        href = a_tag.get('href')
                        if href and href.startswith("http"):
                            self.text_w.insert("end", href + "\n")

            except Exception as e:
                messagebox.showerror("Error!", str(e))

        thread = threading.Thread(target=worker)
        thread.start()

if __name__ == "__main__":
    root = Tk()
    scraper = AdvancedWebScraper(root)
    root.mainloop()
