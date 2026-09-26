#!/usr/bin/python3

# -*- coding: utf-8 -*-
#
# ios-to-sailfish - A collection of Python scripts to easily migrate from iOS to SailfishOS
# Copyright (c) 2026 G. Baudic
#
# ios-to-sailfish is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ios-to-sailfish is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This class was AI generated

import importlib.util
import inspect
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from extractor import Extractor
from ios2sailfish import load_plugins


class IosToSailfishUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("iOS to Sailfish exporter")
        self.geometry("700x500")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.plugins = []
        self.check_vars = []

        self.create_widgets()

        # Initialize with empty directories or defaults
        self.set_directory(self.input_dir, None)
        self.set_directory(self.output_dir, None)

    def create_widgets(self):
        # Top frame: input and output directories
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Input directory row
        self._create_dir_row(top_frame, "Backup directory:", self.input_dir, 0)

        # Output directory row
        self._create_dir_row(top_frame, "Output directory:", self.output_dir, 1)

        # Middle frame: plugin list
        middle_frame = ttk.Frame(self)
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable canvas for plugins list with checkboxes
        self.plugin_canvas = tk.Canvas(middle_frame)
        self.plugin_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=self.plugin_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.plugin_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside canvas to hold plugin items
        self.plugin_frame = ttk.Frame(self.plugin_canvas)
        self.plugin_canvas.create_window((0, 0), window=self.plugin_frame, anchor="nw")

        self.plugin_frame.bind("<Configure>", self._on_frame_configure)

        # Bottom frame with Run button aligned bottom right
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.run_button = ttk.Button(bottom_frame, text="Run", command=self.run_selected_plugins)
        self.run_button.pack(side=tk.RIGHT)

    def _create_dir_row(self, parent, label_text, var, row):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, pady=2)

        # Non-editable text box showing directory
        text_box = ttk.Entry(parent, textvariable=var, width=60, state="readonly")
        text_box.grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=2)

        # Button for selecting folder dialog
        btn = ttk.Button(parent, text="Browse...", command=lambda v=var: self.select_directory(v))
        btn.grid(row=row, column=2, padx=5, pady=2)

    def select_directory(self, var):
        selected = filedialog.askdirectory()
        if selected:
            self.set_directory(var, selected)

    def set_directory(self, var, path):
        if not path:
            var.set("")
        else:
            var.set(path)

    def reload_plugins(self):
        # Clear previous plugins & UI
        for widget in self.plugin_frame.winfo_children():
            widget.destroy()
        self.plugins.clear()
        self.check_vars.clear()

        # Load plugins from current input directory

        try:
            self.plugins = load_plugins('plugins', self.input_dir.get(), self.output_dir.get())
        except Exception as e:
            print(f"Failed to load plugins: {e}")
            self.plugins = []

        # Create UI entries for each plugin: checkbox, name, description
        for i, plugin in enumerate(self.plugins):
            var = tk.BooleanVar(value=True)
            self.check_vars.append(var)

            cb = ttk.Checkbutton(self.plugin_frame, variable=var)
            cb.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)

            name_label = ttk.Label(self.plugin_frame, text=plugin.__class__.__name__, width=20)
            name_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)

            desc_text = plugin.__doc__ or ""
            desc_label = ttk.Label(self.plugin_frame, text=desc_text, wraplength=450, justify=tk.LEFT)
            desc_label.grid(row=i, column=2, sticky=tk.W, padx=5, pady=2)

        self.plugin_frame.update_idletasks()
        self.plugin_canvas.config(scrollregion=self.plugin_canvas.bbox("all"))

    def _on_frame_configure(self, event):
        self.plugin_canvas.configure(scrollregion=self.plugin_canvas.bbox("all"))

    def run_selected_plugins(self):
        # Call apply() on each checked plugin
        selected_plugins = [p for p, var in zip(self.plugins, self.check_vars) if var.get()]
        if not selected_plugins:
            messagebox.showwarning(message="No plugins selected to run.")
            return
        if not self.input_dir.get():
            messagebox.showerror(message="No input directory chosen!")
            return
        if not self.output_dir.get():
            messagebox.showerror(message="No output directory chosen!")
            return
        self.run_button.config(state=tk.DISABLED)

        print(f"Running {len(selected_plugins)} plugin(s)...")
        for plugin in selected_plugins:
            plugin.set_output_dir(self.output_dir.get())
            plugin.set_backup_dir(self.input_dir.get())
            try:
                plugin.apply()
            except Exception as e:
                print(f"Plugin {plugin.__class__.__name__} failed with error: {e}")
        self.run_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = IosToSailfishUI()
    app.reload_plugins()
    app.mainloop()
