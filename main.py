import tkinter as tk
from tkinter import ttk
import pyshorteners

# Defining available URL shortening services with descriptions
SERVICE_OPTIONS = [
    {"name": "TinyURL", "description": "Shorten URLs using TinyURL service."},
    {"name": "Is.gd", "description": "Shorten URLs using Is.gd service."},
    {"name": "Bit.ly", "description": "Shorten URLs using Bit.ly service (API key required)."},
    # Add more services with descriptions here
]

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Shortener")
        self.root.geometry("500x300")
        self.s = pyshorteners.Shortener()

        self.create_gui()

    def create_gui(self):
        # Create the GUI elements
        
        # Title Label
        title_label = tk.Label(self.root, text="URL Shortener", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Long URL Entry
        long_url_label = tk.Label(self.root, text="Enter Long URL:", font=("Arial", 12))
        long_url_label.pack()
        self.long_url_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.long_url_entry.pack(pady=5)

        # Service ComboBox
        service_label = tk.Label(self.root, text="Select a Service:", font=("Arial", 12))
        service_label.pack()
        self.service_combobox = ttk.Combobox(self.root, values=[s["name"] for s in SERVICE_OPTIONS], font=("Arial", 12))
        self.service_combobox.set(SERVICE_OPTIONS[0]["name"])
        self.service_combobox.pack()
        self.service_combobox.bind("<<ComboboxSelected>>", self.on_service_selected)

        # Service Description Label
        self.service_description_label = tk.Label(self.root, text=SERVICE_OPTIONS[0]["description"], font=("Arial", 10))
        self.service_description_label.pack()

        # Shorten Button
        self.shorten_button = tk.Button(self.root, text="Shorten URL", command=self.shorten_url, font=("Arial", 12))
        self.shorten_button.pack(pady=10)

        # Shortened URL Entry
        short_url_label = tk.Label(self.root, text="Shortened URL:", font=("Arial", 12))
        short_url_label.pack()
        self.short_url_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.short_url_entry.pack(pady=5)

        # Error Label
        self.error_label = tk.Label(self.root, text="", fg="red", font=("Arial", 12))
        self.error_label.pack()

    def on_service_selected(self, event):
        # Update the description label based on the selected service
        
        selected_service_name = self.service_combobox.get()
        selected_service = next((s for s in SERVICE_OPTIONS if s["name"] == selected_service_name), None)
        if selected_service:
            self.service_description_label.config(text=selected_service["description"])
        else:
            self.service_description_label.config(text="")

    def shorten_url(self):
        # Shorten the URL when the button is clicked
        
        long_url = self.long_url_entry.get()
        selected_service_name = self.service_combobox.get()

        try:
            short_url = self.shorten_url_with_service(long_url, selected_service_name)
            self.short_url_entry.delete(0, tk.END)
            self.short_url_entry.insert(0, short_url)
            self.error_label.config(text="")
        except Exception as e:
            self.error_label.config(text=f"Error: {str(e)}")

    def shorten_url_with_service(self, url, service_name):
        # Shorten the URL using the selected service
        
        if service_name == "TinyURL":
            return self.s.tinyurl.short(url)
        elif service_name == "Is.gd":
            return self.s.isgd.short(url)
        elif service_name == "Bit.ly":
            api_key = self.get_bitly_api_key()
            if not api_key:
                raise Exception("Bit.ly API key is missing.")
            self.s.bitly.api_key = api_key
            return self.s.bitly.short(url)
        else:
            raise Exception("Invalid service name.")

    def get_bitly_api_key(self):
        # Replace this with your Bit.ly API key retrieval logic
        return "01012c7446823c9d3be920d44948ea3f3917aa13"

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()