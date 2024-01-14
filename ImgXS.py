import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import sys
import subprocess

# 念のため画面初期化
subprocess.run("cls",shell=True)
print("Copyright (C) 2024 Innovation Craft")

# リソース読み込み
def resourcePath(filename):
  if hasattr(sys, "_MEIPASS"):
      return os.path.join(sys._MEIPASS, filename)
  return os.path.join(filename)
print("")
class WatermarkApp:
    def __init__(self, root):
        fontsize=15
        self.root = root
        self.root.geometry("451x300")
        self.root.title("ImgXS (透かし合成ツール) Ver 1.7")
        iconfile = resourcePath('resources/IMG_8776.ICO')
        self.root.iconbitmap(iconfile)
        # 元画像選択ボタン
        self.select_original_button = tk.Button(root, text="元画像を選択", command=self.open_original_file_dialog,font=("", fontsize))
        self.select_original_button.pack(pady=20)

        # 透かし画像選択ボタン
        self.select_watermark_button = tk.Button(root, text="透かし画像を選択", command=self.open_watermark_file_dialog,font=("", fontsize))
        self.select_watermark_button.pack(pady=20)

        # 実行ボタン
        self.execute_button = tk.Button(root, text="透かしを入れて保存", command=self.apply_watermark_and_save,font=("", fontsize))
        self.execute_button.pack(pady=20)

        # 選択されたファイルパスを保持する変数
        self.original_path = None
        self.watermark_path = None

    def open_original_file_dialog(self):
        self.original_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if self.original_path:
            self.show_dialog("元画像を選択しました:\n" + self.original_path)

    def open_watermark_file_dialog(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if self.watermark_path:
            self.show_dialog("透かし画像を選択しました:\n" + self.watermark_path)

    def apply_watermark_and_save(self):
        if self.original_path and self.watermark_path:
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                self.apply_watermark(self.original_path, self.watermark_path, output_path)
                self.show_dialog("透かしを入れた画像を保存しました:\n" + output_path)
        else:
            self.show_dialog("元画像と透かし画像を選択してください。")

    def apply_watermark(self, original_path, watermark_path, output_path):
        original_image = Image.open(original_path)
        watermark_image = Image.open(watermark_path).convert("RGBA")

        original_width, original_height = original_image.size
        watermark_width, watermark_height = watermark_image.size

        # 透かし画像が元画像より大きい場合、アスペクト比を維持してリサイズ
        if watermark_width > original_width or watermark_height > original_height:
            aspect_ratio = min(original_width / watermark_width, original_height / watermark_height)
            new_width = int(watermark_width * aspect_ratio)
            new_height = int(watermark_height * aspect_ratio)
            watermark_image = watermark_image.resize((new_width, new_height), Image.ANTIALIAS)

        x_position = (original_width - watermark_image.width) // 2
        y_position = (original_height - watermark_image.height) // 2

        original_image.paste(watermark_image, (x_position, y_position), watermark_image)
        original_image.save(output_path)

    def show_dialog(self, message):
        dialog = tk.Toplevel(self.root)
        dialog.title("確認")
        dialog.geometry("300x100")
        iconfile = resourcePath('resources/IMG_8776.ICO')
        dialog.iconbitmap(iconfile)
        label = tk.Label(dialog, text=message)
        label.pack(pady=20)
        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()