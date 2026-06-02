import tkinter as tk
from tkinter import scrolledtext

# --- OTOMATA TEORİSİ: ALT SİSTEM SINIFI ---
class AltSistemDFA:
    def __init__(self, isim):
        self.isim = isim
        self.q0 = f"q0_{isim}_Bekleme"
        self.q1 = f"q1_{isim}_Acik_Kabul"
        self.q2 = f"q2_{isim}_Hata_Ret"
        
        self.current_state = self.q0
        
        self.transition_table = {
            # 1. Normal İşlem Geçişleri
            (self.q0, "onay"): self.q1,
            (self.q0, "ret"): self.q2,
            (self.q1, "kapat"): self.q0,
            (self.q2, "sifirla"): self.q0, 
            
            # 2. ÖZ-DÖNGÜ KORUMALARI (Kapı açıkken veya hatadayken gelen yeni girdileri engelleme)
            (self.q1, "onay"): self.q1,
            (self.q1, "ret"): self.q1,
            (self.q2, "onay"): self.q2,
            (self.q2, "ret"): self.q2,
            
            # 3. Global Reset
            (self.q0, "reset"): self.q0,
            (self.q1, "reset"): self.q0,
            (self.q2, "reset"): self.q0
        }

    def process_input(self, user_input):
        key = (self.current_state, user_input)
        if key in self.transition_table:
            previous_state = self.current_state
            self.current_state = self.transition_table[key]
            return True, previous_state, self.current_state
        return False, None, None

    def get_status_info(self):
        if self.current_state == self.q1:
            return "SONUÇ: KABUL (Açık)", "green"
        elif self.current_state == self.q2:
            return "SONUÇ: HATA (İhlal)", "red"
        else:
            return "SONUÇ: BEKLEMEDE (Hazır)", "blue"

# --- ARAYÜZ SINIFI ---
class SmartCampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Kampüs ")
        self.root.geometry("900x650")
        
        self.yaya_dfa = AltSistemDFA("Yaya")
        self.arac_dfa = AltSistemDFA("Arac")
        
        self.yaya_timer = None
        self.arac_timer = None

        tk.Label(root, text="Yaya ve Araç Paralel Geçiş", font=("Arial", 16, "bold")).pack(pady=10)

        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10)
        main_frame.columnconfigure(0, weight=1, uniform="esit_kolon")
        main_frame.columnconfigure(1, weight=1, uniform="esit_kolon")

        # ================= SOL PANEL (YAYA) =================
        left_frame = tk.LabelFrame(main_frame, text="🚶 YAYA TURNİKESİ (Kartlı)", font=("Arial", 12, "bold"), padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5) 

        self.lbl_yaya_durum = tk.Label(left_frame, text=f"Durum: {self.yaya_dfa.current_state}", font=("Arial", 11, "bold"), bg="#e0e0e0", pady=5)
        self.lbl_yaya_durum.pack(fill="x", pady=5)
        
        self.lbl_yaya_sonuc = tk.Label(left_frame, text="SONUÇ: BEKLEMEDE (Hazır)", font=("Arial", 11, "bold"), fg="blue")
        self.lbl_yaya_sonuc.pack(pady=5)

        tk.Button(left_frame, text="Öğrenci Kartı (Onay)", bg="#d9ead3", height=2, command=lambda: self.handle_input(self.yaya_dfa, "onay", "Yaya")).pack(fill="x", pady=3)
        tk.Button(left_frame, text="Geçersiz Kart (Ret)", bg="#f4cccc", height=2, command=lambda: self.handle_input(self.yaya_dfa, "ret", "Yaya")).pack(fill="x", pady=3)
        tk.Button(left_frame, text="Turnikeyi Kapat", bg="#fff2cc", height=2, command=lambda: self.handle_input(self.yaya_dfa, "kapat", "Yaya")).pack(fill="x", pady=3)

        tk.Label(left_frame, text="Yaya Logları:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,0))
        self.log_yaya = scrolledtext.ScrolledText(left_frame, height=10, font=("Consolas", 9), state='disabled')
        self.log_yaya.pack(fill="x")

        # ================= SAĞ PANEL (ARAÇ) =================
        right_frame = tk.LabelFrame(main_frame, text="🚗 ARAÇ BARİYERİ (Plaka)", font=("Arial", 12, "bold"), padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        self.lbl_arac_durum = tk.Label(right_frame, text=f"Durum: {self.arac_dfa.current_state}", font=("Arial", 11, "bold"), bg="#e0e0e0", pady=5)
        self.lbl_arac_durum.pack(fill="x", pady=5)

        self.lbl_arac_sonuc = tk.Label(right_frame, text="SONUÇ: BEKLEMEDE (Hazır)", font=("Arial", 11, "bold"), fg="blue")
        self.lbl_arac_sonuc.pack(pady=5)

        tk.Button(right_frame, text="Plaka Tanındı (Onay)", bg="#d9ead3", height=2, command=lambda: self.handle_input(self.arac_dfa, "onay", "Araç")).pack(fill="x", pady=3)
        tk.Button(right_frame, text="Plaka Bulunamadı (Ret)", bg="#f4cccc", height=2, command=lambda: self.handle_input(self.arac_dfa, "ret", "Araç")).pack(fill="x", pady=3)
        tk.Button(right_frame, text="Bariyeri Kapat", bg="#fff2cc", height=2, command=lambda: self.handle_input(self.arac_dfa, "kapat", "Araç")).pack(fill="x", pady=3)

        tk.Label(right_frame, text="Araç Logları:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,0))
        self.log_arac = scrolledtext.ScrolledText(right_frame, height=10, font=("Consolas", 9), state='disabled')
        self.log_arac.pack(fill="x")

        # ================= ALT PANEL (ORTAK) =================
        tk.Button(root, text="🔄 TÜM SİSTEMLERİ RESETLE", bg="#eaddf6", font=("Arial", 11, "bold"), height=2, command=self.reset_all).pack(fill="x", padx=15, pady=10)

    def handle_input(self, dfa_instance, user_input, sistem_turu):
        success, prev_state, new_state = dfa_instance.process_input(user_input)
        log_area = self.log_yaya if sistem_turu == "Yaya" else self.log_arac

        if success:
            # EĞER ÖZ-DÖNGÜ YAPILDIYSA (Kapı açıkken tekrar basıldıysa)
            if prev_state == new_state and user_input in ["onay", "ret"]:
                self.write_log(log_area, "⚠️ İŞLEM REDDEDİLDİ: Lütfen kapının/bariyerin kapanmasını bekleyin!")
                return # Sistemi yoksay ve alttaki zamanlayıcıları tekrar başlatma

            self.write_log(log_area, f"GEÇİŞ: {prev_state} -({user_input})-> {new_state}")
            self.update_ui()

            # Yeni bir geçiş yapıldıysa eski zamanlayıcıları iptal et
            if sistem_turu == "Yaya" and self.yaya_timer:
                self.root.after_cancel(self.yaya_timer)
                self.yaya_timer = None
            elif sistem_turu == "Araç" and self.arac_timer:
                self.root.after_cancel(self.arac_timer)
                self.arac_timer = None

            # BAŞARILI GEÇİŞ: Otomatik kapanma
            if new_state == dfa_instance.q1:
                if sistem_turu == "Yaya":
                    self.write_log(log_area, "⏱️ 2 sn sonra otomatik kapanacak...")
                    self.yaya_timer = self.root.after(2000, lambda: self.auto_trigger(dfa_instance, "kapat", "Yaya"))
                else:
                    self.write_log(log_area, "⏱️ 4 sn sonra otomatik kapanacak...")
                    self.arac_timer = self.root.after(4000, lambda: self.auto_trigger(dfa_instance, "kapat", "Araç"))
            
            # HATA DURUMU: Otomatik sıfırlama
            elif new_state == dfa_instance.q2:
                if sistem_turu == "Yaya":
                    self.yaya_timer = self.root.after(0, lambda: self.auto_trigger(dfa_instance, "sifirla", "Yaya"))
                else:
                    self.arac_timer = self.root.after(0, lambda: self.auto_trigger(dfa_instance, "sifirla", "Araç"))
        else:
            self.write_log(log_area, f"❌ HATA: '{dfa_instance.current_state}' durumunda '{user_input}' işlemi tanımsız!")

    def auto_trigger(self, dfa_instance, islem, sistem_turu):
        log_area = self.log_yaya if sistem_turu == "Yaya" else self.log_arac
        
        if islem == "kapat":
            self.write_log(log_area, "🔒 Süre doldu, kapı otomatik kapatıldı.")
        elif islem == "sifirla":
            self.write_log(log_area, "🟢 Hata temizlendi, sistem yeni girişe hazır.")
            
        self.handle_input(dfa_instance, islem, sistem_turu)

    def reset_all(self):
        self.handle_input(self.yaya_dfa, "reset", "Yaya")
        self.handle_input(self.arac_dfa, "reset", "Araç")
        self.write_log(self.log_yaya, "🔄 Sistem manuel olarak sıfırlandı.")
        self.write_log(self.log_arac, "🔄 Sistem manuel olarak sıfırlandı.")

    def update_ui(self):
        self.lbl_yaya_durum.config(text=f"Durum: {self.yaya_dfa.current_state}")
        status_y, color_y = self.yaya_dfa.get_status_info()
        self.lbl_yaya_sonuc.config(text=status_y, fg=color_y)

        self.lbl_arac_durum.config(text=f"Durum: {self.arac_dfa.current_state}")
        status_a, color_a = self.arac_dfa.get_status_info()
        self.lbl_arac_sonuc.config(text=status_a, fg=color_a)

    def write_log(self, text_widget, message):
        text_widget.config(state='normal')
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)
        text_widget.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCampusApp(root)
    root.mainloop()