#!/usr/bin/env python
"""Real estate web crawler gui"""
import Tkinter
import ttk
import tkFileDialog
import realestate


def main():
    """Load the gui"""
    top = Tkinter.Tk()
    frame = ttk.Frame(top)
    frame.grid()
    command = Tkinter.StringVar(top, 'buy')
    group = ttk.LabelFrame(frame, text='Listing type')
    group.grid(row=0, column=0)
    for opt in 'buy', 'rent', 'sold':
        ttk.Radiobutton(group, text=opt, variable=command, value=opt).grid()
    search = ttk.Entry(frame)
    search.grid(row=0, column=1)

    def export():
        """Run the real estate program"""
        types = 'CSV {.csv}', 'Text {.txt}', 'All *'
        filehandle = tkFileDialog.asksaveasfile(filetypes=types)
        if filehandle:
            realestate.realestate(command.get(), search.get(), filehandle)
            filehandle.close()

    button = ttk.Button(frame, text='Fetch', command=export)
    button.grid(row=0, column=2)
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    top.mainloop()

if __name__ == '__main__':
    main()
