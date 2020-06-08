import tkinter as tk                            #Tkinterインポート
from tkinter import ttk as ttk                  #ttkインポート
from tkinter.filedialog import askopenfilename  #ファイルオープン用
from PIL import Image, ImageTk                  #画像処理用
from numpy import array                         #データ処理用


#メインクラス
class Main:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Image Background Remover")
        self.root.minsize(width=500, height=500)
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        
        #グローバル変数
        self.imageString = ""
        self.image = None
        self.photo = None
        self.data = None
        self.redData = None
        self.greenData = None
        self.blueData = None
        self.alphaData = None
        self.redMask = 220
        self.greenMask = 220
        self.blueMask = 220
        self.alphaMask = 255
        self.maskBoolean = tk.BooleanVar(value=True)

        #メニューバー
        self.mainMenu = tk.Menu(self.root)
        self.root.config(menu=self.mainMenu)

        self.fileMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="ファイル", menu=self.fileMenu)
        self.fileMenu.add_command(label="画像を開く", command=self.openImage)
        self.fileMenu.add_command(label="画像を閉じる", command=self.closeImage)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="画像を保存", command=self.saveImage)
        self.fileMenu.add_command(label="終了", command=self.quit)

        self.editMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="編集", menu=self.editMenu)
        self.editMenu.add_command(label="背景を削除する", command=self.removeBackground)

        self.helpMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="ヘルプ", menu=self.helpMenu)
        self.helpMenu.add_command(label="（未実装）", command=self.quit)

        # ***** content frame *****
        self.contentFrame = tk.Frame(self.root)
        self.contentFrame.pack(expand=True, fill=tk.BOTH)

        # ***** left frame *****
        self.leftFrame = tk.Frame(self.contentFrame, bg="grey")
        self.leftFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.imageLabel = tk.Label(self.leftFrame, bg="grey")
        self.imageLabel.pack(expand=True)

        # ***** right frame *****
        self.rightFrame = tk.Frame(self.contentFrame)
        self.rightFrame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.rightFrame.tkraise()

        # ***** top right frame *****
        self.topRightFrame = tk.Frame(self.rightFrame)
        self.topRightFrame.pack(side=tk.TOP)

        self.fileLabel = tk.Label(self.topRightFrame, text="ファイル名:")
        self.fileLabel.pack(fill=tk.X, expand=True)

        self.fileEntry = tk.Entry(self.topRightFrame)
        self.fileEntry.bind('<Return>', self.openImage)
        self.fileEntry.pack(fill=tk.X, expand=True)

        self.openButton = tk.Button(self.topRightFrame, text="画像を開く", command=self.openImage)
        self.openButton.pack(fill=tk.X, pady=10, expand=True)

        self.closeButton = tk.Button(self.topRightFrame, text="画像を閉じる", command=self.closeImage)
        self.closeButton.pack(fill=tk.X, expand=True)

        # ***** middle right frame *****
        self.middleRightFrame = tk.Frame(self.rightFrame)
        self.middleRightFrame.pack(side=tk.TOP, fill=tk.X, pady=30)

        self.backgroundRemovalLabel = tk.Label(self.middleRightFrame, text="Background Removal")
        self.backgroundRemovalLabel.pack(fill=tk.X, expand=True)

        self.redSlider = tk.Scale(self.middleRightFrame, from_=0, to=255, orient=tk.HORIZONTAL, bg="red", fg="white")
        self.redSlider.set(self.redMask)
        self.redSlider.pack(fill=tk.X, expand=True)

        self.greenSlider = tk.Scale(self.middleRightFrame, from_=0, to=255, orient=tk.HORIZONTAL, bg="green", fg="white")
        self.greenSlider.set(self.greenMask)
        self.greenSlider.pack(fill=tk.X, expand=True)

        self.blueSlider = tk.Scale(self.middleRightFrame, from_=0, to=255, orient=tk.HORIZONTAL, bg="blue", fg="white")
        self.blueSlider.set(self.blueMask)
        self.blueSlider.pack(fill=tk.X, expand=True)

        self.alphaSlider = tk.Scale(self.middleRightFrame, from_=0, to=255, orient=tk.HORIZONTAL, bg="black", fg="white")
        self.alphaSlider.set(self.alphaMask)
        self.alphaSlider.pack(fill=tk.X, expand=True)

        self.maskButton = tk.Checkbutton(self.middleRightFrame, text="スライドー値以上", variable=self.maskBoolean)
        self.maskButton.pack(fill=tk.X, pady=10, expand=True)

        self.removeBackgroundButton = tk.Button(self.middleRightFrame, text="背景を削除", command=self.removeBackground)
        self.removeBackgroundButton.pack(fill=tk.X, expand=True)

        # ***** bottom right frame *****
        self.bottomRightFrame = tk.Frame(self.rightFrame)
        self.bottomRightFrame.pack(side=tk.BOTTOM, fill=tk.X)

        self.undoButton = tk.Button(self.bottomRightFrame, text="変更を元に戻す", command=self.undo)
        self.undoButton.pack(fill=tk.X, expand=True)

        self.saveButton = tk.Button(self.bottomRightFrame, text="画像を保存", command=self.saveImage)
        self.saveButton.pack(fill=tk.X, pady=10, expand=True)

        self.quitButton = tk.Button(self.bottomRightFrame, text="終了", command=self.quit)
        self.quitButton.pack(fill=tk.X, expand=True)

        # ***** status bar *****
        self.status = tk.Label(self.root, text="画像が開かれていません", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def openImage(self, event=None):
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, askopenfilename(initialdir = "~", title = "ファイルを選択", filetypes = (("JPEG", "*.jpg"), ("PNG", "*.png"), ("すべてのファイル", "*.*"))))
        self.imageString = self.fileEntry.get()
        
        if "." not in self.imageString and not self.imageString == "":
            self.imageString += ".jpg"
            
        if self.imageString == "":
            self.closeImage()
            self.status.configure(text="画像が開かれていません " + self.imageString)
        else:
            try:
                self.status.configure(text="画像を開いています " + self.imageString)
                self.image = Image.open(self.imageString)

                if (self.image.size[0] > self.leftFrame.winfo_width()):
                    sf = self.leftFrame.winfo_width() / self.image.size[0]
                    scaledHeight = int(self.image.size[1] * sf)
                    self.imageDisplay = self.image.resize((self.leftFrame.winfo_width(), scaledHeight), Image.ANTIALIAS)

                elif (self.image.size[1] > self.imageLabel.winfo_height()):
                    sf = self.leftFrame.winfo_height() / self.image.size[1]
                    scaledWidth = int(self.image.size[0] * sf)
                    self.imageDisplay = self.image.resize((scaledWidth, self.leftFrame.winfo_height()), Image.ANTIALIAS)
                    
                self.photoDisplay = ImageTk.PhotoImage(self.imageDisplay)
                self.imageLabel.configure(image=self.photoDisplay)
                self.status.configure(text="編集中 " + self.imageString)

            except FileNotFoundError:
                self.closeImage()
                self.status.configure(text="ファイルが見つかりません: " + self.imageString)

    def closeImage(self):
        self.status.configure(text="画像が開かれていません")
        self.fileEntry.delete(0, tk.END)
        self.imageLabel.configure(image="")

    def undo(self):
        try:
            self.status.configure(text="画像を開いています " + self.imageString)
            self.image = Image.open(self.imageString)
            
            if (self.image.size[0] > self.leftFrame.winfo_width()):
                sf = self.leftFrame.winfo_width() / self.image.size[0]
                scaledHeight = int(self.image.size[1] * sf)
                self.imageDisplay = self.image.resize((self.leftFrame.winfo_width(), scaledHeight), Image.ANTIALIAS)
                
            elif (self.image.size[1] > self.imageLabel.winfo_height()):
                sf = self.leftFrame.winfo_height() / self.image.size[1]
                scaledWidth = int(self.image.size[0] * sf)
                self.imageDisplay = self.image.resize((scaledWidth, self.leftFrame.winfo_height()), Image.ANTIALIAS)
                

            self.photoDisplay = ImageTk.PhotoImage(self.imageDisplay)
            self.imageLabel.configure(image=self.photoDisplay)
            self.status.configure(text="編集中 " + self.imageString)
            
        except FileNotFoundError:
            self.closeImage()
            self.status.configure(text="ファイルが見つかりません: " + self.imageString)

    def removeBackground(self):
        try:
            self.editedImage = self.image.convert('RGBA')
        except:
            self.status.configure(text="画像を開いてください")
            
            return
        
        self.data = array(self.editedImage)
        [self.redData, self.greenData, self.blueData, self.alphaData] = self.data.T

        self.redMask = self.redSlider.get()
        self.greenMask = self.greenSlider.get()
        self.blueMask = self.blueSlider.get()
        self.alphaMask = self.alphaSlider.get()

        # creates a mask for pixels that fit user defined parameters
        if self.maskBoolean.get():
            mask = (self.redData >= self.redMask) & (self.greenData >= self.greenMask) & (self.blueData >= self.blueMask) & (self.alphaData >= self.alphaMask)
            
        else:
            mask = (self.redData <= self.redMask) & (self.greenData <= self.greenMask) & (self.blueData <= self.blueMask) & (self.alphaData >= self.alphaMask)

        # alters pixels included in the mask to be transparent
        self.data[mask.T] = (0, 0, 0, 0)

        # converts four interconnected arrays back into image interpretation
        self.editedImage = Image.fromarray(self.data)
        if (self.editedImage.size[0] > self.leftFrame.winfo_width()):
            sf = self.leftFrame.winfo_width() / self.editedImage.size[0]
            scaledHeight = int(self.editedImage.size[1] * sf)
            self.imageDisplay = self.editedImage.resize((self.leftFrame.winfo_width(), scaledHeight), Image.ANTIALIAS)
            
        elif (self.editedImage.size[1] > self.imageLabel.winfo_height()):
            sf = self.leftFrame.winfo_height() / self.editedImage.size[1]
            scaledWidth = int(self.editedImage.size[0] * sf)
            self.imageDisplay = self.editedImage.resize((scaledWidth, self.leftFrame.winfo_height()), Image.ANTIALIAS)
            
        # self.photo = ImageTk.PhotoImage(self.editedImage)
        self.photoDisplay = ImageTk.PhotoImage(self.imageDisplay)
        self.imageLabel.configure(image=self.photoDisplay)

        self.status.configure(text=self.imageString + " は画像を削除されています。")

    def saveImage(self):
        try:
            # creates a new file name based on the input and saves the edited image under that name
            outputFile = self.imageString[0:len(self.imageString) - 4] + "-edit.png"
            self.editedImage.save(outputFile)
            self.status.configure(text="画像を " + outputFile + " に保存しました。")
        except:
            self.status.configure(text="ファイルは保存されていません")

    def quit(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Main().run()
