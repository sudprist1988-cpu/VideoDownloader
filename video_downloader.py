import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os

class VideoDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Видео Загрузчик")
        self.window.geometry("600x450")
        self.window.configure(bg='#f0f0f0')
        
        # Заголовок
        tk.Label(self.window, text="🎬 Видео Загрузчик", font=("Arial", 14, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        # URL
        frame = tk.Frame(self.window, bg='#f0f0f0')
        frame.pack(pady=10)
        tk.Label(frame, text="Ссылка на видео:", bg='#f0f0f0').pack()
        self.url_entry = tk.Entry(frame, width=50, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(self.window, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        self.analyze_btn = tk.Button(btn_frame, text="🔍 Анализировать", 
                                     command=self.analyze, bg="#2196F3", fg="white",
                                     font=("Arial", 10), padx=15, pady=5)
        self.analyze_btn.pack(side='left', padx=5)
        
        self.download_btn = tk.Button(btn_frame, text="📥 Скачать", 
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 10), padx=15, pady=5, state='disabled')
        self.download_btn.pack(side='left', padx=5)
        
        # Качество
        tk.Label(self.window, text="Качество:", bg='#f0f0f0').pack()
        self.quality_var = tk.StringVar(value="best")
        qualities = ["Лучшее", "1080p", "720p", "480p", "360p"]
        self.quality_menu = ttk.Combobox(self.window, textvariable=self.quality_var, 
                                         values=qualities, state='readonly', width=20)
        self.quality_menu.pack(pady=5)
        
        # Прогресс
        self.progress = ttk.Progressbar(self.window, length=400, mode='indeterminate')
        self.progress.pack(pady=15)
        
        # Статус
        self.status = tk.Label(self.window, text="Готов к работе", bg='#f0f0f0', fg="gray")
        self.status.pack(pady=10)
        
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads", "Видео")
        os.makedirs(self.folder, exist_ok=True)
    
    def analyze(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Ошибка", "Вставьте ссылку")
            return
        
        self.analyze_btn.config(state='disabled', text="Анализ...")
        self.progress.start()
        self.status.config(text="Получаю информацию...")
        
        def do_analyze():
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Без названия')
                    dur = info.get('duration', 0)
                    self.window.after(0, self.analyze_done, title, dur)
            except Exception as e:
                self.window.after(0, self.error, str(e))
        
        threading.Thread(target=do_analyze, daemon=True).start()
    
    def analyze_done(self, title, dur):
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🔍 Анализировать")
        self.download_btn.config(state='normal')
        dur_str = f"{dur//60}:{dur%60:02d}" if dur else "?"
        self.status.config(text=f"📹 {title[:60]}... | ⏱ {dur_str}")
    
    def download(self):
        url = self.url_entry.get().strip()
        quality = self.quality_var.get()
        
        if quality == "Лучшее":
            fmt = "best"
        else:
            h = quality.replace('p', '')
            fmt = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
        
        self.download_btn.config(state='disabled', text="Загрузка...")
        self.progress.start()
        
        def do_download():
            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'format': fmt,
                'merge_output_format': 'mp4',
                'quiet': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    self.window.after(0, self.done, info.get('title', 'видео'))
            except Exception as e:
                self.window.after(0, self.error, str(e))
        
        threading.Thread(target=do_download, daemon=True).start()
    
    def done(self, title):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 Скачать")
        self.status.config(text=f"✅ Сохранено: {title}")
        messagebox.showinfo("Готово", f"Видео сохранено!\n📁 {self.folder}")
    
    def error(self, msg):
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🔍 Анализировать")
        self.download_btn.config(state='normal', text="📥 Скачать")
        self.status.config(text=f"❌ Ошибка: {msg[:80]}")
        messagebox.showerror("Ошибка", msg)

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.window.mainloop()
