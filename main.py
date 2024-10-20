import tkinter as tk
from tkinter import filedialog
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token

# Syntax Highlighting Editor Class
class SyntaxHighlightingEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighting Editor")
        self.root.geometry("800x600")

        # Create Text widget for editor with a uniform color initially
        self.text_area = tk.Text(self.root, wrap="none", undo=True, background="#282c34", 
                                 foreground="#abb2bf", insertbackground="white", font=("Courier New", 12))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        # Set Lexer for Python
        self.lexer = PythonLexer()

        # Define a style for syntax highlighting
        self.style = get_style_by_name('monokai')  # You can change this style

        # Create a Highlight button on the top right
        self.highlight_button = tk.Button(self.root, text="Highlight", command=self.syntax_highlighting)
        self.highlight_button.pack(anchor="ne", padx=10, pady=10)

        # Bind events for saving and opening files
        self.text_area.bind("<Control-s>", self.save_file)
        self.text_area.bind("<Control-o>", self.open_file)

    def syntax_highlighting(self, event=None):
        content = self.text_area.get("1.0", tk.END)
        tokens = self.lexer.get_tokens(content)
        
        # Clear tags
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)
        
        start_line, start_char = 1, 0

        for token_type, token_value in tokens:
            end_char = start_char + len(token_value)
            
            if "\n" in token_value:
                lines = token_value.split("\n")
                for i, line in enumerate(lines[:-1]):
                    self.apply_highlighting(token_type, start_line, start_char, start_char + len(line))
                    start_line += 1
                    start_char = 0
                start_char = len(lines[-1])
            else:
                self.apply_highlighting(token_type, start_line, start_char, end_char)
                start_char = end_char

    def apply_highlighting(self, token_type, line, start_char, end_char):
        # Apply different colors based on token types
        if token_type in Token.Keyword:
            self.text_area.tag_add("keyword", f"{line}.{start_char}", f"{line}.{end_char}")
            self.text_area.tag_config("keyword", foreground="#c678dd")  # Purple for keywords
        elif token_type in Token.String:
            self.text_area.tag_add("string", f"{line}.{start_char}", f"{line}.{end_char}")
            self.text_area.tag_config("string", foreground="#98c379")  # Green for strings
        elif token_type in Token.Comment:
            self.text_area.tag_add("comment", f"{line}.{start_char}", f"{line}.{end_char}")
            self.text_area.tag_config("comment", foreground="#5c6370", italic=True)  # Gray for comments
        elif token_type in Token.Name:
            self.text_area.tag_add("name", f"{line}.{start_char}", f"{line}.{end_char}")
            self.text_area.tag_config("name", foreground="#61afef")  # Blue for names
        elif token_type in Token.Operator:
            self.text_area.tag_add("operator", f"{line}.{start_char}", f"{line}.{end_char}")
            self.text_area.tag_config("operator", foreground="#d19a66")  # Orange for operators

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.root.title(f"Syntax Highlighting Editor - {file_path}")

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"Syntax Highlighting Editor - {file_path}")

# Initialize the main Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlightingEditor(root)
    root.mainloop()


