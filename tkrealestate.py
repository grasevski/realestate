#!/usr/bin/env python
"""Real estate web crawler gui"""
import Tkinter
import ttk
import tkFileDialog
import realestate


def main():
    """Load the gui"""
    top = Tkinter.Tk()
    frame = ttk.Frame(top, relief=Tkinter.RIDGE, borderwidth=2)
    frame.pack()
    command = Tkinter.StringVar(top, 'buy')
    options = 'buy', 'rent', 'sold'
    group = ttk.LabelFrame(frame, text='Listing types')
    group.grid(row=0, column=0)
    for index in range(len(options)):
        opt = options[index]
        btn = ttk.Radiobutton(group, text=opt, variable=command, value=opt)
        btn.pack()
    ttk.Label(frame, text='Search:').grid(row=0, column=1)
    search = ttk.Entry(frame)
    search.grid(row=0, column=2)

    def export():
        """Run the real estate program"""
        filehandle = tkFileDialog.asksaveasfile()
        realestate.realestate(command.get(), search.get(), filehandle)
        filehandle.close()

    button = ttk.Button(frame, text='Export', command=export)
    button.grid(row=0, column=3)
    top.mainloop()

if __name__ == '__main__':
    main()
