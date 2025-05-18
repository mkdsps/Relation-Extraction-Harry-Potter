import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os
import shutil
from datetime import datetime

class JSONCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Dataset Checker")
        self.root.geometry("800x600")
        
        self.dataset = []
        self.current_index = 0
        self.filename = None
        self.total_checked = 0
        
        # Create UI elements
        self.setup_ui()
        
        # Setup keyboard shortcuts
        self.root.bind("<Control-s>", lambda event: self.save_dataset())
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Dataset", command=self.open_dataset)
        filemenu.add_command(label="Save Dataset (Ctrl+S)", command=self.save_dataset)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        
        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(status_frame, text="Current Item:").pack(side=tk.LEFT)
        self.current_item_label = tk.Label(status_frame, text="0/0")
        self.current_item_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(status_frame, text="Checked:").pack(side=tk.LEFT, padx=(20, 0))
        self.checked_label = tk.Label(status_frame, text="0")
        self.checked_label.pack(side=tk.LEFT, padx=5)
        
        self.id_label = tk.Label(status_frame, text="ID: -")
        self.id_label.pack(side=tk.RIGHT)
        
        # Text editor
        self.text_editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=30)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.next_button = tk.Button(button_frame, text="Mark as Checked & Next", command=self.mark_checked_and_next, state=tk.DISABLED)
        self.next_button.pack(side=tk.RIGHT)
        
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.show_previous, state=tk.DISABLED)
        self.prev_button.pack(side=tk.RIGHT, padx=5)
        
        self.save_button = tk.Button(button_frame, text="Save (Ctrl+S)", command=self.save_dataset)
        self.save_button.pack(side=tk.LEFT)
    
    def open_dataset(self):
        filename = filedialog.askopenfilename(
            title="Open JSON Dataset",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.dataset = json.load(f)
            
            self.filename = filename
            self.current_index = 0
            self.total_checked = sum(1 for item in self.dataset if item.get('checked', 0) == 1)
            self.update_status()
            self.load_current_item()
            
            self.next_button.config(state=tk.NORMAL)
            if len(self.dataset) > 1:
                self.prev_button.config(state=tk.NORMAL)
            
            messagebox.showinfo("Success", f"Loaded dataset with {len(self.dataset)} items")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")
    
    def save_dataset(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(
                title="Save JSON Dataset",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not self.filename:
                return
        
        try:
            # Save the current changes in the text editor
            self.save_current_item()
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.dataset, f, ensure_ascii=False, indent=2)
            
            # Show a small popup message that disappears after 1 second
            save_label = tk.Label(self.root, text="Saved!", bg="green", fg="white", padx=10, pady=5)
            save_label.place(relx=0.5, rely=0.9, anchor="center")
            save_label.after(1000, save_label.destroy)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save dataset: {e}")
    
    def create_backup(self):
        if not self.filename or not os.path.exists(self.filename):
            return
        
        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base, filename_ext = os.path.splitext(self.filename)
            backup_filename = f"{filename_base}_backup_{timestamp}{filename_ext}"
            
            # Save the current changes to the backup file
            self.save_current_item()
            
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.dataset, f, ensure_ascii=False, indent=2)
            
            return backup_filename
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def on_closing(self):
        if self.dataset and self.filename:
            answer = messagebox.askyesnocancel("Exit", "Do you want to save changes before exiting?")
            if answer is None:
                # Cancel pressed
                return
            else:
                try:
                    if not self.save_current_item():
                        return  # If invalid JSON, don't proceed

                    if answer:  # Yes
                        # Save to original file
                        with open(self.filename, 'w', encoding='utf-8') as f:
                            json.dump(self.dataset, f, ensure_ascii=False, indent=2)
                    
                    # Always create a backup, whether Yes or No
                    backup_file = self.create_backup()

                    if backup_file:
                        messagebox.showinfo("Backup Created", f"Backup saved to:\n{backup_file}")
                except Exception as e:
                    print(f"Error during closing: {e}")
        
        self.root.destroy()

    
    def update_status(self):
        if not self.dataset:
            self.current_item_label.config(text="0/0")
            self.checked_label.config(text="0")
            self.id_label.config(text="ID: -")
            return
            
        self.current_item_label.config(text=f"{self.current_index + 1}/{len(self.dataset)}")
        self.checked_label.config(text=str(self.total_checked))
        
        current_id = self.dataset[self.current_index].get('id', '-')
        self.id_label.config(text=f"ID: {current_id}")
    
    def load_current_item(self):
        if not self.dataset:
            return
            
        self.text_editor.delete(1.0, tk.END)
        json_text = json.dumps(self.dataset[self.current_index], ensure_ascii=False, indent=2)
        self.text_editor.insert(tk.END, json_text)
        self.update_status()
    
    def save_current_item(self):
        if not self.dataset:
            return
            
        try:
            text_content = self.text_editor.get(1.0, tk.END).strip()
            updated_item = json.loads(text_content)
            self.dataset[self.current_index] = updated_item
        except json.JSONDecodeError as e:
            messagebox.showerror("Invalid JSON", f"The edited text is not valid JSON: {e}")
            return False
        return True
    
    def find_next_unchecked(self, start_index=None):
        if start_index is None:
            start_index = self.current_index + 1
        
        # First try from current position to end
        for i in range(start_index, len(self.dataset)):
            if self.dataset[i].get('checked', 0) == 0:
                return i
        
        # If not found, try from beginning to current position
        for i in range(0, start_index):
            if self.dataset[i].get('checked', 0) == 0:
                return i
        
        # If all items are checked
        return None
    
    def mark_checked_and_next(self):
        if not self.dataset:
            return
            
        if not self.save_current_item():
            return
            
        # Mark current item as checked if it's not already
        if self.dataset[self.current_index].get('checked', 0) == 0:
            self.dataset[self.current_index]['checked'] = 1
            self.total_checked += 1
        
        # Find next unchecked item
        next_index = self.find_next_unchecked()
        
        if next_index is not None:
            self.current_index = next_index
            self.load_current_item()
        else:
            messagebox.showinfo("All Done", "All items have been checked!")
            # Stay on the current item after marking it as checked
            self.load_current_item()
    
    def show_previous(self):
        if not self.dataset or self.current_index <= 0:
            return
            
        if self.save_current_item():
            self.current_index -= 1
            self.load_current_item()

def main():
    root = tk.Tk()
    app = JSONCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()