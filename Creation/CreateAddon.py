import os
os.system("cls")
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
import json


class GameVersion:
    def __init__(self, full:int, sub:int, minor:int = 0, isDev:bool=False):
        self.full:int = full
        self.sub:int = sub
        self.minor:int = minor
        self.isDev:bool = isDev
    def GetAsList(self):
        return [self.full, self.sub, self.minor]
    def __str__(self):
        return f"{self.full}.{self.sub}.{self.minor}{" - DEV" if self.isDev else ""}"

supportedGameVersions:list[GameVersion] = [GameVersion(0, 4, 10, True), GameVersion(0, 5)]  

addonCreatorVersion:GameVersion = GameVersion(1, 0, 0)

def AddTextInput(root, title:str, sampleText:str, height:int=1) -> tk.Text:
    tk.Label(root, text=title).pack()
    inputBox = tk.Text(root, height=height, width=40)
    inputBox.pack()
    inputBox.insert(tk.END, sampleText)
    return inputBox

def MakeWindow():
    global root
    root = tk.Tk()
    root.title(f"Really Fast Rat Addon Creation Helper - {addonCreatorVersion}")
    root.minsize(1000, 700)
    root.maxsize(1000, 700)
    
    tk.Label(root,text="Create New Addon",font=("Font", 15),).pack(ipady=5, fill="x")

    namespaceInputBox = AddTextInput(root, "Namespace", "NewAddon")
    nameInputBox = AddTextInput(root, "Display Name", "New Addon")
    authorInputBox = AddTextInput(root, "Author Name", os.getlogin())
    descriptionInputBox = AddTextInput(root, "Description", "This is a new addon!", 3)

    version = tk.StringVar(value=supportedGameVersions[-1])  

    tk.Label(root, text="Game Version").pack()
    tk.OptionMenu(root, version, *supportedGameVersions).pack()  

    create = tk.Button(root, text="Create", command=lambda: MakeNewAddon(namespaceInputBox, nameInputBox, authorInputBox, descriptionInputBox, version), font=("Font", 15))
    create.pack(pady=100)

def MakeNewAddon(namespaceInputBox:tk.Text, nameInputBox:tk.Text, authorInputBox:tk.Text, descriptionInputBox:tk.Text, version:tk.StringVar):
    namespace = namespaceInputBox.get("1.0", "end-1c")
    if len(namespace) == 0:
        mb.showerror("Error!", "No namespace given!")
        return
    elif " " in namespace:
        mb.showerror("Error!", "Namespace cannot contain spaces!")
        return
    
    mb.showinfo("Select a folder", "Select the folder you would like to create your addon inside.")
    addonFolder:str = filedialog.askdirectory(mustexist=True)

    if not os.path.exists(addonFolder):
        mb.showerror("Error!", "No folder selected!")
        return
    
    empty:bool = True
    for _ in os.scandir(addonFolder):
        empty = False
        break

    if not empty:
        mb.showerror("Error!", "This folder is not empty!")
        return
    else:
        manifest = CreateManifest(
            nameInputBox.get("1.0", "end-1c"),
            descriptionInputBox.get("1.0", "end-1c"),
            namespaceInputBox.get("1.0", "end-1c"),
            authorInputBox.get("1.0", "end-1c"),
            version.get()
        )
        manifestPath:str = f"{addonFolder}\\Manifest.json"
        os.makedirs(os.path.dirname(manifestPath), exist_ok=True)
        with open(manifestPath, "w") as file:
            json.dump(manifest, file, indent=4)
        os.makedirs(f"{addonFolder}\\{manifest["namespace"]}")
        os.makedirs(f"{addonFolder}\\Assets")
        os.startfile(addonFolder)

def CreateManifest(name:str, description:str, namespace:str, author:str, version:str, instanced:bool=False) -> dict:
    versionClass:GameVersion
    for v in supportedGameVersions:
        if str(v) == version:
            versionClass = v
    return { 
        "game-version": versionClass.GetAsList(),
        "namespace": namespace,
        "info":{
            "name": name,
            "author": author,
            "description": description
        },
        "instanced": instanced
    }


    


MakeWindow()
root.mainloop()