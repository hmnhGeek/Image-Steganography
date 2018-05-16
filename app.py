from Tkinter import *
import ttk
from steganographer import steganographer
import os
from tkFileDialog import *
from PIL import Image, ImageTk
import tkMessageBox
import threading
import pickle

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

global userfont, systemfont, userstyle, systemstyle
userfont = ('Courier New', 11)
systemfont = ('timesnewroman', 9)
userstyle = 'white'
systemstyle = 'red'

class TextPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		self.filename = 'No Image Chosen'

		self.filename_display = ttk.Label(self, text=self.filename, font=userfont)
		self.filename_display.pack(pady=5)

		b = ttk.Button(self, text="Choose Image", command=self.activate_textBox)
		b.pack(pady=10)

		scrollbar = Scrollbar(self)
		scrollbar.pack(side = RIGHT, fill = Y)
		self.area = Text(self, yscrollcommand = scrollbar.set, background = 'gray', foreground = userstyle
		        , font = userfont, insertbackground = 'black', insertwidth = 5, selectbackground = 'blue'
		        )
		self.area.pack(expand=True, fill='both')

		self.area.tag_config("system_alert", foreground=systemstyle, background='white')

		scrollbar.config(command = self.area.yview)
		self.area.config(state="disabled")

		self.var = IntVar()

		self.R1 = ttk.Radiobutton(self, text="Encode", variable=self.var, value=1, command=self.encode_priviliges)
		self.R1.pack(pady=5)
		self.R2 = ttk.Radiobutton(self, text="Decode", variable=self.var, value=2, command=self.decode_priviliges)
		self.R2.pack(pady=5)

		self.submit = ttk.Button(self, text="Submit", command=lambda: \
			threading.Thread(target=self.submit_func).start())
		self.submit.pack(pady=10)
		self.submit.config(state='disabled')


	def encode_priviliges(self):
		if self.filename != 'No Image Chosen':
			self.area.config(state='normal')
			self.submit.config(state='normal')
		else:
			tkMessageBox.showwarning("Alert!!", "First select an image.")
			self.var.set(3)

	def decode_priviliges(self):
		if self.filename != 'No Image Chosen':
			self.area.config(state='disabled')
			self.submit.config(state='normal')
		else:
			tkMessageBox.showwarning("Alert!!", "First select an image.")
			self.var.set(3)

	def activate_textBox(self):
		try:
			f = askopenfile()
			self.filename = f.name 
			self.filename_display.config(text=self.filename)
		except:
			pass

	def submit_func(self):
		if self.area['state'] == 'normal':
			extracted_text = self.area.get("1.0", END)

			self.area.insert(END, "\n\n")
			self.area.insert(END, "Encoding the image...\nIt might take some time...\n", "system_alert")
			self.area.config(state='disabled')

			temp_image = steganographer.write_text(extracted_text, Image.open(self.filename).size)
			# save the temporary image.
			temp_image.save("temp.png")

			# now hide the temp image.
			steganographer.encode("temp.png", self.filename)
			os.remove("temp.png")

			tkMessageBox.showinfo("Alert!!", "Image encrypted!!\nEncrypted Image: "+self.filename+"encoded.png")
			self.area.config(state='normal')
		else:
			self.area.config(state="normal")
			self.area.insert(END, "\n\n")
			self.area.insert(END, "Decoding the image...\nIt might take some time...\n", "system_alert")
			self.area.config(state='disabled')

			steganographer.decode(self.filename)
			tkMessageBox.showinfo("Alert!!", "Image decrypted!!\nDecrypted Image: "+self.filename+"decoded.png")


class LoginScreen(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		img = ImageTk.PhotoImage(Image.open("homeImage.jpg"))
		self.ImageLabel = Label(self)
		self.ImageLabel.pack()
		self.ImageLabel.image = img
		self.ImageLabel.configure(image=img)

		passwordLabel = ttk.Label(self, text="Password", font=userfont, background="#C5B358"\
			, foreground="#8B4513")
		passwordLabel.pack(pady=10)
		passwordLabel.place(x=350, y=10)

		self.password = ttk.Entry(self, show='*')
		self.password.pack(pady=5)
		self.password.place(x=310, y=30)

		self.loginbutton = ttk.Button(self, text='Login', command=self.login)
		self.loginbutton.pack(pady=20)
		self.loginbutton.place(x=350, y=60)

		self.deletebutton = ttk.Button(self, text='Delete A/C', command=self.delete)
		self.deletebutton.pack(pady=20)
		self.deletebutton.place(x=350, y=100)

		self.signupbutton = ttk.Button(self, text='Sign Up', command=self.signup)
		self.signupbutton.pack(pady=20)
		self.signupbutton.place(x=350, y=140)

		f = open("creds.dat", "rb")
		try:
			while True:
				l = pickle.load(f)
				if l == []:
					self.loginbutton.config(state='disabled')
					self.signupbutton.config(state='normal')
					self.deletebutton.config(state='disabled')
				else:
					self.loginbutton.config(state='normal')
					self.signupbutton.config(state='disabled')
					self.deletebutton.config(state='normal')
		except:
			pass
		f.close()

	def login(self):
		f = open("creds.dat", "rb")
		try:
			while True:
				l = pickle.load(f)
				registered_password = l[0].decode('base64')
		except:
			f.close()

		if self.password.get() == registered_password:
			main.tp.show()
		else:
			tkMessageBox.showwarning("Alert!!", "Wrong password entered!!")

	def signup(self):
		signupwindow = Toplevel()
		signupwindow.geometry("200x200")
		signupwindow.resizable(height=0, width=0)
		passwLabel = ttk.Label(signupwindow, text="Enter a password").pack()
		passw = ttk.Entry(signupwindow, show="*")
		passw.pack()

		def yes_sign_up():
			fw = open("temp.dat", "wb")
			pickle.dump([passw.get().encode('base64')], fw)
			fw.close()

			os.remove("creds.dat")
			os.rename("temp.dat", "creds.dat")

			self.loginbutton.config(state='normal')
			self.signupbutton.config(state='disabled')
			self.deletebutton.config(state='normal')

			tkMessageBox.showinfo("Alert!!", "You have signed up.")
			signupwindow.destroy()

		submit = ttk.Button(signupwindow, text="Sign Up", command=yes_sign_up)
		submit.pack()

	def delete(self):
		delWindow = Toplevel()
		delWindow.geometry("200x200")
		delWindow.resizable(height=0, width=0)
		passwLabel = ttk.Label(delWindow, text="Enter password to delete this a/c").pack()
		passw = ttk.Entry(delWindow, show="*")
		passw.pack()

		def yes_delete_it():
			f = open("creds.dat", "rb")
			try:
				while True:
					l = pickle.load(f)
					registered_password = l[0].decode('base64')
			except:
				f.close()

			if passw.get() == registered_password:
				os.remove("creds.dat")
				f = open("creds.dat", "wb")
				pickle.dump([], f)
				f.close()

				self.loginbutton.config(state='disabled')
				self.signupbutton.config(state='normal')
				self.deletebutton.config(state='disabled')

				tkMessageBox.showinfo("Alert!!", "A/C deleted!!")
				delWindow.destroy()
			else:
				tkMessageBox.showwarning("Alert!!", "Wrong password enetered!")

		submit = ttk.Button(delWindow, text="Delete A/C", command=yes_delete_it)
		submit.pack()

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.tp = TextPage()
        self.lp = LoginScreen()
        self.container = Frame(self)
        self.container.pack(side = 'top', fill = 'both', expand = True)
        self.tp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        self.lp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        self.lp.show()


if __name__ == '__main__':
    root = Tk()

    main = MainView(root)
    main.pack(side = 'top', fill = 'both', expand = True)

    root.wm_geometry('800x600')
    root.resizable(height=0, width=0)

    root.title('Image Steganographer')

    root.mainloop()
        
        
