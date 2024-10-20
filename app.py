import tkinter as tk
from tkinter import filedialog, messagebox, font, simpledialog
import tkinter.font as tkFont

class NMSNote:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("NMSNote")
        self.pencere.geometry("1366x768")
        self.pencere.config(bg='white')

        self.pencere.bind("<B1-Motion>", self.pencere_tasima)

        self.yuvarlak_kenarli_pencere()

        self.temalar = {
            "Açık Tema": {"bg": "white", "fg": "black"},
            "Koyu Tema": {"bg": "#2c3e50", "fg": "#ecf0f1"}
        }
        self.gecerli_tema = "Açık Tema"
        self.gecerli_font = font.Font(family="Arial", size=14)

        self.yazi_alani = tk.Text(self.pencere, wrap='word', undo=True, bg=self.temalar[self.gecerli_tema]["bg"],
                                  fg=self.temalar[self.gecerli_tema]["fg"], font=self.gecerli_font)
        self.yazi_alani.place(x=30, y=30, width=540, height=540)

        menu_cubugu = tk.Menu(self.pencere)
        self.pencere.config(menu=menu_cubugu)

        dosya_menusu = tk.Menu(menu_cubugu)
        menu_cubugu.add_cascade(label="Dosya", menu=dosya_menusu)
        dosya_menusu.add_command(label="Yeni", command=self.yeni_dosya)
        dosya_menusu.add_command(label="Aç", command=self.dosya_ac)
        dosya_menusu.add_command(label="Kaydet", command=self.dosya_kaydet)
        dosya_menusu.add_command(label="Farklı Kaydet", command=self.farkli_kaydet)
        dosya_menusu.add_separator()
        dosya_menusu.add_command(label="Çıkış", command=self.pencere.quit)

        duzen_menusu = tk.Menu(menu_cubugu)
        menu_cubugu.add_cascade(label="Düzen", menu=duzen_menusu)
        duzen_menusu.add_command(label="Geri Al", command=self.yazi_alani.edit_undo)
        duzen_menusu.add_command(label="Yinele", command=self.yazi_alani.edit_redo)
        duzen_menusu.add_separator()
        duzen_menusu.add_command(label="Kes", command=lambda: self.pencere.focus_get().event_generate("<<Cut>>"))
        duzen_menusu.add_command(label="Kopyala", command=lambda: self.pencere.focus_get().event_generate("<<Copy>>"))
        duzen_menusu.add_command(label="Yapıştır", command=lambda: self.pencere.focus_get().event_generate("<<Paste>>"))
        duzen_menusu.add_command(label="Tümünü Seç", command=lambda: self.yazi_alani.tag_add("sel", "1.0", "end"))

        tema_menusu = tk.Menu(menu_cubugu)
        menu_cubugu.add_cascade(label="Tema", menu=tema_menusu)
        for tema_adi in self.temalar.keys():
            tema_menusu.add_command(label=tema_adi, command=lambda tema=tema_adi: self.tema_degistir(tema))

        ayarlar_menusu = tk.Menu(menu_cubugu)
        menu_cubugu.add_cascade(label="Ayarlar", menu=ayarlar_menusu)
        ayarlar_menusu.add_command(label="Font Seç", command=self.font_sec)

        self.yazi_alani.focus_set()

    def yeni_dosya(self):
        self.yazi_alani.delete(1.0, tk.END)

    def dosya_ac(self):
        dosya_yolu = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Tüm Dosyalar", "*.*"), ("Metin Dosyaları", "*.txt")])
        if dosya_yolu:
            with open(dosya_yolu, "r", encoding="utf-8") as dosya:
                self.yazi_alani.delete(1.0, tk.END)
                self.yazi_alani.insert(tk.END, dosya.read())

    def dosya_kaydet(self):
        uzanti = ".txt"  # Dosyayı doğrudan .txt olarak kaydedecek
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=uzanti, filetypes=[("Tüm Dosyalar", "*.*"), ("Metin Dosyaları", "*.txt")])
        if dosya_yolu:
            try:
                with open(dosya_yolu, "w", encoding="utf-8") as dosya:
                    dosya.write(self.yazi_alani.get(1.0, tk.END))
                messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}")

    def farkli_kaydet(self):
        self.dosya_kaydet()

    def tema_degistir(self, tema_adi):
        self.gecerli_tema = tema_adi
        self.yazi_alani.config(bg=self.temalar[tema_adi]["bg"], fg=self.temalar[tema_adi]["fg"])

    def font_sec(self):
        fontlar = list(tkFont.families())
        fontlar.sort()  # Fontları alfabetik olarak sıralar

        def font_secimi():
            secilen_index = font_secim_box.curselection()  # Seçilen fontun indeksini al
            if secilen_index:
                secilen_font = font_secim_box.get(secilen_index)  # Seçilen fontu al
                self.gecerli_font = font.Font(family=secilen_font, size=self.gecerli_font.actual("size"))
                self.yazi_alani.config(font=self.gecerli_font)

        secim_penceresi = tk.Toplevel(self.pencere)
        secim_penceresi.title("Font Seçimi")
        secim_penceresi.geometry("400x400")

        font_secim_box = tk.Listbox(secim_penceresi, height=20)
        for font_adi in fontlar:
            font_secim_box.insert(tk.END, font_adi)
        font_secim_box.pack(fill=tk.BOTH, expand=True)

        secim_buton = tk.Button(secim_penceresi, text="Seç", command=font_secimi)
        secim_buton.pack(pady=10)

    def yuvarlak_kenarli_pencere(self):
        self.canvas = tk.Canvas(self.pencere, width=600, height=600, bg='white', highlightthickness=0)
        self.canvas.create_oval(10, 10, 590, 590, fill='white', outline="")
        self.canvas.pack(fill='both', expand=True)

    def pencere_tasima(self, event):
        x = self.pencere.winfo_pointerx() - self.pencere.winfo_rootx()
        y = self.pencere.winfo_pointery() - self.pencere.winfo_rooty()
        self.pencere.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    pencere = tk.Tk()
    NMSNote = NMSNote(pencere)
    pencere.mainloop()
