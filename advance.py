import requests
from bs4 import BeautifulSoup
import threading
from tkinter import (Tk, Text, messagebox, Button, Entry, Label, Scrollbar, Listbox, Toplevel, ttk, StringVar)
from stem import Signal
from stem.control import Controller

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
        
        self.setup_tor()
        self.setup_ui()

    def setup_tor(self):
        # Setup stem to route through the local Tor process
        self.session = requests.session()
        self.session.proxies = {'http':  'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

    def setup_ui(self):
        self.user_agent_var = StringVar(self.root)
        self.user_agent_var.set(self.USER_AGENTS[0])
        
        Label(self.root, text="Enter Website URL:").pack(pady=10)
        self.url_entry = Entry(self.root, width=50)
        self.url_entry.pack(pady=10)
        
        Label(self.root, text="User Agent:").pack(pady=10)
        self.user_agent_dropdown = ttk.Combobox(self.root, textvariable=self.user_agent_var, values=self.USER_AGENTS, width=80)
        self.user_agent_dropdown.pack(pady=10)
        
        Button(self.root, text="Load Navigation", command=self.load_navigation).pack(pady=10)
        self.nav_listbox = Listbox(self.root)
        self.nav_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.nav_listbox.bind('<Double-Button-1>', self.navigate_to_link)
        
        self.text_w = Text(self.root, wrap="word", cursor="arrow")
        self.text_w.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.scroll_y = Scrollbar(self.root, orient="vertical", command=self.text_w.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.text_w.config(yscrollcommand=self.scroll_y.set)

    def load_navigation(self):
        base_url = self.url_entry.get()
        headers = {'User-Agent': self.user_agent_var.get()}
        response = self.session.get(base_url, headers=headers)
        
        if response.status_code != 200:
            messagebox.showerror("Error!", f"Failed to fetch data. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, "html.parser")
        nav_links = soup.find_all('a')
        self.nav_listbox.delete(0, 'end')
        
        for link in nav_links:
            if link.get('href'):
                self.nav_listbox.insert('end', link.get('href'))

    def navigate_to_link(self, event):
        link = self.nav_listbox.get(self.nav_listbox.curselection())
        self.scrape_website(link)

    def scrape_website(self, link=None):
        if not link:
            link = self.url_entry.get()
        
        headers = {'User-Agent': self.user_agent_var.get()}
        response = self.session.get(link, headers=headers)
        
        if response.status_code != 200:
            messagebox.showerror("Error!", f"Failed to fetch data. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, "html.parser")
        data = soup.get_text()
        self.text_w.delete(1.0, "end")
        self.text_w.insert("end", data + "\n")

if __name__ == "__main__":
    root = Tk()
    scraper = AdvancedWebScraper(root)
    root.mainloop()
