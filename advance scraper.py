import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Text, messagebox, Button, Entry, Label, Scrollbar
import threading

def scrape_website():
    def worker():
        base_url = url_entry.get().rstrip('/')

        # Empty the text widget
        text_w.delete(1.0, "end")

        try:
            response = requests.get(base_url)
            if response.status_code != 200:
                messagebox.showerror("Error!", f"Failed to fetch data from {base_url}. Status code: {response.status_code}")
                return

            soup = BeautifulSoup(response.content, "html.parser")

            # Assuming the navigation links are within <nav> or have class 'navbar'
            nav = soup.find('nav') or soup.find(class_='navbar')

            if not nav:
                messagebox.showerror("Error!", "Navigation bar not found!")
                return

            # Extracting links from the navigation bar
            nav_links = [a['href'] for a in nav.find_all('a', href=True) if a['href']]

            for link in nav_links:
                # Making sure it's a relative link and not an external link
                if not link.startswith('http'):
                    current_url = base_url + link
                else:
                    current_url = link

                try:
                    sub_response = requests.get(current_url)
                    if sub_response.status_code != 200:
                        continue

                    sub_soup = BeautifulSoup(sub_response.content, "html.parser")

                    # Insert the link as a heading
                    text_w.insert("end", f"\nPAGE: {current_url.upper()}:\n")
                    text_w.insert("end", "=" * len(current_url) * 2 + "\n")

                    # Extract headings and subsequent content
                    for heading in sub_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                        text_w.insert("end", heading.text + "\n")
                        for sibling in heading.find_next_siblings():
                            if sibling.name and sibling.name.startswith('h'):
                                break
                            text_w.insert("end", sibling.text.strip() + "\n")

                    # Display image URLs
                    for img_tag in sub_soup.find_all('img'):
                        img_url = img_tag.get('src')
                        if not img_url.startswith("http"):
                            img_url = base_url + img_url
                        text_w.insert("end", f"Image URL: {img_url}\n")

                except Exception as e:
                    messagebox.showerror("Error!", str(e))

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

scroll_y = Scrollbar(root, orient="vertical")
text_w = Text(root, wrap="word", cursor="arrow", yscrollcommand=scroll_y.set)
text_w.pack(pady=10, padx=10, fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
scroll_y.config(command=text_w.yview)

root.mainloop()
