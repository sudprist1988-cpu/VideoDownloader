import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import yt_dlp
import os

class VideoDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Видео Загрузчик")
        self.window.geometry("700x600")
        self.window.configure(bg='#f0f0f0')
        
        tk.Label(self.window, text="🎬 Видео Загрузчик", font=("Arial", 14, "bold"), 
                bg='#f0f0f0').pack(pady=15)
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Вкладка скачивания
        download_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(download_frame, text="📥 Скачать")
        
        tk.Label(download_frame, text="Ссылка на видео:", bg='#f0f0f0', font=("Arial", 10)).pack(pady=5)
        self.url_entry = tk.Entry(download_frame, width=60, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(download_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        self.analyze_btn = tk.Button(btn_frame, text="🔍 Анализировать", 
                                     command=self.analyze, bg="#2196F3", fg="white",
                                     font=("Arial", 10), padx=15, pady=5)
        self.analyze_btn.pack(side='left', padx=5)
        
        self.download_btn = tk.Button(btn_frame, text="📥 Скачать", 
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 10), padx=15, pady=5, state='disabled')
        self.download_btn.pack(side='left', padx=5)
        
        # Список доступных форматов
        tk.Label(download_frame, text="Доступные форматы:", bg='#f0f0f0', font=("Arial", 10, "bold")).pack(pady=5)
        
        list_frame = tk.Frame(download_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.format_listbox = tk.Listbox(list_frame, height=8, font=("Courier", 10),
                                         yscrollcommand=scrollbar.set, selectmode='single')
        self.format_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.format_listbox.yview)
        
        # Прогресс
        self.progress = ttk.Progressbar(download_frame, length=400, mode='indeterminate')
        self.progress.pack(pady=10)
        
        self.status = tk.Label(download_frame, text="Готов к работе", bg='#f0f0f0', fg="gray")
        self.status.pack(pady=5)
        
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
        tk.Button(cookies_frame, text="📁 Выбрать", command=self.select_cookies,
                 bg="#607D8B", fg="white", font=("Arial", 9), padx=10).pack(side='left')
        
        tk.Button(auth_frame, text="🔑 Использовать cookies файл", 
                 command=self.use_cookies_file, bg="#FF9800", fg="white",
                 font=("Arial", 10), padx=15, pady=8).pack(pady=10)
        
        self.auth_status = tk.Label(auth_frame, text="Статус: не настроена", 
                                     bg='#f0f0f0', fg='red', font=("Arial", 10))
        self.auth_status.pack(pady=10)
        
        self.folder = os.path.join(os.path.expanduser("~"), "Downloads", "Видео")
        os.makedirs(self.folder, exist_ok=True)
        self.cookies_config = None
        self.available_formats = []
    
    def select_cookies(self):
        filename = filedialog.askopenfilename(
            title="Выберите cookies.txt",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            self.cookies_path.set(filename)
    
    def use_browser_cookies(self):
        browser = self.browser_var.get()
        self.cookies_config = ('browser', browser)
        self.auth_status.config(
            text=f"✅ Выбран браузер: {browser}\n⚠️ Закройте браузер перед скачиванием!", 
            fg='green'
        )
        messagebox.showinfo("Настроено", f"Браузер: {browser}\n\n⚠️ Закройте браузер перед скачиванием!")
    
    def use_cookies_file(self):
        path = self.cookies_path.get()
        if path == "Не выбран" or not os.path.exists(path):
            messagebox.showerror("Ошибка", "Выберите файл cookies.txt")
            return
        self.cookies_config = ('file', path)
        self.auth_status.config(text="✅ Cookies файл загружен", fg='green')
        messagebox.showinfo("Готово", "Cookies из файла будут использоваться")
    
    def format_size(self, size):
        if not size or size == 'N/A':
            return 'N/A'
        try:
            size = float(size)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return 'N/A'
    
    def analyze(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Ошибка", "Вставьте ссылку")
            return
        
        self.analyze_btn.config(state='disabled', text="Анализ...")
        self.progress.start()
        self.status.config(text="Получаю информацию о форматах...")
        self.format_listbox.delete(0, tk.END)
        
        def do_analyze():
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                self._add_cookies(ydl_opts)
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    self.available_formats = []
                    seen = set()
                    
                    # Собираем доступные форматы
                    for f in info['formats']:
                        fmt_id = f.get('format_id', '')
                        ext = f.get('ext', '')
                        height = f.get('height', 0)
                        filesize = f.get('filesize') or f.get('filesize_approx', 'N/A')
                        note = f.get('format_note', '')
                        
                        # Создаём ключ для уникальности
                        key = f"{height}_{ext}"
                        
                        if height and key not in seen and ext in ['mp4', 'webm']:
                            seen.add(key)
                            self.available_formats.append({
                                'id': fmt_id,
                                'height': height,
                                'ext': ext,
                                'size': filesize,
                                'note': note,
                                'description': f.get('resolution', f'{height}p')
                            })
                    
                    # Сортируем по качеству
                    self.available_formats.sort(key=lambda x: x['height'], reverse=True)
                    
                    self.window.after(0, self.analyze_done, info)
            except Exception as e:
                self.window.after(0, self.error, str(e))
        
        threading.Thread(target=do_analyze, daemon=True).start()
    
    def analyze_done(self, info):
        self.progress.stop()
        self.analyze_btn.config(state='normal', text="🔍 Анализировать")
        self.download_btn.config(state='normal')
        
        self.format_listbox.delete(0, tk.END)
        
        # Добавляем "Лучшее качество"
        self.format_listbox.insert(tk.END, "⭐ ЛУЧШЕЕ ДОСТУПНОЕ КАЧЕСТВО (рекомендуется)")
        self.format_listbox.insert(tk.END, "")
        
        for fmt in self.available_formats:
            size = self.format_size(fmt['size'])
            display = f"  {fmt['height']}p  |  {fmt['ext']:5}  |  ~{size}"
            self.format_listbox.insert(tk.END, display)
        
        self.format_listbox.selection_set(0)
        
        title = info.get('title', 'Без названия')
        dur = info.get('duration', 0)
        dur_str = f"{dur//60}:{dur%60:02d}" if dur else "?"
        self.status.config(text=f"📹 {title[:50]}... | ⏱ {dur_str}")
    
    def download(self):
        url = self.url_entry.get().strip()
        
        if not url:
            return
        
        # Определяем выбранный формат
        selection = self.format_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите формат из списка")
            return
        
        idx = selection[0]
        
        if idx == 0:  # Лучшее качество
            fmt = "bestvideo+bestaudio/best"
        elif idx == 1:  # Пустая строка
            fmt = "bestvideo+bestaudio/best"
        else:
            fmt_idx = idx - 2  # Пропускаем первые две строки
            if fmt_idx < len(self.available_formats):
                fmt = self.available_formats[fmt_idx]['id']
            else:
                fmt = "bestvideo+bestaudio/best"
        
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
        if self.cookies_config:
            config_type, value = self.cookies_config
            if config_type == 'browser':
                ydl_opts['cookiesfrombrowser'] = (value,)
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
        messagebox.showerror("Ошибка", msg)

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.window.mainloop()
