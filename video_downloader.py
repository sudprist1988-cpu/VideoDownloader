import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os

class VideoDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Видео Загрузчик")
        self.window.geometry("550x450")
        self.window.configure(bg='#f0f0f0')
        
        tk.Label(self.window, text="🎬 Видео Загрузчик", font=("Arial", 14, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        # URL
        tk.Label(self.window, text="Ссылка на видео:", bg='#f0f0f0').pack(pady=5)
        self.url_entry = tk.Entry(self.window, width=55, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Браузер
        browser_frame = tk.LabelFrame(self.window, text="🔑 Авторизация", bg='#f0f0f0')
        browser_frame.pack(pady=10, padx=20, fill='x')
        
        self.browser_var = tk.StringVar(value="none")
        
        browsers = [
            ("Без авторизации", "none"),
            ("Opera", "opera"),
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Edge", "edge"),
        ]
        
        for text, value in browsers:
            tk.Radiobutton(browser_frame, text=text, variable=self.browser_var, 
                          value=value, bg='#f0f0f0').pack(side='left', padx=10, pady=5)
        
        # Качество
        quality_frame = tk.LabelFrame(self.window, text="📊 Качество", bg='#f0f0f0')
        quality_frame.pack(pady=10, padx=20, fill='x')
        
        self.quality_var = tk.StringVar(value="best")
        
        qualities = [
            ("Лучшее", "best"),
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480"),
            ("360p", "360"),
        ]
        
        for text, value in qualities:
            tk.Radiobutton(quality_frame, text=text, variable=self.quality_var, 
                          value=value, bg='#f0f0f0').pack(side='left', padx=10, pady=5)
        
        # Кнопка
        self.download_btn = tk.Button(self.window, text="📥 СКАЧАТЬ", 
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 12, "bold"), padx=20, pady=10)
        self.download_btn.pack(pady=15)
        
        # Прогресс
        self.progress = ttk.Progressbar(self.window, length=400, mode='indeterminate')
        self.progress.pack(pady=5)
        
        self.status = tk.Label(self.window, text="Готов", bg='#f0f0f0', fg="gray")
        self.status.pack(pady=5)
        
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads", "Видео")
        os.makedirs(self.folder, exist_ok=True)
    
    def download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Ошибка", "Вставьте ссылку")
            return
        
        quality = self.quality_var.get()
        browser = self.browser_var.get()
        
        # ФОРМАТЫ КОТОРЫЕ ТОЧНО РАБОТАЮТ
        if quality == "best":
            format_str = "bestvideo+bestaudio/best"
        else:
            format_str = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best[height<={quality}]/best"
        
        self.download_btn.config(state='disabled', text="Загрузка...")
        self.progress.start()
        self.status.config(text="Скачиваю...")
        
        def do_download():
            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'format': format_str,
                'merge_output_format': 'mp4',
                'quiet': True,
                'ignoreerrors': True,
            }
            
            if browser != "none":
                ydl_opts['cookiesfrombrowser'] = (browser,)
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    self.window.after(0, self.done, info.get('title', 'видео'))
            except Exception as e:
                self.window.after(0, self.error, str(e))
        
        threading.Thread(target=do_download, daemon=True).start()
    
    def done(self, title):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 СКАЧАТЬ")
        self.status.config(text=f"✅ {title}")
        messagebox.showinfo("Готово", f"Сохранено в:\n{self.folder}")
    
    def error(self, msg):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 СКАЧАТЬ")
        self.status.config(text="❌ Ошибка")
        
        # Понятная ошибка
        if "cookie" in msg.lower():
            msg = "ЗАКРОЙТЕ БРАУЗЕР перед скачиванием!\n\n" + msg
        elif "format" in msg.lower():
            msg = "Выберите 'Лучшее' качество\n\n" + msg
        
        messagebox.showerror("Ошибка", msg)

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.window.mainloop()
