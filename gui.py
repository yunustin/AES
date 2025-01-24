import customtkinter as ctk
import threading
from tkinterdnd2 import DND_FILES
from tkinter import filedialog, messagebox, PhotoImage, ttk, filedialog
from encryption import AESHandler
import os


ButtonBorderColour = "#194179"

class AESApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AES Şifreleme Uygulaması")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = 500
        window_height = 400
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.master.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.master.minsize(500, 400)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.key = None
        self.action_var = ctk.StringVar(value="encrypt")

        self.main_frame = ctk.CTkFrame(master)
        self.text_frame = ctk.CTkFrame(master)
        self.image_frame = ctk.CTkFrame(master)
        self.setup_main_frame()
        self.main_frame.pack(fill="both", expand=True)

    def setup_main_frame(self):
        self.batch_frame = ctk.CTkFrame(self.master)  # Toplu işlem için yeni çerçeve ekleme
        self.text_frame.pack_forget()
        self.image_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(self.main_frame, text="AES Şifreleme Uygulaması", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        key_options_frame = ctk.CTkFrame(self.main_frame)
        key_options_frame.pack(pady=10)
        ctk.CTkButton(key_options_frame, text="Anahtar Oluştur", command=self.generate_key, border_color= ButtonBorderColour, border_width=2).grid(row=0, column=0, padx=5)
        ctk.CTkButton(key_options_frame, text="Anahtarı İçe Aktar", command=self.import_key, border_color= ButtonBorderColour, border_width=2).grid(row=0, column=1, padx=5)
        ctk.CTkButton(key_options_frame, text="Anahtarı Dışa Aktar", command=self.export_key, border_color= ButtonBorderColour, border_width=2).grid(row=0, column=2, padx=5)

        ctk.CTkButton(self.main_frame, text="Metin Şifrele / Çöz", command=self.open_text_frame, border_color= ButtonBorderColour, border_width=2).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Görsel Şifrele / Çöz", command=self.open_image_frame, border_color= ButtonBorderColour, border_width=2).pack(pady=15)

        def change_theme(choice):
            if choice == "Light":
                ctk.set_appearance_mode("light")
                ButtonBorderColour= "#174D38"
            elif choice == "Dark":
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("dark-blue")

        themes = ["Light", "Dark",]  # Tema seçenekleri
        theme_menu = ctk.CTkOptionMenu(self.main_frame, values=themes, command=change_theme)
        theme_menu.set("Theme")
        theme_menu.pack(side="left", anchor="sw", padx=10, pady=10)  # Sol altta konumlanır



    def generate_key(self):
        self.key = AESHandler.generate_key()
        messagebox.showinfo("Anahtar", "Anahtar başarıyla oluşturuldu.")

    def import_key(self):
        filepath = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    self.key = f.read()
                messagebox.showinfo("Başarılı", "Anahtar başarıyla içe aktarıldı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Anahtar içe aktarma sırasında hata oluştu: {str(e)}")

    def export_key(self):
        if not self.key:
            messagebox.showerror("Hata", "Henüz bir anahtar oluşturulmadı.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key")])
        if filepath:
            try:
                with open(filepath, 'wb') as f:
                    f.write(self.key)
                messagebox.showinfo("Başarılı", "Anahtar başarıyla dışa aktarıldı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Anahtar dışa aktarma sırasında hata oluştu: {str(e)}")

    def open_text_frame(self):
        self.main_frame.pack_forget()
        self.image_frame.pack_forget()
        self.text_frame.pack(fill="both", expand=True)
        for widget in self.text_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.text_frame, text="Metin Şifreleme ve Çözme", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        text_input = ctk.CTkTextbox(self.text_frame, height=150, width=400)
        text_input.pack(pady=10)

        def encrypt_text():
            if not self.key:
                messagebox.showerror("Hata", "Lütfen önce bir anahtar oluşturun veya içe aktarın.")
                return
            text = text_input.get("1.0", "end").strip()
            if not text:
                messagebox.showerror("Hata", "Şifrelenecek metin alanı boş.")
                return
            try:
                encrypted_text = AESHandler.encrypt_text(self.key, text)
                text_input.delete("1.0", "end")
                text_input.insert("1.0", encrypted_text)
                messagebox.showinfo("Başarılı", "Metin başarıyla şifrelendi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifreleme sırasında bir hata oluştu: {str(e)}")

        def decrypt_text():
            if not self.key:
                messagebox.showerror("Hata", "Lütfen önce bir anahtar oluşturun veya içe aktarın.")
                return
            encrypted_text = text_input.get("1.0", "end").strip()
            if not encrypted_text:
                messagebox.showerror("Hata", "Çözülecek metin alanı boş.")
                return
            try:
                original_text = AESHandler.decrypt_text(self.key, encrypted_text)
                text_input.delete("1.0", "end")
                text_input.insert("1.0", original_text)
                messagebox.showinfo("Başarılı", "Metin başarıyla çözüldü.")
            except Exception as e:
                messagebox.showerror("Hata", f"Şifre çözme sırasında bir hata oluştu: {str(e)}")

        ctk.CTkButton(self.text_frame, text="Metni Şifrele", command=encrypt_text).pack(pady=5)
        ctk.CTkButton(self.text_frame, text="Metni Çöz", command=decrypt_text).pack(pady=5)
        ctk.CTkButton(self.text_frame, text="Geri Dön", command=self.setup_main_frame).pack(pady=15)

    def open_image_frame(self):
        self.main_frame.pack_forget()
        self.text_frame.pack_forget()
        self.image_frame.pack(fill="both", expand=True)
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.image_frame, text="Görsel Şifreleme ve Çözme", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        option_frame = ctk.CTkFrame(self.image_frame)
        option_frame.pack(pady=10)
        encrypt_option = ctk.CTkRadioButton(
            option_frame, text="Şifrele", value="encrypt", variable=self.action_var)
        encrypt_option.grid(row=0, column=0)
        decrypt_option = ctk.CTkRadioButton(
            option_frame, text="Çöz", value="decrypt", variable=self.action_var)
        decrypt_option.grid(row=0, column=1)
        encrypt_option.select()
        ctk.CTkButton(self.image_frame, text="Toplu Dosya İşleme", command=self.open_batch_processing,
                      border_color=ButtonBorderColour, border_width=2).pack(pady=15)
        drop_label = ctk.CTkLabel(self.image_frame, text="Bir dosya sürükleyip bırakın.")
        drop_label.pack(pady=20)


        def on_drop(event):
            if not self.key:
                messagebox.showerror("Hata", "Lütfen önce bir anahtar oluşturun veya içe aktarın.")
                return
            file_path = event.data.strip()
            if file_path.startswith('{') and file_path.endswith('}'):
                file_path = file_path[1:-1]
            file_path = os.path.normpath(file_path)
            try:
                if self.action_var.get() == "encrypt":
                    encrypted_file_path = AESHandler.encrypt_file(self.key, file_path)
                   # self.show_tick_image()  # Başarı görselini göster
                    messagebox.showinfo("Başarılı", f"Dosya başarıyla şifrelendi: {encrypted_file_path}")
                elif self.action_var.get() == "decrypt":
                    if not file_path.endswith(".enc"):
                        messagebox.showerror("Hata", ".enc uzantılı bir dosya seçmelisiniz.")
                        return
                    decrypted_file_path = AESHandler.decrypt_file(self.key, file_path)
                  #  self.show_tick_image()  # Başarı görselini göster
                    messagebox.showinfo("Başarılı", f"Dosya başarıyla çözüldü: {decrypted_file_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

        self.image_frame.drop_target_register(DND_FILES)
        self.image_frame.dnd_bind('<<Drop>>', on_drop)

        back_btn = ctk.CTkButton(self.image_frame, text="Geri Dön", command=self.setup_main_frame)
        back_btn.pack(pady=20)

    #Build'den sonra çalışmadığı için devre dışı bıraktık -Yusuf
    """ def show_tick_image(self):
        for widget in self.image_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and hasattr(widget, "is_tick_image"):
                widget.destroy()
        try:
            tick_image = PhotoImage(file="ticklogo.png")
            tick_image = tick_image.subsample(20,20)
            tick_label = ctk.CTkLabel(self.image_frame, image=tick_image, text="")
            tick_label.image = tick_image  # Referansı tutmak için
            tick_label.is_tick_image = True  # Diğer widget'larla karışmasını önlemek için işaret ekle
            tick_label.pack(pady=10)  # Drag-and-drop alanının altında göstermek için
        except Exception as e:
            messagebox.showerror("Hata", f"Görsel yüklenemedi: {str(e)}")
    """

    #Toplu Dosya İşlemen için
    def batch_process_files(self, files, operation):
        if not self.key:
            messagebox.showerror("Hata", "Lütfen önce bir anahtar oluşturun veya içe aktarın.")
            return

        progress_window = ctk.CTkToplevel(self.master)  # İlerleme durumu penceresi
        progress_window.title("İşlem Durumu")
        progress_label = ctk.CTkLabel(progress_window, text="Dosyalar işleniyor...")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", mode="determinate", length=300)
        progress_bar.pack(pady=10)

        def process():
            try:
                progress_bar["maximum"] = len(files)
                for i, file_path in enumerate(files):
                    if operation == "encrypt":
                        AESHandler.encrypt_file(self.key, file_path)
                    elif operation == "decrypt":
                        if not file_path.endswith(".enc"):
                            messagebox.showerror("Hata", ".enc uzantılı bir dosya seçmelisiniz.")
                            continue
                        AESHandler.decrypt_file(self.key, file_path)
                    progress_bar["value"] = i + 1  # İlerleme çubuğunu güncelleme
                    progress_window.update_idletasks()  # Arayüzü yenile komutu

                delete_originals = messagebox.askyesno(
                    "Dosyaları Sil",
                    "Dosyalar başarıyla işlendi. Orijinal dosyaları silmek ister misiniz?"
                )
                if delete_originals:
                    for file_path in files:
                        try:
                            os.remove(file_path)  # Dosyayı sil
                        except Exception as e:
                            messagebox.showerror("Hata", f"Dosya silinirken bir hata oluştu: {str(e)}")
                    messagebox.showinfo("Bilgi", "Orijinal dosyalar başarıyla silindi.")
                else:
                    messagebox.showinfo("Bilgi", "Orijinal dosyalar korunmuştur.")

                progress_label.configure(text="İşlem tamamlandı!")
                messagebox.showinfo("Başarılı", "Tüm dosyalar başarıyla işlendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu: {str(e)}")
                progress_bar["value"] = len(files)  # İlerleme çubuğunu tamam olarak ayarla hata durumu için
            finally:
                progress_window.destroy()

        threading.Thread(target=process).start()

    def open_batch_processing(self):
        files = filedialog.askopenfilenames(title="Dosyaları Seçin", filetypes=[("Tüm Dosyalar (*.*)", "*.*"), ("Şifreli Dosyalar (*.enc)", "*.enc")])
        if not files:
            return

        operation = self.action_var.get().lower()  #normalize
        if operation not in ["encrypt", "decrypt"]:
            messagebox.showerror("Hata", "Geçersiz işlem seçimi.")
            return

        self.batch_process_files(files, operation)