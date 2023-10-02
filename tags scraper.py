import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, StringVar, messagebox

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) ...',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; ...) ...'
]

class AdvancedScraper(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Advanced Web Scraper")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.url_frame = ttk.LabelFrame(self, text="URL & User-Agent", padding=(10, 5))
        self.url_frame.pack(pady=20, fill="x", padx=10)

        self.label_url = ttk.Label(self.url_frame, text="Website URL:")
        self.label_url.grid(row=0, column=0, padx=(0, 10), pady=(10, 0))

        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.grid(row=0, column=1, pady=(10, 0))

        self.label_agent = ttk.Label(self.url_frame, text="User-Agent:")
        self.label_agent.grid(row=1, column=0, pady=10, padx=(0, 10))

        self.user_agent_var = StringVar()
        self.user_agent_dropdown = ttk.Combobox(self.url_frame, textvariable=self.user_agent_var, values=USER_AGENTS, width=47)
        self.user_agent_dropdown.current(0)
        self.user_agent_dropdown.grid(row=1, column=1, pady=10)

        self.scrape_btn = ttk.Button(self.url_frame, text="Scrape!", command=self.scrape_website)
        self.scrape_btn.grid(row=0, column=2, padx=20)

        self.tags_frame = ttk.LabelFrame(self, text="Filter Tags (comma separated, optional)", padding=(10, 5))
        self.tags_frame.pack(pady=20, fill="x", padx=10)

        self.tags_entry = ttk.Entry(self.tags_frame, width=80)
        self.tags_entry.pack(pady=10)

        self.result_text = tk.Text(self, wrap="word")
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

    def scrape_website(self):
        url = self.url_entry.get()
        tags = self.tags_entry.get().split(",") if self.tags_entry.get() else ["p", "h1", "h2", "img"]
        user_agent = self.user_agent_var.get()

        headers = {"User-Agent": user_agent}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                messagebox.showerror("Error", f"Failed to fetch data. Status code: {response.status_code}")
                return

            soup = BeautifulSoup(response.content, "html.parser")
            self.result_text.delete(1.0, tk.END)

            for tag in tags:
                elements = soup.find_all(tag.strip())
                self.result_text.insert(tk.END, f"--- {tag.strip().upper()} ---\n")
                for element in elements:
                    if tag.strip() == "img":
                        self.result_text.insert(tk.END, element.get("src") + "\n")
                    else:
                        self.result_text.insert(tk.END, element.text + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = AdvancedScraper()
    app.mainloop()
