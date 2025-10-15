import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import multiprocessing as mp
from multiprocessing import Pool
import time
import os

class ParallelDocumentSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Research Paper Search System")
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
        title_frame = tk.Frame(main_frame, bg='#1a237e', relief=tk.RAISED, bd=3)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="📚 Research Paper Search System", 
                              font=('Arial', 24, 'bold'), bg='#1a237e', fg='white', pady=15)
        title_label.pack()
        
        subtitle = tk.Label(title_frame, text="Parallel Document Retrieval Using Multiprocessing", 
                           font=('Arial', 11), bg='#1a237e', fg='#b3e5fc', pady=5)
        subtitle.pack()
        
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
        file_frame = tk.LabelFrame(parent, text="📁 Load Input Files", font=('Arial', 12, 'bold'),
                                   bg='#e3f2fd', fg='#1565c0', padx=10, pady=10)
        file_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Documents file
        docs_file_frame = tk.Frame(file_frame, bg='#e3f2fd')
        docs_file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(docs_file_frame, text="Research Papers:", bg='#e3f2fd', 
                font=('Arial', 10, 'bold'), width=15, anchor='w').pack(side=tk.LEFT)
        self.docs_file_label = tk.Label(docs_file_frame, text="No file loaded", 
                                        bg='white', relief=tk.SUNKEN, anchor='w', fg='#666')
        self.docs_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(docs_file_frame, text="📂 Browse", command=self.load_documents,
                 bg='#1976d2', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        
        # Query file
        query_file_frame = tk.Frame(file_frame, bg='#e3f2fd')
        query_file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(query_file_frame, text="Search Query:", bg='#e3f2fd', 
                font=('Arial', 10, 'bold'), width=15, anchor='w').pack(side=tk.LEFT)
        self.query_file_label = tk.Label(query_file_frame, text="No file loaded", 
                                         bg='white', relief=tk.SUNKEN, anchor='w', fg='#666')
        self.query_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(query_file_frame, text="📂 Browse", command=self.load_query,
                 bg='#1976d2', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        
        # Parameters Section
        params_frame = tk.LabelFrame(parent, text="⚙️ Search Parameters", font=('Arial', 12, 'bold'),
                                    bg='#f3e5f5', fg='#6a1b9a', padx=10, pady=10)
        params_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(params_frame, text="Top K Results:", bg='#f3e5f5', 
                font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.k_var = tk.StringVar(value='10')
        tk.Entry(params_frame, textvariable=self.k_var, width=10, 
                font=('Arial', 10)).grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(params_frame, text="CPU Cores:", bg='#f3e5f5',
                font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.proc_var = tk.StringVar(value='4')
        tk.Entry(params_frame, textvariable=self.proc_var, width=10,
                font=('Arial', 10)).grid(row=1, column=1, pady=5, padx=10)
        
        # Action Buttons
        button_frame = tk.Frame(parent, bg='#ffffff')
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(button_frame, text="🔍 Search Papers", command=self.run_search,
                 bg='#2e7d32', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="📝 Generate Sample Data", command=self.create_sample_files,
                 bg='#d84315', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(fill=tk.X, pady=5)
        
        # Documents List
        docs_frame = tk.LabelFrame(parent, text=f"📄 Research Papers Database ({len(self.documents)})",
                                  font=('Arial', 12, 'bold'), bg='#e8f5e9',
                                  fg='#1b5e20', padx=10, pady=10)
        docs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.docs_text = scrolledtext.ScrolledText(docs_frame, height=15, width=40,
                                                   font=('Courier', 9), bg='#ffffff')
        self.docs_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_right_panel(self, parent):
        # Query Display
        query_frame = tk.LabelFrame(parent, text="🔎 Search Query Features", 
                                   font=('Arial', 12, 'bold'), bg='#fff3e0',
                                   fg='#e65100', padx=10, pady=10)
        query_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.query_text = tk.Text(query_frame, height=3, width=50,
                                 font=('Courier', 11), bg='#fffef0')
        self.query_text.pack(fill=tk.X)
        
        # Results Section
        results_frame = tk.LabelFrame(parent, text="📊 Search Results (Ranked by Relevance)", 
                                     font=('Arial', 12, 'bold'), bg='#e1f5fe',
                                     fg='#01579b', padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=50,
                                                     font=('Courier', 9), bg='#ffffff')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Stats Section
        stats_frame = tk.LabelFrame(parent, text="⚡ Performance Metrics",
                                   font=('Arial', 12, 'bold'), bg='#fce4ec',
                                   fg='#880e4f', padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=50,
                                 font=('Courier', 9), bg='#fff8f8')
        self.stats_text.pack(fill=tk.X)
    
    def load_documents(self):
        filename = filedialog.askopenfilename(
            title="Select Research Papers File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.documents = parse_documents_file(filename)
                self.documents_file = filename
                self.docs_file_label.config(text=os.path.basename(filename), fg='#2e7d32')
                self.update_docs_display()
                messagebox.showinfo("Success", f"✅ Loaded {len(self.documents)} research papers!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load papers:\n{str(e)}")
    
    def load_query(self):
        filename = filedialog.askopenfilename(
            title="Select Query File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.query = parse_query_file(filename)
                self.query_file = filename
                self.query_file_label.config(text=os.path.basename(filename), fg='#2e7d32')
                self.update_query_display()
                messagebox.showinfo("Success", f"✅ Loaded query with {len(self.query)} features!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load query:\n{str(e)}")
    
    def update_docs_display(self):
        self.docs_text.delete('1.0', tk.END)
        for doc in self.documents:
            self.docs_text.insert(tk.END, f"Paper {doc['id']:3d}: {doc['values']}\n")
        # Update label
        parent = self.docs_text.master
        parent.config(text=f"📄 Research Papers Database ({len(self.documents)})")
    
    def update_query_display(self):
        self.query_text.delete('1.0', tk.END)
        self.query_text.insert(tk.END, f"Feature Vector: {self.query}\n")
        self.query_text.insert(tk.END, f"Total Features: {len(self.query)}")
    
    def create_sample_files(self):
        try:
            # Create sample research_papers.txt with topic vectors
            # Vector represents: [AI, ML, DataScience, ComputerVision, NLP, Security, Networking, HPC]
            with open('research_papers.txt', 'w') as f:
                f.write("# Research Papers - Feature Vectors\n")
                f.write("# Features: AI, ML, DataScience, ComputerVision, NLP, Security, Networking, HPC\n\n")
                f.write("100: 8 9 7 6 8 2 3 4\n")  # AI/ML focused paper
                f.write("101: 7 8 9 5 7 3 2 5\n")  # Data Science heavy
                f.write("102: 9 8 6 9 7 1 2 3\n")  # Computer Vision focused
                f.write("103: 8 7 5 4 9 2 1 3\n")  # NLP focused
                f.write("104: 5 6 4 3 5 9 8 7\n")  # Security & Networking
                f.write("105: 6 7 8 7 6 5 4 9\n")  # HPC focused
                f.write("106: 9 9 8 8 9 3 2 4\n")  # Comprehensive AI/ML
                f.write("107: 4 5 3 2 4 8 9 6\n")  # Network Security
                f.write("108: 7 8 9 6 8 4 3 8\n")  # ML & HPC
                f.write("109: 8 7 6 9 8 2 3 5\n")  # Vision & NLP
                f.write("110: 6 5 4 3 7 7 8 4\n")  # Security focused
                f.write("111: 9 8 7 8 9 3 4 6\n")  # AI/Vision/NLP
                f.write("112: 5 6 8 4 5 6 9 7\n")  # Network & HPC
                f.write("113: 8 9 9 7 8 2 3 7\n")  # Data Science & AI
                f.write("114: 7 6 5 8 7 4 5 6\n")  # Balanced paper
                f.write("115: 9 9 8 9 9 1 2 3\n")  # Top AI research
            
            # Create sample search_query.txt
            # Looking for AI + ML + Computer Vision papers
            with open('search_query.txt', 'w') as f:
                f.write("# Query for AI + ML + Computer Vision research\n")
                f.write("2 2 1 2 1 1 1 1\n")
            
            messagebox.showinfo("Success", 
                "✅ Sample files created:\n\n"
                "📄 research_papers.txt\n"
                "   - 16 research papers with feature vectors\n"
                "   - Features: AI, ML, Data Science, CV, NLP, Security, Networks, HPC\n\n"
                "🔎 search_query.txt\n"
                "   - Query for AI/ML/Computer Vision papers\n\n"
                "You can now load them using the Browse buttons!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample files:\n{str(e)}")
    
    def run_search(self):
        if not self.documents:
            messagebox.showwarning("Warning", "Please load a research papers file first!")
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
            
            self.results_text.insert(tk.END, "🚀 Processing with TRUE PARALLEL EXECUTION...\n")
            self.results_text.insert(tk.END, "=" * 55 + "\n\n")
            self.root.update()
            
            # Run parallel search
            start_time = time.time()
            results = parallel_document_search(self.documents, self.query, k, num_processors)
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Display results
            self.results_text.insert(tk.END, f"📊 Top {k} Most Relevant Research Papers:\n")
            self.results_text.insert(tk.END, "-" * 55 + "\n\n")
            
            for rank, result in enumerate(results['top_results'], 1):
                self.results_text.insert(tk.END, f"🏆 Rank #{rank}\n")
                self.results_text.insert(tk.END, f"   Paper ID: {result['id']}\n")
                self.results_text.insert(tk.END, f"   Features: {result['values']}\n")
                self.results_text.insert(tk.END, f"   Relevance Score: {result['similarity']:.2f}\n\n")
            
            # Display stats
            self.stats_text.insert(tk.END, "⚡ PERFORMANCE STATISTICS\n")
            self.stats_text.insert(tk.END, "=" * 55 + "\n\n")
            self.stats_text.insert(tk.END, f"⏱️  Execution Time: {execution_time:.3f} ms\n")
            self.stats_text.insert(tk.END, f"📚 Total Papers: {len(self.documents)}\n")
            self.stats_text.insert(tk.END, f"💻 CPU Cores Used: {num_processors}\n")
            self.stats_text.insert(tk.END, f"📊 Papers/Core: ~{len(self.documents)//num_processors}\n\n")
            
            self.stats_text.insert(tk.END, "🔄 Parallel Processing Distribution:\n")
            self.stats_text.insert(tk.END, "-" * 55 + "\n")
            for proc_info in results['processor_distribution']:
                doc_list = ', '.join(str(d) for d in proc_info['docs'])
                self.stats_text.insert(tk.END, 
                    f"Core {proc_info['processor']}: Papers [{doc_list}]\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# File parsing functions
def parse_documents_file(filename):
    """
    Parse documents file in format:
    100: 8 9 7 6 8 2 3 4
    """
    documents = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
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
    Parse query file - single line of space-separated integers
    """
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            query = [int(x) for x in line.split()]
            return query
    return []


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