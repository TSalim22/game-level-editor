import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from levels import TILES, new_level, paint, load_level, save_level, check_assets

CELL = 28


class Editor:
    def __init__(self,root):
        self.root = root
        self.level = new_level()
        self.dirty = False
        root.title('Student Level Editor')
        toolbar = ttk.Frame(root,padding=12)
        toolbar.pack(fill='x')
        for title,command in [('New',self.new),('Open',self.open),('Save',self.save),('Check asset folder',self.assets)]:
            ttk.Button(toolbar,text=title,command=command).pack(side='left',padx=3)
        self.selection = tk.StringVar(value='Wall')
        ttk.Combobox(toolbar,textvariable=self.selection,values=[value[0] for value in TILES.values()],state='readonly',width=12).pack(side='left',padx=10)
        self.canvas = tk.Canvas(root,background='white',highlightthickness=0)
        self.canvas.pack(padx=12,pady=12)
        self.canvas.bind('<Button-1>',self.paint)
        self.canvas.bind('<B1-Motion>',self.paint)
        self.canvas.bind('<Button-3>',lambda event:self.paint(event,erase=True))
        self.status = tk.StringVar()
        ttk.Label(root,textvariable=self.status,padding=12).pack(fill='x')
        root.protocol('WM_DELETE_WINDOW',self.close)
        self.draw()

    def draw(self):
        self.canvas.configure(width=self.level['width']*CELL,height=self.level['height']*CELL)
        self.canvas.delete('all')
        for y,row in enumerate(self.level['tiles']):
            for x,tile in enumerate(row):
                self.canvas.create_rectangle(x*CELL,y*CELL,(x+1)*CELL,(y+1)*CELL,fill=TILES[tile][1],outline='#c4ccd8')
        self.status.set(f"{self.level['width']} × {self.level['height']} · Left click or drag to paint · Right click to erase"+(' · Unsaved changes' if self.dirty else ''))

    def paint(self,event,erase=False):
        tile = 0 if erase else next(key for key,value in TILES.items() if value[0]==self.selection.get())
        paint(self.level,event.x//CELL,event.y//CELL,tile)
        self.dirty = True
        self.draw()

    def can_discard(self):
        return not self.dirty or messagebox.askyesno('Unsaved changes','Discard unsaved changes?',parent=self.root)

    def new(self):
        if self.can_discard():
            self.level = new_level()
            self.dirty = False
            self.draw()

    def open(self):
        if not self.can_discard(): return
        path = filedialog.askopenfilename(filetypes=[('JSON maps','*.json')])
        if not path: return
        try:
            level = load_level(path)
            self.level = level
            self.dirty = False
            self.draw()
        except (OSError,ValueError) as error:
            messagebox.showerror('Cannot open map',str(error),parent=self.root)

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON maps','*.json')])
        if not path: return
        try:
            save_level(path,self.level)
            self.dirty = False
            self.draw()
        except (OSError,ValueError) as error:
            messagebox.showerror('Cannot save map',str(error),parent=self.root)

    def assets(self):
        folder = filedialog.askdirectory()
        if folder:
            try:
                messagebox.showinfo('Asset checks','\n'.join(check_assets(folder)),parent=self.root)
            except OSError as error:
                messagebox.showerror('Cannot read assets',str(error),parent=self.root)

    def close(self):
        if self.can_discard(): self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    Editor(root)
    root.mainloop()
