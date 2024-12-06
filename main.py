import tkinter as tk
from tkinter import filedialog
from pygments.lexers import PythonLexer
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Punctuation
from tkinter import messagebox


class SyntaxHighlightingEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighting Editor with Line Numbers")
        self.root.geometry("800x600")

        # Frame to hold line numbers and text area
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Line numbers
        self.line_numbers = tk.Text(
            self.main_frame,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background="#282c34",
            foreground="#abb2bf",
            state="disabled",
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Text area configuration
        self.text_area = tk.Text(
            self.main_frame,
            wrap="none",
            undo=True,
            background="#282c34",
            foreground="#abb2bf",
            insertbackground="white",
            font=("Courier New", 12),
        )
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attach scrollbar to both line numbers and text area
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        # Lexer for Python
        self.lexer = PythonLexer()

        # Menu bar
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Highlight button
        self.highlight_button = tk.Button(self.root, text="Highlight", command=self.syntax_highlighting)
        self.highlight_button.pack(anchor="ne", padx=10, pady=10)

        # Bindings for updating line numbers
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<Control-s>", self.save_file)
        self.text_area.bind("<Control-o>", self.open_file)

        # Initial update
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        line_count = int(self.text_area.index(tk.END).split(".")[0]) - 1
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_string)
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, *args):
        
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def open_file(self, event=None):
        
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.root.title(f"Syntax Highlighting Editor - {file_path}")
                self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self, event=None):
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END).strip())
                self.root.title(f"Syntax Highlighting Editor - {file_path}")
                messagebox.showinfo("Success", f"File saved as: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def syntax_highlighting(self):
        
        content = self.text_area.get("1.0", tk.END)
        tokens = self.lexer.get_tokens(content)

        # Remove existing tags
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)

        # Apply syntax highlighting
        start = 0
        for token_type, value in tokens:
            if value.strip():
                end = start + len(value)
                start_index = self.text_area.index(f"1.0+{start}c")
                end_index = self.text_area.index(f"1.0+{end}c")
                tag_name = str(token_type).split(".")[1].lower()  # Use token type as tag name
                self.text_area.tag_add(tag_name, start_index, end_index)
                self.text_area.tag_config(tag_name, foreground=self.get_token_color(token_type))
            start += len(value)

    def get_token_color(self, token_type):
        
        token_colors = {
            Keyword: "#ff79c6",        # 핑크 (키워드)
            Name: "#8be9fd",           # 밝은 하늘색 (이름)
            Comment: "#6272a4",        # 어두운 파란색 (주석)
            String: "#f1fa8c",         # 밝은 노란색 (문자열)
            Error: "#ff5555",          # 빨간색 (에러)
            Number: "#bd93f9",         # 보라색 (숫자)
            Operator: "#50fa7b",       # 밝은 녹색 (연산자)
            Punctuation: "#ffb86c",    # 주황색 (구두점)
        }
        for token_class, color in token_colors.items():
            if token_type in token_class:
                return color
        return "#ffffff"  # 기본 흰색



if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlightingEditor(root)
    root.mainloop()
