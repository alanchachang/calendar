import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import os

class CalendarFolderOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Folder Organizer")
        self.root.geometry("800x700")  # Increased height for new controls
        
        self.excluded_dates = set()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left side - Calendar and controls
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx=10, sticky=(tk.N, tk.S))
        
        # Calendar
        self.calendar = Calendar(self.left_frame, selectmode='day', 
                               date_pattern='y-mm-dd',
                               showweeknumbers=False)
        self.calendar.grid(row=0, column=0, pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)
        
        # Buttons for date management
        ttk.Button(self.left_frame, text="Exclude Selected Date", 
                  command=self.exclude_date).grid(row=1, column=0, pady=5)
        ttk.Button(self.left_frame, text="Clear Excluded Dates", 
                  command=self.clear_excluded).grid(row=2, column=0, pady=5)
        
        # Right side - Settings and excluded dates list
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=10, sticky=(tk.N, tk.S))
        
        # Base Directory Section
        ttk.Label(self.right_frame, text="Base Directory:").grid(row=0, column=0, sticky=tk.W)
        self.base_dir = tk.StringVar(value=os.path.expanduser("~/Documents"))
        ttk.Entry(self.right_frame, textvariable=self.base_dir, width=40).grid(row=1, column=0, pady=5)
        
        # Folder Name Section
        ttk.Label(self.right_frame, text="Folder Name:").grid(row=2, column=0, sticky=tk.W)
        self.folder_name = tk.StringVar(value="Project")
        ttk.Entry(self.right_frame, textvariable=self.folder_name, width=40).grid(row=3, column=0, pady=5)
        
        # Date Position
        ttk.Label(self.right_frame, text="Date Position:").grid(row=4, column=0, sticky=tk.W)
        self.date_position = tk.StringVar(value="before")
        date_positions = ttk.Frame(self.right_frame)
        date_positions.grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(date_positions, text="Before name (2024-12-30_ProjectName)", 
                       variable=self.date_position, value="before").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(date_positions, text="After name (ProjectName_2024-12-30)", 
                       variable=self.date_position, value="after").grid(row=1, column=0, sticky=tk.W)
        
        # Date Format
        ttk.Label(self.right_frame, text="Date Format:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.date_format = tk.StringVar(value="YYYY-MM-DD")
        format_options = ["YYYY-MM-DD", "MM-DD-YYYY", "DD-MM-YYYY"]
        ttk.Combobox(self.right_frame, textvariable=self.date_format, 
                    values=format_options, state="readonly").grid(row=7, column=0, sticky=tk.W)
        
        # Date Range Section
        ttk.Label(self.right_frame, text="Date Range:").grid(row=8, column=0, sticky=tk.W, pady=5)
        
        # Start Date
        self.start_frame = ttk.Frame(self.right_frame)
        self.start_frame.grid(row=9, column=0, sticky=(tk.W, tk.E))
        ttk.Label(self.start_frame, text="Start Date:").grid(row=0, column=0)
        self.start_date = tk.StringVar()
        ttk.Entry(self.start_frame, textvariable=self.start_date, width=20).grid(row=0, column=1)
        
        # End Date
        self.end_frame = ttk.Frame(self.right_frame)
        self.end_frame.grid(row=10, column=0, sticky=(tk.W, tk.E))
        ttk.Label(self.end_frame, text="End Date:").grid(row=0, column=0)
        self.end_date = tk.StringVar()
        ttk.Entry(self.end_frame, textvariable=self.end_date, width=20).grid(row=0, column=1)
        
        # Excluded Dates List
        ttk.Label(self.right_frame, text="Excluded Dates:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.excluded_listbox = tk.Listbox(self.right_frame, height=6, width=40)
        self.excluded_listbox.grid(row=12, column=0, pady=5)
        
        # Preview Button
        ttk.Button(self.right_frame, text="Preview Folder Names", 
                  command=self.preview_folders).grid(row=13, column=0, pady=5)
        
        # Create Folders Button
        ttk.Button(self.right_frame, text="Create Folders", 
                  command=self.create_folders).grid(row=14, column=0, pady=5)
        
        # Status Label
        self.status_var = tk.StringVar()
        ttk.Label(self.right_frame, textvariable=self.status_var).grid(row=15, column=0, pady=5)

    def on_date_select(self, event=None):
        selected_date = self.calendar.get_date()
        if not self.start_date.get() or (self.start_date.get() and self.end_date.get()):
            self.start_date.set(selected_date)
            self.end_date.set("")
        else:
            self.end_date.set(selected_date)

    def exclude_date(self):
        selected_date = self.calendar.get_date()
        if selected_date not in self.excluded_dates:
            self.excluded_dates.add(selected_date)
            self.update_excluded_listbox()

    def clear_excluded(self):
        self.excluded_dates.clear()
        self.update_excluded_listbox()

    def update_excluded_listbox(self):
        self.excluded_listbox.delete(0, tk.END)
        for date in sorted(self.excluded_dates):
            self.excluded_listbox.insert(tk.END, date)

    def _format_date(self, date_str):
        year, month, day = map(int, date_str.split('-'))
        date_format = self.date_format.get()
        month_str = str(month).zfill(2)
        day_str = str(day).zfill(2)
        
        if date_format == "YYYY-MM-DD":
            return f"{year}-{month_str}-{day_str}"
        elif date_format == "MM-DD-YYYY":
            return f"{month_str}-{day_str}-{year}"
        else:  # DD-MM-YYYY
            return f"{day_str}-{month_str}-{year}"

    def _generate_folder_name(self, date_str):
        formatted_date = self._format_date(date_str)
        folder_name = self.folder_name.get().strip()
        
        if not folder_name:
            return formatted_date
        
        if self.date_position.get() == "before":
            return f"{formatted_date}_{folder_name}"
        else:
            return f"{folder_name}_{formatted_date}"

    def preview_folders(self):
        try:
            if not self.start_date.get() or not self.end_date.get():
                messagebox.showerror("Error", "Please select both start and end dates")
                return
                
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d')
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d')
            
            if start > end:
                messagebox.showerror("Error", "Start date must be before end date")
                return
            
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Folder Name Preview")
            preview_window.geometry("400x300")
            
            preview_text = tk.Text(preview_window, wrap=tk.WORD, width=40, height=15)
            preview_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            current_date = start
            while current_date <= end:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str not in self.excluded_dates:
                    folder_name = self._generate_folder_name(date_str)
                    preview_text.insert(tk.END, folder_name + '\n')
                current_date += timedelta(days=1)
            
            preview_text.config(state=tk.DISABLED)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid dates")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_folders(self):
        try:
            if not self.start_date.get() or not self.end_date.get():
                messagebox.showerror("Error", "Please select both start and end dates")
                return
                
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d')
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d')
            
            if start > end:
                messagebox.showerror("Error", "Start date must be before end date")
                return
            
            current_date = start
            created_count = 0
            
            while current_date <= end:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str not in self.excluded_dates:
                    folder_name = self._generate_folder_name(date_str)
                    folder_path = os.path.join(self.base_dir.get(), folder_name)
                    
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        created_count += 1
                
                current_date += timedelta(days=1)
            
            self.status_var.set(f"Successfully created {created_count} folders")
            messagebox.showinfo("Success", f"Created {created_count} folders")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid dates")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarFolderOrganizerApp(root)
    root.mainloop()
