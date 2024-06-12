import tkinter as tk
from tkinter import ttk, messagebox

# Create a list of available materials
materials = ['Titanium', 'Platinum', 'Gold', 'GaSb', 'AlSbAs', 'Custom']

class LayerEntry:
    def __init__(self, frame, row):
        self.material = tk.StringVar(value='Titanium')
        self.thickness = tk.StringVar(value='0')
        self.repeats = tk.StringVar(value='1')
        self.create_widgets(frame, row)

    def create_widgets(self, frame, row):
        self.material_menu = ttk.Combobox(frame, textvariable=self.material, values=materials)
        self.material_menu.grid(row=row, column=0, padx=5, pady=5)

        self.thickness_entry = tk.Entry(frame, textvariable=self.thickness)
        self.thickness_entry.grid(row=row, column=1, padx=5, pady=5)

        self.repeats_entry = tk.Entry(frame, textvariable=self.repeats)
        self.repeats_entry.grid(row=row, column=2, padx=5, pady=5)

class LayerInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Layer Input")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.create_header()
        self.layers = []
        self.add_layer()

        self.add_button = tk.Button(self.frame, text="Add Layer", command=self.add_layer)
        self.add_button.grid(row=999, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.frame, text="Save", command=self.save_layers)
        self.save_button.grid(row=999, column=1, padx=5, pady=5)

    def create_header(self):
        tk.Label(self.frame, text="Material").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame, text="Thickness (nm)").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame, text="Repeats").grid(row=0, column=2, padx=5, pady=5)

    def add_layer(self):
        row = len(self.layers) + 1
        new_layer = LayerEntry(self.frame, row)
        self.layers.append(new_layer)

    def save_layers(self):
        layer_data = []
        for layer in self.layers:
            try:
                thickness = float(layer.thickness.get())
                repeats = int(layer.repeats.get())
                material = layer.material.get()
                layer_data.append([material, thickness, repeats])
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for thickness and repeats.")
                return

        # Here you can process the `layer_data` as needed
        # For this example, we'll just print it
        print(layer_data)
        messagebox.showinfo("Layer Data", f"Saved Layers:\n{layer_data}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LayerInputApp(root)
    root.mainloop()
