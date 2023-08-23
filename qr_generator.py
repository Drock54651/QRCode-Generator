import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode
try: 
    from ctypes import windll, byref, sizeof, c_int #! changes title bar color
except:
    pass

class App(ctk.CTk): #! Main Window 
    def __init__(self):
        self.title_bar_color()

        #* Window set up
        ctk.set_appearance_mode('light')
        super().__init__(fg_color= 'white')

        #*Customization  
        self.geometry('400x400')
        self.title('') #! no title
        self.iconbitmap('PythonTkinter/4QR Code/empty.ico') #! gets rid of icon
         
        #*Entry field   
        self.entry_string = ctk.StringVar()
        self.entry_string.trace('w', self.create_qr) #! when entry field is changed, call the func

        EntryField(self, self.entry_string, self.save) 
        
        self.bind('<Return>', self.save)


        #* QR code

        self.QR_image = None
        self.QR_image_tk = None
        self.qr_image = QRImage(self)


        #*Run
        self.mainloop() 

    def create_qr(self, *args): #! need args for trace, everytime entry field is changed, this func will run, making new qr codes
        current_text = self.entry_string.get()

        if current_text: #! if text is in entry field create QR image
            self.QR_image = qrcode.make(current_text).resize((400,400)) #! makes a unique qr in respect to whatevers in the entry field, so for example i can connect links to the QR code
            self.QR_image_tk = ImageTk.PhotoImage(self.QR_image) #! needs to be in same scope as mainloop so use self.
            self.qr_image.update_image(self.QR_image_tk)

        else: #! no text so nothing there
            self.qr_image.clear()
            self.QR_image = None
            self.tk_image = None

    def save(self, event = ''): #! user can save qr as a jpg to their machine
        if self.QR_image: #! check if the Qr image exists
            file_path = filedialog.asksaveasfilename() #! gets path to wherever user wants

            if file_path:
                self.QR_image.save(file_path + '.jpg') #! actually saves it to file path

    def title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND,
                                                 35,
                                                  byref(c_int(0x00FFFFFF)),
                                                  sizeof(c_int))
        except:
            pass

       

class EntryField(ctk.CTkFrame): #! create entry field and button
    def __init__(self,parent, entry_string, save_function):
        super().__init__(parent, corner_radius = 20, fg_color = '#021fb3')
        self.place(relx = .5, rely = 1, relwidth = 1, relheight = .4, anchor = 'center')  #! make and place frame with center at the bottom of window
                                                                                          
        
        #*Grid layout: since i only want to work with the top half of the frame, i will use grid to play widgets on top half
        self.rowconfigure((0,1), weight = 1, uniform = 'a') 
        self.columnconfigure(0, weight = 1, uniform = 'a')
        
        #*Widgets
        self.widget_frame = ctk.CTkFrame(self, fg_color = 'transparent')
        self.widget_frame.grid(row = 0, column = 0) #! frame created and placed within the main frame

        #! to space out widgets nicely, could use other layout methods though
        self.widget_frame.columnconfigure(0, weight = 1, uniform = 'b')
        self.widget_frame.columnconfigure(1, weight = 4, uniform = 'b')
        self.widget_frame.columnconfigure(2, weight = 2, uniform = 'b')
        self.widget_frame.columnconfigure(3, weight = 1, uniform = 'b')

        entry = ctk.CTkEntry(
            self.widget_frame, 
            fg_color = '#2e54e8', 
            border_width = 0, 
            text_color = 'white',
            textvariable = entry_string)
        
        entry.grid(row = 0, column = 1, sticky = 'news')

        button = ctk.CTkButton(
            self.widget_frame, 
            text = 'save', 
            fg_color = '#2e54e8', 
            hover_color = '#4266f1', 
            command  =  save_function)
        
        button.grid(row = 0, column = 2, padx = 10, sticky = 'news')

class QRImage(tk.Canvas): #! making canvas and putting images inside it
    def __init__(self,parent):
        super().__init__(parent, background = 'white', bd = 0, highlightthickness = 0, relief = 'ridge') #! gets rid of canvas outline

        self.place(relx = .5, rely = .4, width = 400, height = 400, anchor = 'center') #! placing canvas in center of avaliable space
                                                                                       #! height of blue frame is .4, however only showing half
                                                                                       #! so actual shown height = .2
                                                                                       #! 1 - .2 = .8
                                                                                       #! rely = .8 / 2 to place in center

    def update_image(self,image_tk): #! takes in new image and update
        self.clear() #! so the qr doesnt keep stacking on each other
        self.create_image(0,0, image = image_tk, anchor = 'nw')


    def clear(self): #! clears image when no text in entry field
        self.delete('all')




App()