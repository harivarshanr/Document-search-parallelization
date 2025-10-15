# import tkinter as tk
# from tkinter import ttk, scrolledtext, messagebox
# import multiprocessing as mp
# from multiprocessing import Pool
# import time
# import random

# class ParallelDocumentSearchGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Parallel Document Search System")
#         self.root.geometry("1200x800")
#         self.root.configure(bg='#f0f4f8')
        
#         # Default data
#         self.documents = [
#             {'id': 0, 'values': [5, 7, 6]},
#             {'id': 1, 'values': [2, 6, 5]},
#             {'id': 2, 'values': [7, 2, 1]},
#             {'id': 3, 'values': [6, 3, 9]},
#             {'id': 4, 'values': [6, 2, 6]},
#             {'id': 5, 'values': [9, 7, 8]},
#             {'id': 6, 'values': [3, 2, 0]},
#             {'id': 7, 'values': [2, 9, 5]},
#             {'id': 8, 'values': [7, 9, 8]},
#             {'id': 9, 'values': [2, 1, 6]}
#         ]
#         self.query = [3, 2, 1]
        
#         self.setup_ui()
        
#     def setup_ui(self):
#         # Main container
#         main_frame = tk.Frame(self.root, bg='#f0f4f8')
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
#         # Title
#         title_frame = tk.Frame(main_frame, bg='#2c3e50', relief=tk.RAISED, bd=3)
#         title_frame.pack(fill=tk.X, pady=(0, 20))
        
#         title_label = tk.Label(title_frame, text="🔍 Parallel Document Search System", 
#                               font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white', pady=15)
#         title_label.pack()
        
#         # Content frame (left and right panels)
#         content_frame = tk.Frame(main_frame, bg='#f0f4f8')
#         content_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Left Panel
#         left_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
#         left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
#         # Right Panel
#         right_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
#         right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
#         self.setup_left_panel(left_panel)
#         self.setup_right_panel(right_panel)
        
#     def setup_left_panel(self, parent):
#         # Query Vector Section
#         query_frame = tk.LabelFrame(parent, text="Query Vector", font=('Arial', 12, 'bold'),
#                                    bg='#e8f4f8', fg='#2c3e50', padx=10, pady=10)
#         query_frame.pack(fill=tk.X, padx=15, pady=10)
        
#         self.query_entries = []
#         query_input_frame = tk.Frame(query_frame, bg='#e8f4f8')
#         query_input_frame.pack()
        
#         for i, val in enumerate(self.query):
#             entry = tk.Entry(query_input_frame, width=8, font=('Arial', 11), justify='center')
#             entry.insert(0, str(val))
#             entry.pack(side=tk.LEFT, padx=5)
#             self.query_entries.append(entry)
        
#         tk.Button(query_input_frame, text="+ Dimension", command=self.add_dimension,
#                  bg='#3498db', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
#         # Parameters Section
#         params_frame = tk.LabelFrame(parent, text="Parameters", font=('Arial', 12, 'bold'),
#                                     bg='#f8e8f8', fg='#2c3e50', padx=10, pady=10)
#         params_frame.pack(fill=tk.X, padx=15, pady=10)
        
#         tk.Label(params_frame, text="Top K Documents:", bg='#f8e8f8', 
#                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
#         self.k_var = tk.StringVar(value='5')
#         tk.Entry(params_frame, textvariable=self.k_var, width=10, 
#                 font=('Arial', 10)).grid(row=0, column=1, pady=5, padx=10)
        
#         tk.Label(params_frame, text="Number of Processors:", bg='#f8e8f8',
#                 font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
#         self.proc_var = tk.StringVar(value='4')
#         tk.Entry(params_frame, textvariable=self.proc_var, width=10,
#                 font=('Arial', 10)).grid(row=1, column=1, pady=5, padx=10)
        
#         # Action Buttons
#         button_frame = tk.Frame(parent, bg='#ffffff')
#         button_frame.pack(fill=tk.X, padx=15, pady=10)
        
#         tk.Button(button_frame, text="▶ Run Search", command=self.run_search,
#                  bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
#                  padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
#         tk.Button(button_frame, text="+ Add Document", command=self.add_document,
#                  bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
#                  padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
#         # Documents List
#         docs_frame = tk.LabelFrame(parent, text=f"Documents ({len(self.documents)})",
#                                   font=('Arial', 12, 'bold'), bg='#f0f0f0',
#                                   fg='#2c3e50', padx=10, pady=10)
#         docs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
#         self.docs_text = scrolledtext.ScrolledText(docs_frame, height=15, width=40,
#                                                    font=('Courier', 10), bg='#ffffff')
#         self.docs_text.pack(fill=tk.BOTH, expand=True)
#         self.update_docs_display()
        
#     def setup_right_panel(self, parent):
#         # Results Section
#         results_frame = tk.LabelFrame(parent, text="Search Results", 
#                                      font=('Arial', 12, 'bold'), bg='#e8f8e8',
#                                      fg='#2c3e50', padx=10, pady=10)
#         results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
#         self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=50,
#                                                      font=('Courier', 10), bg='#ffffff')
#         self.results_text.pack(fill=tk.BOTH, expand=True)
        
#         # Stats Section
#         stats_frame = tk.LabelFrame(parent, text="Performance Statistics",
#                                    font=('Arial', 12, 'bold'), bg='#fff8e8',
#                                    fg='#2c3e50', padx=10, pady=10)
#         stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
#         self.stats_text = tk.Text(stats_frame, height=8, width=50,
#                                  font=('Courier', 10), bg='#fffef0')
#         self.stats_text.pack(fill=tk.X)
        
#     def update_docs_display(self):
#         self.docs_text.delete('1.0', tk.END)
#         for doc in self.documents:
#             self.docs_text.insert(tk.END, f"Doc {doc['id']:2d}: {doc['values']}\n")
    
#     def add_dimension(self):
#         self.query.append(0)
#         entry = tk.Entry(self.query_entries[0].master, width=8, 
#                         font=('Arial', 11), justify='center')
#         entry.insert(0, '0')
#         entry.pack(side=tk.LEFT, padx=5, before=self.query_entries[0].master.winfo_children()[-1])
#         self.query_entries.append(entry)
        
#         # Add random value to all documents
#         for doc in self.documents:
#             doc['values'].append(random.randint(0, 9))
#         self.update_docs_display()
        
#     def add_document(self):
#         new_id = len(self.documents)
#         query_len = len(self.query)
#         new_doc = {
#             'id': new_id,
#             'values': [random.randint(0, 9) for _ in range(query_len)]
#         }
#         self.documents.append(new_doc)
#         self.update_docs_display()
#         messagebox.showinfo("Success", f"Document {new_id} added!")
    
#     def get_query(self):
#         return [int(entry.get()) for entry in self.query_entries]
    
#     def run_search(self):
#         try:
#             query = self.get_query()
#             k = int(self.k_var.get())
#             num_processors = int(self.proc_var.get())
            
#             if k > len(self.documents):
#                 k = len(self.documents)
            
#             self.results_text.delete('1.0', tk.END)
#             self.stats_text.delete('1.0', tk.END)
            
#             self.results_text.insert(tk.END, "Processing with TRUE PARALLELIZATION...\n")
#             self.results_text.insert(tk.END, "=" * 50 + "\n\n")
#             self.root.update()
            
#             # Run parallel search
#             start_time = time.time()
#             results = parallel_document_search(self.documents, query, k, num_processors)
#             end_time = time.time()
            
#             execution_time = (end_time - start_time) * 1000  # Convert to ms
            
#             # Display results
#             self.results_text.insert(tk.END, f"Top {k} Most Similar Documents:\n")
#             self.results_text.insert(tk.END, "-" * 50 + "\n\n")
            
#             for rank, result in enumerate(results['top_results'], 1):
#                 self.results_text.insert(tk.END, f"Rank #{rank}\n")
#                 self.results_text.insert(tk.END, f"  Document ID: {result['id']}\n")
#                 self.results_text.insert(tk.END, f"  Vector: {result['values']}\n")
#                 self.results_text.insert(tk.END, f"  Similarity Score: {result['similarity']:.2f}\n\n")
            
#             # Display stats
#             self.stats_text.insert(tk.END, "EXECUTION STATISTICS\n")
#             self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
#             self.stats_text.insert(tk.END, f"Execution Time: {execution_time:.3f} ms\n")
#             self.stats_text.insert(tk.END, f"Total Documents: {len(self.documents)}\n")
#             self.stats_text.insert(tk.END, f"Processors Used: {num_processors}\n")
#             self.stats_text.insert(tk.END, f"Docs per Processor: ~{len(self.documents)//num_processors}\n\n")
            
#             self.stats_text.insert(tk.END, "Processor Distribution:\n")
#             self.stats_text.insert(tk.END, "-" * 50 + "\n")
#             for proc_info in results['processor_distribution']:
#                 self.stats_text.insert(tk.END, 
#                     f"Processor {proc_info['processor']}: Docs {proc_info['docs']}\n")
            
#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred: {str(e)}")


# # Parallel processing functions (must be at module level for multiprocessing)
# def calculate_similarity(doc_data):
#     """Calculate similarity for a single document"""
#     doc, query = doc_data
#     similarity = sum(d ** q for d, q in zip(doc['values'], query))
#     return {'id': doc['id'], 'values': doc['values'], 'similarity': similarity}


# def parallel_document_search(documents, query, k, num_processors):
#     """
#     Perform parallel document search using multiprocessing.
#     This actually uses multiple CPU cores for true parallelization.
#     """
#     # Prepare data for parallel processing
#     doc_query_pairs = [(doc, query) for doc in documents]
    
#     # Create processor distribution info
#     docs_per_proc = len(documents) // num_processors
#     processor_distribution = []
#     for i in range(num_processors):
#         start = i * docs_per_proc
#         end = start + docs_per_proc if i < num_processors - 1 else len(documents)
#         processor_distribution.append({
#             'processor': i,
#             'docs': list(range(start, end))
#         })
    
#     # Use multiprocessing Pool for TRUE parallelization
#     with Pool(processes=num_processors) as pool:
#         # Map the similarity calculation across multiple processes
#         similarities = pool.map(calculate_similarity, doc_query_pairs)
    
#     # Sort by similarity (descending)
#     similarities.sort(key=lambda x: x['similarity'], reverse=True)
    
#     # Get top K results
#     top_results = similarities[:k]
    
#     return {
#         'top_results': top_results,
#         'processor_distribution': processor_distribution
#     }


# if __name__ == '__main__':
#     # Required for multiprocessing on Windows
#     mp.freeze_support()
    
#     root = tk.Tk()
#     app = ParallelDocumentSearchGUI(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import multiprocessing as mp
from multiprocessing import Pool
import time
import os

class ParallelDocumentSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel Document Search System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f4f8')
        
        # Default data
        self.documents = []
        self.query = []
        self.documents_file = None
        self.query_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#2c3e50', relief=tk.RAISED, bd=3)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🔍 Parallel Document Search System", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white', pady=15)
        title_label.pack()
        
        # Content frame (left and right panels)
        content_frame = tk.Frame(main_frame, bg='#f0f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel
        left_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right Panel
        right_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)
        
    def setup_left_panel(self, parent):
        # File Loading Section
        file_frame = tk.LabelFrame(parent, text="Load Files", font=('Arial', 12, 'bold'),
                                   bg='#e8f4f8', fg='#2c3e50', padx=10, pady=10)
        file_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Documents file
        docs_file_frame = tk.Frame(file_frame, bg='#e8f4f8')
        docs_file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(docs_file_frame, text="Documents:", bg='#e8f4f8', 
                font=('Arial', 10), width=12, anchor='w').pack(side=tk.LEFT)
        self.docs_file_label = tk.Label(docs_file_frame, text="No file loaded", 
                                        bg='white', relief=tk.SUNKEN, anchor='w')
        self.docs_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(docs_file_frame, text="Browse", command=self.load_documents,
                 bg='#3498db', fg='white', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Query file
        query_file_frame = tk.Frame(file_frame, bg='#e8f4f8')
        query_file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(query_file_frame, text="Query:", bg='#e8f4f8', 
                font=('Arial', 10), width=12, anchor='w').pack(side=tk.LEFT)
        self.query_file_label = tk.Label(query_file_frame, text="No file loaded", 
                                         bg='white', relief=tk.SUNKEN, anchor='w')
        self.query_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(query_file_frame, text="Browse", command=self.load_query,
                 bg='#3498db', fg='white', font=('Arial', 9)).pack(side=tk.LEFT)
        
        # Parameters Section
        params_frame = tk.LabelFrame(parent, text="Parameters", font=('Arial', 12, 'bold'),
                                    bg='#f8e8f8', fg='#2c3e50', padx=10, pady=10)
        params_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(params_frame, text="Top K Documents:", bg='#f8e8f8', 
                font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.k_var = tk.StringVar(value='5')
        tk.Entry(params_frame, textvariable=self.k_var, width=10, 
                font=('Arial', 10)).grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(params_frame, text="Number of Processors:", bg='#f8e8f8',
                font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.proc_var = tk.StringVar(value='4')
        tk.Entry(params_frame, textvariable=self.proc_var, width=10,
                font=('Arial', 10)).grid(row=1, column=1, pady=5, padx=10)
        
        # Action Buttons
        button_frame = tk.Frame(parent, bg='#ffffff')
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(button_frame, text="▶ Run Search", command=self.run_search,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="📝 Create Sample Files", command=self.create_sample_files,
                 bg='#e67e22', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(fill=tk.X, pady=5)
        
        # Documents List
        docs_frame = tk.LabelFrame(parent, text=f"Documents ({len(self.documents)})",
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0',
                                  fg='#2c3e50', padx=10, pady=10)
        docs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.docs_text = scrolledtext.ScrolledText(docs_frame, height=15, width=40,
                                                   font=('Courier', 10), bg='#ffffff')
        self.docs_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_right_panel(self, parent):
        # Query Display
        query_frame = tk.LabelFrame(parent, text="Query Vector", 
                                   font=('Arial', 12, 'bold'), bg='#fff8e8',
                                   fg='#2c3e50', padx=10, pady=10)
        query_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.query_text = tk.Text(query_frame, height=3, width=50,
                                 font=('Courier', 11), bg='#fffef0')
        self.query_text.pack(fill=tk.X)
        
        # Results Section
        results_frame = tk.LabelFrame(parent, text="Search Results", 
                                     font=('Arial', 12, 'bold'), bg='#e8f8e8',
                                     fg='#2c3e50', padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=50,
                                                     font=('Courier', 10), bg='#ffffff')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Stats Section
        stats_frame = tk.LabelFrame(parent, text="Performance Statistics",
                                   font=('Arial', 12, 'bold'), bg='#ffe8e8',
                                   fg='#2c3e50', padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=50,
                                 font=('Courier', 10), bg='#fffef0')
        self.stats_text.pack(fill=tk.X)
    
    def load_documents(self):
        filename = filedialog.askopenfilename(
            title="Select Documents File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.documents = parse_documents_file(filename)
                self.documents_file = filename
                self.docs_file_label.config(text=os.path.basename(filename))
                self.update_docs_display()
                messagebox.showinfo("Success", f"Loaded {len(self.documents)} documents!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load documents:\n{str(e)}")
    
    def load_query(self):
        filename = filedialog.askopenfilename(
            title="Select Query File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.query = parse_query_file(filename)
                self.query_file = filename
                self.query_file_label.config(text=os.path.basename(filename))
                self.update_query_display()
                messagebox.showinfo("Success", f"Loaded query with {len(self.query)} dimensions!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load query:\n{str(e)}")
    
    def update_docs_display(self):
        self.docs_text.delete('1.0', tk.END)
        for doc in self.documents:
            self.docs_text.insert(tk.END, f"Doc {doc['id']:2d}: {doc['values']}\n")
        # Update label
        parent = self.docs_text.master
        parent.config(text=f"Documents ({len(self.documents)})")
    
    def update_query_display(self):
        self.query_text.delete('1.0', tk.END)
        self.query_text.insert(tk.END, f"Query Vector: {self.query}\n")
        self.query_text.insert(tk.END, f"Dimensions: {len(self.query)}")
    
    def create_sample_files(self):
        try:
            # Create sample documents.txt
            with open('documents.txt', 'w') as f:
                f.write("0: 5 7 6\n")
                f.write("1: 2 6 5\n")
                f.write("2: 7 2 1\n")
                f.write("3: 6 3 9\n")
                f.write("4: 6 2 6\n")
                f.write("5: 9 7 8\n")
                f.write("6: 3 2 0\n")
                f.write("7: 2 9 5\n")
                f.write("8: 7 9 8\n")
                f.write("9: 2 1 6\n")
            
            # Create sample query.txt
            with open('query.txt', 'w') as f:
                f.write("3 2 1\n")
            
            messagebox.showinfo("Success", 
                "Sample files created:\n- documents.txt\n- query.txt\n\nYou can now load them!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample files:\n{str(e)}")
    
    def run_search(self):
        if not self.documents:
            messagebox.showwarning("Warning", "Please load a documents file first!")
            return
        
        if not self.query:
            messagebox.showwarning("Warning", "Please load a query file first!")
            return
        
        try:
            k = int(self.k_var.get())
            num_processors = int(self.proc_var.get())
            
            if k > len(self.documents):
                k = len(self.documents)
            
            self.results_text.delete('1.0', tk.END)
            self.stats_text.delete('1.0', tk.END)
            
            self.results_text.insert(tk.END, "Processing with TRUE PARALLELIZATION...\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.root.update()
            
            # Run parallel search
            start_time = time.time()
            results = parallel_document_search(self.documents, self.query, k, num_processors)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Display results
            self.results_text.insert(tk.END, f"Top {k} Most Similar Documents:\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n\n")
            
            for rank, result in enumerate(results['top_results'], 1):
                self.results_text.insert(tk.END, f"Rank #{rank}\n")
                self.results_text.insert(tk.END, f"  Document ID: {result['id']}\n")
                self.results_text.insert(tk.END, f"  Vector: {result['values']}\n")
                self.results_text.insert(tk.END, f"  Similarity Score: {result['similarity']:.2f}\n\n")
            
            # Display stats
            self.stats_text.insert(tk.END, "EXECUTION STATISTICS\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
            self.stats_text.insert(tk.END, f"Execution Time: {execution_time:.3f} ms\n")
            self.stats_text.insert(tk.END, f"Total Documents: {len(self.documents)}\n")
            self.stats_text.insert(tk.END, f"Processors Used: {num_processors}\n")
            self.stats_text.insert(tk.END, f"Docs per Processor: ~{len(self.documents)//num_processors}\n\n")
            
            self.stats_text.insert(tk.END, "Processor Distribution:\n")
            self.stats_text.insert(tk.END, "-" * 50 + "\n")
            for proc_info in results['processor_distribution']:
                self.stats_text.insert(tk.END, 
                    f"Processor {proc_info['processor']}: Docs {proc_info['docs']}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# File parsing functions
def parse_documents_file(filename):
    """
    Parse documents file in format:
    0: 5 7 6
    1: 2 6 5
    etc.
    """
    documents = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split by colon
            parts = line.split(':')
            if len(parts) != 2:
                continue
            
            doc_id = int(parts[0].strip())
            values = [int(x) for x in parts[1].strip().split()]
            
            documents.append({
                'id': doc_id,
                'values': values
            })
    
    return documents


def parse_query_file(filename):
    """
    Parse query file - single line of space-separated integers:
    3 2 1
    """
    with open(filename, 'r') as f:
        line = f.readline().strip()
        query = [int(x) for x in line.split()]
    return query


# Parallel processing functions (must be at module level for multiprocessing)
def calculate_similarity(doc_data):
    """Calculate similarity for a single document"""
    doc, query = doc_data
    similarity = sum(d ** q for d, q in zip(doc['values'], query))
    return {'id': doc['id'], 'values': doc['values'], 'similarity': similarity}


def parallel_document_search(documents, query, k, num_processors):
    """
    Perform parallel document search using multiprocessing.
    This actually uses multiple CPU cores for true parallelization.
    """
    # Prepare data for parallel processing
    doc_query_pairs = [(doc, query) for doc in documents]
    
    # Create processor distribution info
    docs_per_proc = len(documents) // num_processors
    processor_distribution = []
    for i in range(num_processors):
        start = i * docs_per_proc
        end = start + docs_per_proc if i < num_processors - 1 else len(documents)
        processor_distribution.append({
            'processor': i,
            'docs': list(range(start, end))
        })
    
    # Use multiprocessing Pool for TRUE parallelization
    with Pool(processes=num_processors) as pool:
        # Map the similarity calculation across multiple processes
        similarities = pool.map(calculate_similarity, doc_query_pairs)
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Get top K results
    top_results = similarities[:k]
    
    return {
        'top_results': top_results,
        'processor_distribution': processor_distribution
    }


if __name__ == '__main__':
    # Required for multiprocessing on Windows
    mp.freeze_support()
    
    root = tk.Tk()
    app = ParallelDocumentSearchGUI(root)
    root.mainloop()