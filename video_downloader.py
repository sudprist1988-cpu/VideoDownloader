import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import yt_dlp
import os

class VideoDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Видео Загрузчик")
        self.window.geometry("650x550")
        self.window.configure(bg='#f0f0f0')
        
        # Заголовок
        tk.Label(self.window, text="🎬 Видео Загрузчик", font=("Arial", 14, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        # Вкладки
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Вкладка скачивания
        download_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(download_frame, text="📥 Скачать")
        
        # URL
        tk.Label(download_frame, text="Ссылка на видео:", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        self.url_entry = tk.Entry(download_frame, width=55, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Качество
        tk.Label(download_frame, text="Качество:", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        self.quality_var = tk.StringVar(value="Лучшее")
        qualities = ["Лучшее", "1080p", "720p", "480p", "360p"]
        self.quality_menu = ttk.Combobox(download_frame, textvariable=self.quality_var, 
                                         values=qualities, state='readonly', width=20)
        self.quality_menu.pack(pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(download_frame, bg='#f0f0f0')
        btn_frame.pack(pady=15)
        
        self.analyze_btn = tk.Button(btn_frame, text="🔍 Анализировать", 
                                     command=self.analyze, bg="#2196F3", fg="white",
                                     font=("Arial", 10), padx=15, pady=5)
        self.analyze_btn.pack(side='left', padx=5)
        
        self.download_btn = tk.Button(btn_frame, text="📥 Скачать", 
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 10), padx=15, pady=5, state='disabled')
        self.download_btn.pack(side='left', padx=5)
        
        # Прогресс
        self.progress = ttk.Progressbar(download_frame, length=400, mode='indeterminate')
        self.progress.pack(pady=15)
        
        self.status = tk.Label(download_frame, text="Готов к работе", bg='#f0f0f0', fg="gray")
        self.status.pack(pady=10)
        
        # Вкладка авторизации
        auth_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(auth_frame, text="🔑 Авторизация YouTube")
        
        tk.Label(auth_frame, text="Авторизация YouTube", font=("Arial", 12, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        tk.Label(auth_frame, text="Выберите браузер (должен быть ЗАКРЫТ при скачивании):", 
                bg='#f0f0f0', font=("Arial", 10)).pack(pady=10)
        
        self.browser_var = tk.StringVar(value="opera")
        
        browsers = [
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Edge", "edge"),
            ("Opera", "opera"),
            ("Opera GX", "operagx"),
            ("Brave", "brave"),
            ("Vivaldi", "vivaldi"),
        ]
        
        for text, value in browsers:
            tk.Radiobutton(auth_frame, text=text, variable=self.browser_var, 
                          value=value, bg='#f0f0f0', font=("Arial", 10)).pack(anchor='w', padx=50)
        
        tk.Button(auth_frame, text="🔑 Использовать cookies браузера", 
                 command=self.use_browser_cookies, bg="#4CAF50", fg="white",
                 font=("Arial", 10, "bold"), padx=15, pady=10).pack(pady=15)
        
        tk.Label(auth_frame, text="────────── ИЛИ ──────────", 
                bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        
        tk.Label(auth_frame, text="Загрузите файл cookies.txt:", 
                bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        
        cookies_frame = tk.Frame(auth_frame, bg='#f0f0f0')
        cookies_frame.pack(pady=5)
        
        self.cookies_path = tk.StringVar(value="Не выбран")
        
        tk.Label(cookies_frame, textvariable=self.cookies_path, 
                bg='#f0f0f0', fg='blue', font=("Arial", 9)).pack(side='left', padx=5)
        tk.Button(cookies_frame, text="📁 Выбрать файл", command=self.select_cookies,
                 bg="#607D8B", fg="white", font=("Arial", 9), padx=10).pack(side='left')
        
        self.auth_status = tk.Label(auth_frame, text="Статус: не настроена", 
                                     bg='#f0f0f0', fg='red', font=("Arial", 10))
        self.auth_status.pack(pady=15)
        
        # Настройки
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads", "Видео")
        os.makedirs(self.folder, exist_ok=True)
        self.cookies_config = None  # ('browser', 'opera') или ('file', 'path')
        
        # Авто-выбор Opera при запуске
        self.window.after(500, self.auto_detect_browser)
    
    def auto_detect_browser(self):
        """Автоматически пробуем Opera"""
        self.auth_status.config(text="🔄 Пробую Opera...", fg='orange')
    
    def select_cookies(self):
        filename = filedialog.askopenfilename(
            title="Выберите файл cookies.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.cookies_path.set(filename)
    
    def use_browser_cookies(self):
        browser = self.browser_var.get()
        self.cookies_config = ('browser', browser)
        self.auth_status.config(
            text=f"✅ Будет использован {browser}\n⚠️ Закройте браузер перед скачиванием!", 
            fg='green'
        )
        messagebox.showinfo("Настроено", 
            f"Выбран браузер: {browser}\n\n"
            "⚠️ ВАЖНО: Закройте браузер перед скачиванием!\n"
            "Иначе возникнет ошибка доступа к cookies.")
    
    def select_cookies_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите cookies.txt",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            self.cookies_config = ('file', filename)
            self.auth_status.config(text=f"✅ Cookies файл загружен", fg='green')
    
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
                self._add_cookies(ydl_opts)
                
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
        self.status.config(text="Скачиваю...")
        
        def do_download():
            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'format': fmt,
                'merge_output_format': 'mp4',
                'quiet': True,
            }
            self._add_cookies(ydl_opts)
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    self.window.after(0, self.done, info.get('title', 'видео'))
            except Exception as e:
                self.window.after(0, self.error, str(e))
        
        threading.Thread(target=do_download, daemon=True).start()
    
    def _add_cookies(self, ydl_opts):
        """Добавляет cookies в настройки"""
        if self.cookies_config:
            config_type, value = self.cookies_config
            if config_type == 'browser':
                ydl_opts['cookiesfrombrowser'] = (value, None, None, None, None)
            elif config_type == 'file':
                ydl_opts['cookiefile'] = value
    
    def done(self, title):
        self.progress.stop()
        self.download_btn.config(state='normal', text="📥 Скачать")
        self.status.config(text=f"✅ Сохранено: {title}")
        messagebox.showinfo("Готово", f"Видео сохранено!\n📁 {self.folder}")
    
    def error(self, msg):
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🔍 Анализировать")
        self.download_btn.config(state='normal', text="📥 Скачать")
        self.status.config(text=f"❌ Ошибка")
        
        # Если ошибка cookies - даём подсказку
        if "cookie" in msg.lower() or "chrome" in msg.lower():
            msg += "\n\n💡 ЗАКРОЙТЕ БРАУЗЕР перед скачиванием!"
        
        messagebox.showerror("Ошибка", msg)

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.window.mainloop()
