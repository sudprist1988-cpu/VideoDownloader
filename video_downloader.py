import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os

class VideoDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Видео Загрузчик")
        self.window.geometry("600x500")
        self.window.configure(bg='#f0f0f0')
        
        # Заголовок
        tk.Label(self.window, text="🎬 Видео Загрузчик", font=("Arial", 14, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        # Фрейм для URL
        url_frame = tk.LabelFrame(self.window, text="🔗 Ссылка", bg='#f0f0f0', font=("Arial", 10, "bold"))
        url_frame.pack(fill='x', padx=15, pady=10)
        
        self.url_entry = tk.Entry(url_frame, font=("Arial", 10))
        self.url_entry.pack(fill='x', padx=10, pady=10)
        
        # Фрейм для настроек
        settings_frame = tk.Frame(self.window, bg='#f0f0f0')
        settings_frame.pack(fill='x', padx=15, pady=5)
        
        # Выбор браузера (слева)
        browser_frame = tk.LabelFrame(settings_frame, text="🔑 Браузер для авторизации", 
                                      bg='#f0f0f0', font=("Arial", 9, "bold"))
        browser_frame.pack(side='left', fill='both', expand=True, padx=(0,5))
        
        self.browser_var = tk.StringVar(value="none")
        
        browsers = [
            ("Без авторизации", "none"),
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Opera", "opera"),
            ("Edge", "edge"),
            ("Brave", "brave"),
        ]
        
        for text, value in browsers:
            tk.Radiobutton(browser_frame, text=text, variable=self.browser_var, 
                          value=value, bg='#f0f0f0', font=("Arial", 9),
                          anchor='w').pack(fill='x', padx=5, pady=1)
        
        # Выбор качества (справа)
        quality_frame = tk.LabelFrame(settings_frame, text="📊 Качество", 
                                      bg='#f0f0f0', font=("Arial", 9, "bold"))
        quality_frame.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        self.quality_var = tk.StringVar(value="best")
        
        qualities = [
            ("Лучшее доступное", "best"),
            ("4K (2160p)", "best[height<=2160]"),
            ("2K (1440p)", "best[height<=1440]"),
            ("Full HD (1080p)", "best[height<=1080]"),
            ("HD (720p)", "best[height<=720]"),
            ("480p", "best[height<=480]"),
            ("360p", "best[height<=360]"),
        ]
        
        for text, value in qualities:
            tk.Radiobutton(quality_frame, text=text, variable=self.quality_var, 
                          value=value, bg='#f0f0f0', font=("Arial", 9),
                          anchor='w').pack(fill='x', padx=5, pady=1)
        
        # Кнопка скачивания
        self.download_btn = tk.Button(self.window, text="📥 СКАЧАТЬ ВИДЕО", 
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 12, "bold"), padx=20, pady=12,
                                      cursor="hand2")
        self.download_btn.pack(pady=15)
        
        # Прогресс
        self.progress = ttk.Progressbar(self.window, length=500, mode='indeterminate')
        self.progress.pack(pady=5)
        
        # Статус
        self.status = tk.Label(self.window, text="Готов к работе", bg='#f0f0f0', fg="gray", font=("Arial", 9))
        self.status.pack(pady=5)
        
        # Папка сохранения
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads", "Видео")
        os.makedirs(self.folder, exist_ok=True)
        
        folder_label = tk.Label(self.window, text=f"📁 {self.folder}", 
                               bg='#f0f0f0', fg='blue', font=("Arial", 8))
        folder_label.pack(pady=5)
    
    def download(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("⚠️ Внимание", "Вставьте ссылку на видео")
            return
        
        quality = self.quality_var.get()
        browser = self.browser_var.get()
        
        self.download_btn.config(state='disabled', text="⏳ Загрузка...")
        self.progress.start()
        self.status.config(text="📥 Скачиваю видео...")
        
        def do_download():
            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'format': quality,
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
            }
            
            # Добавляем cookies если выбран браузер
            if browser != "none":
                ydl_opts['cookiesfrombrowser'] = (browser,)
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'видео')
                    self.window.after(0, self.done, title)
            except Exception as e:
                error_msg = str(e)
                # Подсказки при ошибках
                if "cookie" in error_msg.lower():
                    error_msg = "❌ Закройте браузер перед скачиванием!\n\n" + error_msg
                elif "requested format" in error_msg.lower():
                    error_msg = "❌ Формат недоступен. Выберите 'Лучшее доступное'\n\n" + error_msg
                elif "sign in" in error_msg.lower():
                    error_msg = "❌ YouTube требует авторизацию. Выберите браузер\n\n" + error_msg
                
                self.window.after(0, self.error, error_msg)
        
        threading.Thread(target=do_download, daemon=True).start()
    
    def done(self, title):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 СКАЧАТЬ ВИДЕО")
        self.status.config(text=f"✅ Сохранено: {title}")
        messagebox.showinfo("✅ Готово!", f"Видео сохранено!\n\n📹 {title}\n📁 {self.folder}")
    
    def error(self, msg):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 СКАЧАТЬ ВИДЕО")
        self.status.config(text="❌ Ошибка загрузки")
        messagebox.showerror("❌ Ошибка", msg)

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.window.mainloop()
