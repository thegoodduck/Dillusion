import requests
import hashlib
import tkinter as tk
from tkinter import scrolledtext

# Function to fetch web page content with Tor
def fetch_with_tor(url):
    proxies = {
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050',
    }
    response = requests.get(url, proxies=proxies)
    return response.text

# Function to fetch web page content without Tor
def fetch_without_tor(url):
    response = requests.get(url)
    return response.text

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    hash1 = hashlib.sha256(text1.encode()).hexdigest()
    hash2 = hashlib.sha256(text2.encode()).hexdigest()
    similarity_percentage = len(set(hash1) & set(hash2)) / float(len(set(hash1) | set(hash2))) * 100
    return similarity_percentage

# Function to compare content fetched with and without Tor
def compare_content(url):
    content_with_tor = fetch_with_tor(url)
    content_without_tor = fetch_without_tor(url)
    
    similarity_percentage = calculate_similarity(content_with_tor, content_without_tor)
    
    return similarity_percentage, content_with_tor, content_without_tor

# Function to update the GUI with comparison results
def update_gui(similarity_percentage, content_with_tor, content_without_tor):
    lbl_similarity.config(text=f"Similarity Percentage: {similarity_percentage:.2f}%")
    txt_with_tor.delete(1.0, tk.END)
    txt_with_tor.insert(tk.END, content_with_tor)
    txt_without_tor.delete(1.0, tk.END)
    txt_without_tor.insert(tk.END, content_without_tor)

# Function to handle the comparison button click event
def compare_button_click():
    url = entry_url.get()
    if url:
        similarity_percentage, content_with_tor, content_without_tor = compare_content(url)
        update_gui(similarity_percentage, content_with_tor, content_without_tor)

# Create main application window
root = tk.Tk()
root.title("Tor Content Comparison")

# Create URL entry widget
lbl_url = tk.Label(root, text="Enter URL:")
lbl_url.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=5, pady=5)

# Create comparison button
btn_compare = tk.Button(root, text="Compare", command=compare_button_click)
btn_compare.grid(row=0, column=2, padx=5, pady=5)

# Create similarity percentage label
lbl_similarity = tk.Label(root, text="")
lbl_similarity.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Create scrolled text widget for content fetched with Tor
txt_with_tor = scrolledtext.ScrolledText(root, width=50, height=20)
txt_with_tor.grid(row=2, column=0, padx=5, pady=5, columnspan=3)

# Create scrolled text widget for content fetched without Tor
txt_without_tor = scrolledtext.ScrolledText(root, width=50, height=20)
txt_without_tor.grid(row=3, column=0, padx=5, pady=5, columnspan=3)

# Run the application
root.mainloop()
