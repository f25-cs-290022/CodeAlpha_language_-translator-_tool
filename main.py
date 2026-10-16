import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.parse
import json
import html


def translate_text():
    text = input_box.get("1.0", tk.END).strip()

    source = source_language.get()
    target = target_language.get()

    if not text:
        messagebox.showwarning(
            "Missing Text",
            "Please enter text to translate."
        )
        return

    if source == target:
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, text)
        output_box.config(state="disabled")
        return

    translate_button.config(state="disabled", text="Translating...")
    root.update_idletasks()

    try:
        params = urllib.parse.urlencode({
            "q": text,
            "langpair": f"{languages[source]}|{languages[target]}"
        })

        url = "https://api.mymemory.translated.net/get?" + params

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "LanguageTranslationTool/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("responseStatus") != 200:
            raise ValueError("The translation service returned an error.")

        translated = html.unescape(
            data["responseData"]["translatedText"]
        )

        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, translated)
        output_box.config(state="disabled")

    except Exception as error:
        messagebox.showerror(
            "Translation Error",
            "Unable to translate your text.\n\n"
            "Please check your internet connection and try again.\n\n"
            f"Details: {error}"
        )

    finally:
        translate_button.config(
            state="normal",
            text="Translate"
        )


def copy_translation():
    translated = output_box.get("1.0", tk.END).strip()

    if not translated:
        messagebox.showwarning(
            "No Translation",
            "Translate some text first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(translated)
    root.update()
    messagebox.showinfo("Success", "Translation copied!")


def clear_text():
    input_box.delete("1.0", tk.END)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")


languages = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "Arabic": "ar",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-CN"
}


root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("650x650")
root.minsize(550, 580)
root.configure(bg="#eef3f8")

title = tk.Label(
    root,
    text="Language Translation Tool",
    font=("Arial", 22, "bold"),
    bg="#eef3f8",
    fg="#193b63"
)
title.pack(pady=(22, 5))

subtitle = tk.Label(
    root,
    text="Translate text into your preferred language",
    font=("Arial", 11),
    bg="#eef3f8",
    fg="#526579"
)
subtitle.pack(pady=(0, 20))

language_frame = tk.Frame(root, bg="#eef3f8")
language_frame.pack(pady=5)

tk.Label(
    language_frame,
    text="From:",
    font=("Arial", 11, "bold"),
    bg="#eef3f8"
).grid(row=0, column=0, padx=7, pady=5)

source_language = ttk.Combobox(
    language_frame,
    values=list(languages.keys()),
    state="readonly",
    width=13
)
source_language.set("English")
source_language.grid(row=0, column=1, padx=7, pady=5)

tk.Label(
    language_frame,
    text="To:",
    font=("Arial", 11, "bold"),
    bg="#eef3f8"
).grid(row=0, column=2, padx=7, pady=5)

target_language = ttk.Combobox(
    language_frame,
    values=list(languages.keys()),
    state="readonly",
    width=13
)
target_language.set("Urdu")
target_language.grid(row=0, column=3, padx=7, pady=5)

tk.Label(
    root,
    text="Enter your text",
    font=("Arial", 12, "bold"),
    bg="#eef3f8",
    fg="#193b63"
).pack(anchor="w", padx=45, pady=(18, 5))

input_box = tk.Text(
    root,
    height=5,
    font=("Arial", 12),
    wrap="word",
    relief="solid",
    bd=1
)
input_box.pack(fill="x", padx=40)

translate_button = tk.Button(
    root,
    text="Translate",
    command=translate_text,
    bg="#2463a6",
    fg="white",
    activebackground="#193b63",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    padx=25,
    pady=8,
    cursor="hand2"
)
translate_button.pack(pady=15)

tk.Label(
    root,
    text="Translated Result",
    font=("Arial", 12, "bold"),
    bg="#eef3f8",
    fg="#193b63"
).pack(anchor="w", padx=45, pady=(5, 5))

output_box = tk.Text(
    root,
    height=5,
    font=("Arial", 12),
    wrap="word",
    relief="solid",
    bd=1,
    state="disabled"
)
output_box.pack(fill="x", padx=40)

button_frame = tk.Frame(root, bg="#eef3f8")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Copy Translation",
    command=copy_translation,
    font=("Arial", 10, "bold"),
    padx=12,
    pady=6,
    cursor="hand2"
).grid(row=0, column=0, padx=7)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_text,
    font=("Arial", 10),
    padx=18,
    pady=6,
    cursor="hand2"
).grid(row=0, column=1, padx=7)

footer = tk.Label(
    root,
    text="Powered by MyMemory Translation API",
    font=("Arial", 9),
    bg="#eef3f8",
    fg="#526579"
)
footer.pack(side="bottom", pady=12)

root.mainloop()
