import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class MegaSenaInterface:
    def __init__(self, generator):
        self.generator = generator
        self.root = tk.Tk()
        self.root.title("Mega-Sena Optimizer")
        self.root.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Generate button
        ttk.Button(main_frame, text="Generate Combinations", 
                  command=self.generate_combinations).grid(row=0, column=0, pady=10)
        
        # Results area
        self.results_text = tk.Text(main_frame, height=20, width=80)
        self.results_text.grid(row=1, column=0, pady=10)
        
        # Save button
        ttk.Button(main_frame, text="Save Combinations", 
                  command=self.save_combinations).grid(row=2, column=0, pady=10)
        
        # Statistics button
        ttk.Button(main_frame, text="Show Statistics", 
                  command=self.show_statistics).grid(row=3, column=0, pady=10)
    
    def generate_combinations(self):
        """Generate and display combinations"""
        combinations = self.generator.generate_combinations()
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "Generated Combinations:\n\n")
        for i, combo in enumerate(combinations, 1):
            prob = self.generator.calculate_combination_probability(combo)
            self.results_text.insert(tk.END, 
                f"Combination {i}: {combo}\n"
                f"Probability: {prob:.10f}\n\n")
    
    def save_combinations(self):
        """Save the generated combinations to a file"""
        content = self.results_text.get(1.0, tk.END)
        if content.strip():
            filename = f"mega_sena_combinations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Combinations saved to {filename}")
        else:
            messagebox.showwarning("Warning", "No combinations to save!")
    
    def show_statistics(self):
        """Display statistical analysis"""
        stats = self.generator.analyzer.get_number_stats()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Mega-Sena Statistics")
        stats_window.geometry("600x400")
        
        text_widget = tk.Text(stats_window, height=20, width=60)
        text_widget.pack(padx=10, pady=10)
        
        text_widget.insert(tk.END, "Statistical Analysis:\n\n")
        
        # Most frequent numbers
        text_widget.insert(tk.END, "Top 10 Most Frequent Numbers:\n")
        sorted_freq = sorted(stats['frequency'].items(), key=lambda x: x[1], reverse=True)[:10]
        for num, freq in sorted_freq:
            text_widget.insert(tk.END, f"Number {num}: {freq} times\n")
        
        # Even/Odd ratio
        text_widget.insert(tk.END, f"\nEven/Odd Ratio: {stats['even_odd_ratio']:.2f}\n")
        
        # Decade distribution
        text_widget.insert(tk.END, "\nDecade Distribution:\n")
        for decade, count in sorted(stats['decade_distribution'].items()):
            range_start = decade * 10 + 1
            range_end = range_start + 9
            text_widget.insert(tk.END, f"{range_start}-{range_end}: {count}\n")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()