import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import os
import threading
import queue


def process_html_file(file_path, q):
    """
    Process a single HTML/HTM file to extract its text content.
    :param file_path: Path to the HTML/HTM file.
    :param q: Queue to store the extracted text for thread-safe retrieval.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = extract_text_from_soup(soup)
        q.put(text)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        q.put("")


def extract_text_from_soup(soup):
    """
    Extracts text content from a BeautifulSoup object, preserving some structure (headings, paragraphs).
    :param soup: BeautifulSoup object representing the HTML document.
    :return: Extracted and structured text.
    """
    text = ""

    # Add title if present
    if soup.title:
        text += soup.title.string + "\n\n"

    # Extract headings and paragraphs, preserving some structure
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']):
        if tag.name.startswith('h'):
            text += "\n" + tag.get_text(separator=" ", strip=True).upper() + "\n"
        else:
            text += tag.get_text(separator=" ", strip=True) + "\n"

    return text


def select_folder_and_process_html():
    """
    Allows the user to select a folder containing HTML/HTM files and processes them to extract text.
    The extracted text is combined and saved to a text file.
    """
    folder_path = filedialog.askdirectory(title="Select Folder Containing HTML/HTM Files")
    if not folder_path:
        return

    html_files = [f for f in os.listdir(folder_path) if f.endswith(('.html', '.htm'))]
    if not html_files:
        messagebox.showwarning("No HTML Files", "No HTML or HTM files found in the selected folder.")
        return

    q = queue.Queue()
    threads = []

    # Process each HTML file in a separate thread
    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        thread = threading.Thread(target=process_html_file, args=(file_path, q))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine the extracted text content
    combined_text_content = '\n\n'.join(q.get() for _ in range(len(html_files)))

    # Save the combined text to a file
    save_combined_file(combined_text_content)


def select_html_file_and_process():
    """
    Allows the user to select a single HTML file, processes it to extract the text, and saves the extracted text.
    """
    file_path = filedialog.askopenfilename(title="Select HTML file", filetypes=[("HTML files", "*.html;*.htm")])
    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = extract_text_from_soup(soup)

        # Save the extracted text to a file
        save_combined_file(text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the file: {e}")


def save_combined_file(content):
    """
    Allows the user to specify a file path and saves the provided content to a text file.
    :param content: The text content to save.
    """
    file_path = filedialog.asksaveasfilename(title="Save Text File", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("Success", f"File saved successfully at {file_path}")
    else:
        messagebox.showwarning("No File Saved", "File save operation was canceled.")


def main():
    """
    Main function that sets up the Tkinter GUI and provides options to extract text from HTML files.
    """
    root = tk.Tk()
    root.title("HTML Text Extractor")

    # Button for selecting a folder of HTML/HTM files to combine text
    combine_button = tk.Button(root, text="Select Folder and Extract Text from HTML/HTM Files", command=select_folder_and_process_html)
    combine_button.pack(pady=10)

    # Button for selecting a single HTML file to extract and save its text
    single_file_button = tk.Button(root, text="Select Single HTML File and Extract Text", command=select_html_file_and_process)
    single_file_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
