import tkinter as tk
from tkinter import ttk, messagebox
import time
import json

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Application")

        self.name_var = tk.StringVar()
        self.accuracy_score = 0
        self.speed_score = 0
        self.interoperability_score = 0
        # Initialize a variable for storing the CAPP system name
        self.capp_name_var = tk.StringVar()
        # Load the leaderboard data from a file
        self.load_leaderboard_data()
        self.answer_vars = []

        # CAPP System Name Entry
        tk.Label(self.root, text="Enter CAPP System Name:").pack(pady=(10, 5))
        capp_name_entry = tk.Entry(self.root, textvariable=self.capp_name_var)
        capp_name_entry.pack(pady=(0, 20))
        capp_name_entry.focus_set()  # Set focus to the entry widget




        self.tabControl = ttk.Notebook(root)
        self.tab_accuracy = ttk.Frame(self.tabControl)
        self.tab_speed = ttk.Frame(self.tabControl)
        self.tab_interoperability = ttk.Frame(self.tabControl)
        self.tab_leaderboard = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_accuracy, text='Accuracy')
        self.tabControl.add(self.tab_speed, text='Speed')
        self.tabControl.add(self.tab_interoperability, text='Interoperability')
        self.tabControl.add(self.tab_leaderboard, text='Leaderboard')

        self.initialize_accuracy_tab()
        self.initialize_speed_tab()
        self.initialize_interoperability_tab()
        self.initialize_leaderboard_tab()

        self.tabControl.pack(expand=1, fill="both")

    def load_leaderboard_data(self):
        try:
            with open('leaderboard_data.json', 'r') as file:
                self.leaderboard_data = json.load(file)
        except FileNotFoundError:
            self.leaderboard_data = []

    def save_leaderboard_data(self):
        with open('leaderboard_data.json', 'w') as file:
            json.dump(self.leaderboard_data, file)

    def update_leaderboard(self, accuracy_score, speed_score, interoperability_score):
        capp_name = self.capp_name_var.get()
        overall_benchmark_score = (0.6 * accuracy_score) + (0.05 * speed_score) + (0.35 * interoperability_score)
        new_entry = [capp_name, accuracy_score, speed_score, interoperability_score, overall_benchmark_score]
        
        for i, entry in enumerate(self.leaderboard_data):
            if entry[0] == capp_name:
                self.leaderboard_data[i] = new_entry
                break
        else:
            self.leaderboard_data.append(new_entry)
        
        self.refresh_leaderboard()
        self.save_leaderboard_data()

    def initialize_accuracy_tab(self):
        tk.Label(self.tab_accuracy, text="Accuracy Test").pack(pady=10)
        # Initialization of questions and options
        for i in range(20):  # Assuming 20 questions
            frame = ttk.Frame(self.tab_accuracy)
            frame.pack(pady=5)
            ttk.Label(frame, text=f"Question {i+1}: What process is needed?").pack(side="left")
            
            question_vars = []
            for option in ["Milling", "Drilling", "Turning", "Hobbing"]:
                var = tk.BooleanVar()
                ttk.Checkbutton(frame, text=option, variable=var).pack(side="left")
                question_vars.append(var)  # Store the BooleanVar directly

            self.answer_vars.append(question_vars)  # Store the vars for each question

        ttk.Button(self.tab_accuracy, text="Submit", command=self.calculate_accuracy_score).pack(pady=20)

    def calculate_accuracy_score(self):
        self.accuracy_score = 0
    # Assuming correct_answers is a list of sets, each set containing the correct options for a question
        correct_answers = [
            {"Milling"},
            {"Turning", "Milling"},
            {"Turning", "Milling"},
            {"Turning", "Milling"},
            {"Turning"},
            {"Milling", "Drilling"},
            {"Milling", "Drilling"},
            {"Milling"},
            {"Milling"},
            {"Milling"},
            {"Milling", "Turning"},
            {"Milling"},
            {"Milling", "Drilling"},
            {"Turning"},
            {"Milling", "Turning", "Hobbing"},
            {"Milling", "Turning"},
            {"Milling"},
            {"Turnig"},
            {"Turning"},
            {"Milling", "Hobbing"} # Example correct answers for 5 questions
        ]
        options = ["Milling", "Drilling", "Turning", "Hobbing"]

        question_points = [2] * 5 + [3] * 5 + [5] * 5 + [10] * 5

        for i, question_vars in enumerate(self.answer_vars):
        # Collect the options selected by the user for this question
            selected = {options[j] for j, var in enumerate(question_vars) if var.get()}

        # Check if the selected options match the correct answers for this question
            if selected == correct_answers[i]:
            # Increment the score by the points for the current question
               self.accuracy_score += question_points[i]

        self.update_leaderboard(self.accuracy_score, self.speed_score, self.interoperability_score)
        messagebox.showinfo("Accuracy Score", f"Your accuracy score is: {self.accuracy_score}")



    def initialize_speed_tab(self):
        self.speed_timer_label = tk.Label(self.tab_speed, text="00:00:00", font=('Helvetica', 48))
        self.speed_timer_label.pack(pady=10, padx=10)  # You can adjust padding here

        ttk.Button(self.tab_speed, text="Start", command=self.start_speed_test).pack(side=tk.LEFT, padx=(20, 10), pady=20)
        ttk.Button(self.tab_speed, text="Stop", command=self.stop_speed_test).pack(side=tk.LEFT, padx=(10, 20), pady=20)

    def start_speed_test(self):
        self.speed_start_time = time.time()
        self.update_speed_timer()

    def stop_speed_test(self):
        if self.speed_start_time:
           elapsed_time = time.time() - self.speed_start_time
        # Calculate the speed score as specified
           self.speed_score = round(1 / elapsed_time * 100)
        # Corrected: Removed self.name_var.get() from the arguments
           self.update_leaderboard(self.accuracy_score, self.speed_score, self.interoperability_score)
           messagebox.showinfo("Speed Score", f"Your speed score is: {self.speed_score}")
           self.speed_start_time = None

    def update_speed_timer(self):
        if self.speed_start_time:
            elapsed_time = time.time() - self.speed_start_time
            self.speed_timer_label.config(text=time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
            self.root.after(1000, self.update_speed_timer)

    def initialize_interoperability_tab(self):
        label_interoperability = tk.Label(self.tab_interoperability, text="Interoperability Test")
        label_interoperability.pack(pady=10)

        self.interop_options = ["STEP", "IGES", "DWG", "STL", "SLDPRT"]
        self.interop_vars = {fmt: tk.BooleanVar(value=False) for fmt in self.interop_options}

        for fmt in self.interop_options:
            tk.Checkbutton(self.tab_interoperability, text=fmt, variable=self.interop_vars[fmt]).pack(anchor="w")

        tk.Button(self.tab_interoperability, text="Submit", command=self.record_interoperability_score).pack(pady=20)




    def record_interoperability_score(self):
       score_per_option = 20  # Each selected option adds 10 points
       self.interoperability_score = sum(var.get() for var in self.interop_vars.values()) * score_per_option
    # Corrected: Removed self.capp_name from the arguments
       self.update_leaderboard(self.accuracy_score, self.speed_score, self.interoperability_score)
       messagebox.showinfo("Interoperability Score", f"Interoperability Score: {self.interoperability_score}")


    def reset_leaderboard(self):
        self.leaderboard_data = []
        self.refresh_leaderboard()
        messagebox.showinfo("Reset Leaderboard", "Leaderboard has been reset.")
        self.save_leaderboard_data()  # Save the cleared leaderboard data to the file

    def initialize_leaderboard_tab(self):
    # Add some styling
        style = ttk.Style(self.root)
        style.theme_use("clam")  # Using a theme that allows for customization
        style.configure("Treeview", background="#E8E8E8", foreground="black",
                        rowheight=25, fieldbackground="#E8E8E8")
        style.map('Treeview', background=[('selected', '#347083')])  # Change highlight color

    # Create Treeview with specified column headings
        self.leaderboard_tree = ttk.Treeview(self.tab_leaderboard, columns=("Name", "Accuracy", "Speed", "Interoperability", "Overall Score"), show="headings")
    
    # Define column headings and widths
        col_width = 120  # You can adjust widths as needed
        self.leaderboard_tree.heading("Name", text="CAPP System Name")
        self.leaderboard_tree.column("Name", width=col_width)
        self.leaderboard_tree.heading("Accuracy", text="Accuracy Score")
        self.leaderboard_tree.column("Accuracy", width=col_width)
        self.leaderboard_tree.heading("Speed", text="Speed Score")
        self.leaderboard_tree.column("Speed", width=col_width)
        self.leaderboard_tree.heading("Interoperability", text="Interoperability Score")
        self.leaderboard_tree.column("Interoperability", width=col_width)
        self.leaderboard_tree.heading("Overall Score", text="Overall Benchmark Score")
        self.leaderboard_tree.column("Overall Score", width=col_width)
    
    # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.tab_leaderboard, orient="vertical", command=self.leaderboard_tree.yview)
        self.leaderboard_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    # Pack the Treeview
        self.leaderboard_tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Refresh the leaderboard to display any data
        self.refresh_leaderboard()

    # Add Reset Button
        reset_button = ttk.Button(self.tab_leaderboard, text="Reset Leaderboard", command=self.reset_leaderboard)
        reset_button.pack(pady=10)

    def refresh_leaderboard(self):
        for item in self.leaderboard_tree.get_children():
            self.leaderboard_tree.delete(item)
        sorted_leaderboard = sorted(self.leaderboard_data, key=lambda x: x[4], reverse=True)
        for data in sorted_leaderboard:
            self.leaderboard_tree.insert('', 'end', values=data)  # 'data' includes the Overall Benchmark Score


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
