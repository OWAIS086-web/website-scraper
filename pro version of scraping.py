import requests
from bs4 import BeautifulSoup
import threading
from tkinter import (Tk, Text, messagebox, Button, Entry, Label, Scrollbar,
                     Listbox, Toplevel, ttk, StringVar, IntVar, Checkbutton, Frame, Menu)
import random
import socks
import socket

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
        # Set up a Tor SOCKS proxy for requests
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
        socket.socket = socks.socksocket

    def setup_ui(self):
        # URL Entry
        Label(self.root, text="Enter Website URL:").pack(pady=10)
        self.url_entry = Entry(self.root, width=80)
        self.url_entry.pack(pady=10)

        # User Agent Dropdown
        Label(self.root, text="User Agent:").pack(pady=10)
        self.user_agent_var = StringVar(self.root)
        self.user_agent_var.set(self.USER_AGENTS[0])
        self.dropdown = ttk.Combobox(self.root, textvariable=self.user_agent_var, values=self.USER_AGENTS, width=80)
        self.dropdown.pack(pady=10)

        # Load Navigation & Scrape Button
        self.load_nav_button = Button(self.root, text="Load Navigation", command=self.load_navigation)
        self.load_nav_button.pack(pady=10)
        self.scrape_button = Button(self.root, text="Scrape!", command=self.scrape_website)
        self.scrape_button.pack(pady=10)

        # Results Tab
        self.text_w = Text(self.root, wrap="word", cursor="arrow")
        self.text_w.pack(pady=10, padx=10, fill="both", expand=True)
        scrollbar_y = Scrollbar(self.root, orient="vertical", command=self.text_w.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.text_w.config(yscrollcommand=scrollbar_y.set)

    def load_navigation(self):
        base_url = self.url_entry.get()
        headers = {'User-Agent': self.user_agent_var.get()}

        try:
            response = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            # Creating a top level window to display navigation links
            nav_win = Toplevel(self.root)
            nav_win.title("Navigation Links")
            nav_win.geometry("400x600")
            Label(nav_win, text="Select a link to scrape:").pack(pady=10)
            nav_listbox = Listbox(nav_win, width=50, height=30)
            nav_listbox.pack(pady=10, padx=10)

            for link in soup.find_all('a'):
                title = link.text.strip() or link.get('href')
                href = link.get('href')
                if href:
                    nav_listbox.insert('end', href)

            Button(nav_win, text="Scrape Selected", command=lambda: self.scrape_website(nav_listbox.get(nav_listbox.curselection()[0]))).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error!", str(e))

    def scrape_website(self, link=None):
        if link:
            base_url = link
        else:
            base_url = self.url_entry.get()

        headers = {'User-Agent': self.user_agent_var.get()}

        def worker():
            try:
                response = requests.get(base_url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                data = soup.get_text()
                self.text_w.delete(1.0, 'end')
                self.text_w.insert("end", data + "\n")

            except Exception as e:
                messagebox.showerror("Error!", str(e))

        thread = threading.Thread(target=worker)
        thread.start()

if __name__ == "__main__":
    root = Tk()
    scraper = AdvancedWebScraper(root)
    root.mainloop()
