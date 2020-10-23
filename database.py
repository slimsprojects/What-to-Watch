# Description: This is an application for users to store Movies and TV Shows in a database, allowing for editing and sorting, with a gui 

import tkinter as tk 
from tkinter import ttk
from tkinter import font as tkfont
from PIL import ImageTk, Image
import sqlite3
import imdb
from tkmacosx import SFrame

class View(tk.Tk):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.main_Frame = ttk.Frame(self, width=600, height=400, padding=(0, 0, 0, 0))
        self.main_Frame.grid(row=0, column=0)

        self._make_start_frame()
        #self._make_add_frame()

        self._center_window()


    def main(self):
        self.title('What To Watch')
        self.resizable(width=False, height=False)
        self.mainloop()

    
##### START FRAME main menu #####
    def _make_start_frame(self):
        self.start_frame = ttk.Frame(self.main_Frame)
        self.start_frame.pack()

        # Background image and canvas
        #n=0.25
        # Adding a background image
        background_img = Image.open("light-bulbs.jpg")
        #[imageSizeWidth, imageSizeHeight] = background_img.size
        #background_img = background_img.resize((newImageSizeWidth,newImageSizeHeight),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(background_img)
        self.canvas_main = tk.Canvas(self.start_frame)
        self.canvas_main.create_image(300, 300, image = img)      
        self.canvas_main.config(bg="white",width = 600, height = 450)
        self.canvas_main.img = img
        self.canvas_main.pack(expand=True, fill='both')

        # Header 
        self.headingFrame1 = tk.Frame(self.start_frame,bg="#FFBB00",bd=5)
        self.headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
        headingLabel = tk.Label(self.headingFrame1, text="What to Watch \n Library", bg='black', fg='white', font=('Courier',15))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

        # Buttons
        self.button_frame = ttk.Frame(self.start_frame)
        self.button_frame.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.35)
        view_list_btn = tk.Button(self.button_frame,text="View My List",bg='black', fg='white', command=self._make_view_frame)
        view_list_btn.pack(expand=True, fill='both')
        add_btn = tk.Button(self.button_frame,text="Add Title",bg='black', fg='white', command=self._make_add_frame)
        add_btn.pack(expand=True, fill='both')

        ## Buttons
        # view_list_btn = tk.Button(self.start_frame,text="View My List",bg='black', fg='white')
        # view_list_btn.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
        # add_btn = tk.Button(self.start_frame,text="Add Title",bg='black', fg='white')
        # add_btn.place(relx=0.28,rely=0.5, relwidth=0.45,relheight=0.1)
        # edit_btn = tk.Button(self.start_frame,text="Edit Desire/Rank",bg='black', fg='white')
        # edit_btn.place(relx=0.28,rely=0.6, relwidth=0.45,relheight=0.1)
        # delete_btn = tk.Button(self.start_frame,text="Delete Title",bg='black', fg='white')
        # delete_btn.place(relx=0.28,rely=0.7, relwidth=0.45,relheight=0.1)
        
        self.gui_elements = [
            self.start_frame,
            self.canvas_main,
            self.headingFrame1,
            self.button_frame
        ]


##### VIEW FRAME #####
    def _make_view_frame(self):
        self.gui_elements_remove(self.gui_elements)

        self.view_frame = ttk.Frame(self.main_Frame)
        self.view_frame.pack(expand=True, fill='both')
        
        self.n = ttk.Notebook(self.view_frame)
        f1 = ttk.Frame(self.n) # All   
        f2 = ttk.Frame(self.n) # Movies
        f3 = ttk.Frame(self.n) # Shows
        self.n.add(f1, text='All')
        self.n.add(f2, text='Movies')
        self.n.add(f3, text='Shows')
        self.n.grid(row=0,column=0)
        
        ### SHOW ALL ### 
        def show_lists():
            # Create a database or connect to one
            conn = sqlite3.connect('MovieDesire.db')
            # Create cursor
            c = conn.cursor()

            # Query the db
            c.execute("SELECT *, oid FROM moviedesireDB")
            records = c.fetchall()
            #print(records)

            # Loop through results
            # All
            print_titles_A = ''
            print_desirerank_A = ''
            for record in records:
                #imdb_rate = get_imdb_rating(str(record[0]))
                print_titles_A += str(record[5]) + " : " + str(record[0]) + "\n"
                print_desirerank_A += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f1
            label_frame_A = SFrame(f1, width=550)
            label_frame_A.pack()
            # header
            print_titleheader_A_label = tk.Label(label_frame_A, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_A_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_A_header_label = tk.Label(label_frame_A, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_A_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_A_label = tk.Label(label_frame_A, text=print_titles_A, justify='left')
            print_titles_A_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_A_label = tk.Label(label_frame_A, text=print_desirerank_A, justify='left')
            print_desirerank_A_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Movies
            print_titles_M = ''
            print_desirerank_M = ''
            for record in records:
                if str(record[4]) == 'M':
                    print_titles_M += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_M += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f2
            label_frame_M = SFrame(f2, width=550)
            label_frame_M.pack()
            # header
            print_titleheader_M_label = tk.Label(label_frame_M, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_M_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_M_header_label = tk.Label(label_frame_M, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_M_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_M_label = tk.Label(label_frame_M, text=print_titles_M, justify='left')
            print_titles_M_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_M, justify='left')
            print_desirerank_M_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Shows
            print_titles_S = ''
            print_desirerank_S = ''
            for record in records:
                if str(record[4]) == 'S':
                    print_titles_S += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_S += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f3
            label_frame_S = SFrame(f3, width=550)
            label_frame_S.pack()
            # header
            print_titleheader_label = tk.Label(label_frame_S, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_S_header_label = tk.Label(label_frame_S, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_S_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_S_label = tk.Label(label_frame_S, text=print_titles_S, justify='left')
            print_titles_S_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_S_label = tk.Label(label_frame_S, text=print_desirerank_S, justify='left')
            print_desirerank_S_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Commit changes
            conn.commit()
            #Close connection
            conn.close()
        

        ### DESIRE HIGHLOW ###
        def desire_highlow():
            self.n.destroy()

            self.n = ttk.Notebook(self.view_frame)
            f1 = ttk.Frame(self.n) # All   
            f2 = ttk.Frame(self.n) # Movies
            f3 = ttk.Frame(self.n) # Shows
            self.n.add(f1, text='All')
            self.n.add(f2, text='Movies')
            self.n.add(f3, text='Shows')
            self.n.grid(row=0,column=0)

            # Create a database or connect to one
            conn = sqlite3.connect('MovieDesire.db')
            # Create cursor
            c = conn.cursor()

            # Query the db
            c.execute("SELECT *, oid FROM moviedesireDB ORDER BY movie_desire DESC")
            highlow_var = c.fetchall()

            # Loop through results
            # All
            print_titles_A = ''
            print_desirerank_A = ''
            for record in highlow_var:
                #imdb_rate = get_imdb_rating(str(record[0]))
                print_titles_A += str(record[5]) + " : " + str(record[0]) + "\n"
                print_desirerank_A += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f1
            label_frame_A = SFrame(f1, width=550)
            label_frame_A.pack()
            # header
            print_titleheader_A_label = tk.Label(label_frame_A, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_A_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_A_header_label = tk.Label(label_frame_A, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_A_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_A_label = tk.Label(label_frame_A, text=print_titles_A, justify='left')
            print_titles_A_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_A_label = tk.Label(label_frame_A, text=print_desirerank_A, justify='left')
            print_desirerank_A_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Movies
            print_titles_M = ''
            print_desirerank_M = ''
            for record in highlow_var:
                if str(record[4]) == 'M' and str(record[2]) == '':
                    print_titles_M += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_M += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f2
            label_frame_M = SFrame(f2, width=550)
            label_frame_M.pack()
            # header
            print_titleheader_M_label = tk.Label(label_frame_M, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_M_label.grid(row=1, column=0, ipadx=15, sticky='w')
            #print_desirerank_M_header_label = tk.Label(label_frame_M, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_M_header_label = tk.Label(label_frame_M, text=" Desire: " + "\t" + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_M_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_M_label = tk.Label(label_frame_M, text=print_titles_M, justify='left')
            print_titles_M_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_M, justify='left')
            print_desirerank_M_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Shows
            print_titles_S = ''
            print_desirerank_S = ''
            for record in highlow_var:
                if str(record[4]) == 'S' and str(record[2]) == '':
                    print_titles_S += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_S += str(record[1]) + "\t" + str(record[2]) + "\t" + str(record[3]) + "\n"
            # frame in f3
            label_frame_S = SFrame(f3, width=550)
            label_frame_S.pack()
            # header
            print_titleheader_label = tk.Label(label_frame_S, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_label.grid(row=1, column=0, ipadx=15, sticky='w')
            #print_desirerank_S_header_label = tk.Label(label_frame_S, text=" Desire: " + "\t" + "  Rank: " + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_S_header_label = tk.Label(label_frame_S, text=" Desire: " + "\t" + "\t" + "  IMDB Rating:", justify='left', font="none 15 underline")
            print_desirerank_S_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_S_label = tk.Label(label_frame_S, text=print_titles_S, justify='left')
            print_titles_S_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_S_label = tk.Label(label_frame_S, text=print_desirerank_S, justify='left')
            print_desirerank_S_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Commit changes
            conn.commit()
            #Close connection
            conn.close()


        ### RANK HIGHLOW ###
        def rank_highlow():
            self.n.destroy()

            self.n = ttk.Notebook(self.view_frame)
            f1 = ttk.Frame(self.n) # All   
            f2 = ttk.Frame(self.n) # Movies
            f3 = ttk.Frame(self.n) # Shows
            self.n.add(f1, text='All')
            self.n.add(f2, text='Movies')
            self.n.add(f3, text='Shows')
            self.n.grid(row=0,column=0)

            # Create a database or connect to one
            conn = sqlite3.connect('MovieDesire.db')
            # Create cursor
            c = conn.cursor()

            # Query the db
            c.execute("SELECT *, oid FROM moviedesireDB ORDER BY watched_rank DESC")
            records = c.fetchall() 
            #print(records)

            # Loop through results
            # All
            print_titles_A = ''
            print_desirerank_A = ''
            print_titles_A_no_rank = ''
            print_desirerank_A_no_rank = ''
            for record in records:
                if record[2] != '':
                    #imdb_rate = get_imdb_rating(str(record[0]))
                    print_titles_A += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_A += str(record[2]) + "\t" + str(record[1]) + "\t" + str(record[3]) + "\n"
                else:
                    print_titles_A_no_rank += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_A_no_rank += str(record[2]) + "\t" + str(record[1]) + "\t" + str(record[3]) + "\n"
            # frame in f1
            label_frame_A = SFrame(f1, width=550)
            label_frame_A.pack()
            # header
            print_titleheader_A_label = tk.Label(label_frame_A, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_A_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_A_header_label = tk.Label(label_frame_A, text="My Rank: " + " \t " + " Desire: " + "\t" + " IMDB Rating: ", justify='left', font="none 15 underline")
            print_desirerank_A_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_A_label = tk.Label(label_frame_A, text=print_titles_A, justify='left')
            print_titles_A_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_A_label = tk.Label(label_frame_A, text=print_desirerank_A, justify='left')
            print_desirerank_A_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')
            print_titles_A_no_rank_label = tk.Label(label_frame_A, text=print_titles_A_no_rank, justify='left')
            print_titles_A_no_rank_label.grid(row=3, column=0, ipadx=15, sticky='w')
            print_desirerank_A_no_rank_label = tk.Label(label_frame_A, text=print_desirerank_A_no_rank, justify='left')
            print_desirerank_A_no_rank_label.grid(row=3, column=1, padx=15, ipadx=30, sticky='w')

            # Movies
            print_titles_M = ''
            print_desirerank_M = ''
            for record in records:
                if str(record[4]) == 'M' and str(record[2]) != '':
                    print_titles_M += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_M += str(record[2]) + "\t" + str(record[1]) + "\t" + str(record[3]) + "\n"
            # frame in f2
            label_frame_M = SFrame(f2, width=550)
            label_frame_M.pack()
            # header
            print_titleheader_M_label = tk.Label(label_frame_M, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_M_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_M_header_label = tk.Label(label_frame_M, text="My Rank: " + " \t " + " Desire: " + "\t" + " IMDB Rating: ", justify='left', font="none 15 underline")
            print_desirerank_M_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_M_label = tk.Label(label_frame_M, text=print_titles_M, justify='left')
            print_titles_M_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_M, justify='left')
            print_desirerank_M_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Shows
            print_titles_S = ''
            print_desirerank_S = ''
            for record in records:
                if str(record[4]) == 'S' and str(record[2]) != '':
                    print_titles_S += str(record[5]) + " : " + str(record[0]) + "\n"
                    print_desirerank_S += str(record[2]) + "\t" + str(record[1]) + "\t" + str(record[3]) + "\n"
            # frame in f3
            label_frame_S = SFrame(f3, width=550)
            label_frame_S.pack()
            # header
            print_titleheader_label = tk.Label(label_frame_S, text="ID:  " + "Title: ", justify='left', font="none 15 underline")
            print_titleheader_label.grid(row=1, column=0, ipadx=15, sticky='w')
            print_desirerank_S_header_label = tk.Label(label_frame_S, text="My Rank: " + " \t " + " Desire: " + "\t" + " IMDB Rating: ", justify='left', font="none 15 underline")
            print_desirerank_S_header_label.grid(row=1, column=1, padx=15, sticky='w')
            # info
            print_titles_S_label = tk.Label(label_frame_S, text=print_titles_S, justify='left')
            print_titles_S_label.grid(row=2, column=0, ipadx=15)
            print_desirerank_S_label = tk.Label(label_frame_S, text=print_desirerank_S, justify='left')
            print_desirerank_S_label.grid(row=2, column=1, padx=15, ipadx=30, sticky='w')

            # Commit changes
            conn.commit()
            #Close connection
            conn.close()

        ### BY DESIRE ###
        def bydesire():
            get_desire_entry = desire_entry.get()
            if get_desire_entry != '':
                self.n.destroy()

                self.n = ttk.Notebook(self.view_frame)
                f1 = ttk.Frame(self.n) # All   
                f2 = ttk.Frame(self.n) # Movies
                f3 = ttk.Frame(self.n) # Shows
                self.n.add(f1, text='All')
                self.n.add(f2, text='Movies')
                self.n.add(f3, text='Shows')
                self.n.grid(row=0,column=0)

                # Create a database or connect to one
                conn = sqlite3.connect('MovieDesire.db')
                # Create cursor
                c = conn.cursor()

                # Query the db
                c.execute("SELECT *, oid FROM moviedesireDB WHERE movie_desire =" + str(get_desire_entry))
                records = c.fetchall() 
                #print(records)

                # Loop through results
                if len(records) == 0:
                    label_frame_A = tk.Frame(f1, width=550)
                    label_frame_A.pack()
                    print_titles_M = "No titles with selected desire"
                    print_titles_M_label = tk.Label(label_frame_A, text=print_titles_M, justify='left')
                    print_titles_M_label.pack()
                else:
                    # All
                    print_titles_A = ''
                    print_desirerank_A = ''
                    for record in records:
                        #imdb_rate = get_imdb_rating(str(record[0]))
                        print_titles_A += str(record[5]) + " : " + str(record[0]) + "\n"
                        print_desirerank_A += "Desire: " + str(record[1]) + " | Rank: " + str(record[2]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_A == '':
                        print_titles_A = "No titles with selected desire"
                    # frame in f1
                    label_frame_A = SFrame(f1, width=550)
                    label_frame_A.pack()
                    # info
                    print_titles_A_label = tk.Label(label_frame_A, text=print_titles_A, justify='left')
                    print_titles_A_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_A_label = tk.Label(label_frame_A, text=print_desirerank_A, justify='left')
                    print_desirerank_A_label.grid(row=1, column=1, padx=50, pady=40)

                    # Movies
                    print_titles_M = ''
                    print_desirerank_M = ''
                    for record in records:
                        if str(record[4]) == 'M':
                            print_titles_M += str(record[5]) + " : " + str(record[0]) + "\n"
                            print_desirerank_M += "Desire: " + str(record[1]) + " | Rank: " + str(record[2]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_M == '':
                        print_titles_M = "No movies with selected desire"
                    # frame in f2
                    label_frame_M = SFrame(f2, width=550)
                    label_frame_M.pack()
                    # info
                    print_titles_M_label = tk.Label(label_frame_M, text=print_titles_M, justify='left')
                    print_titles_M_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_M, justify='left')
                    print_desirerank_M_label.grid(row=1, column=1, padx=50, pady=40)

                    # Shows
                    print_titles_S = ''
                    print_desirerank_S = ''
                    for record in records:
                        if str(record[4]) == 'S':
                            print_titles_S += str(record[5]) + " : " + str(record[0]) + "\n"
                            print_desirerank_S += "Desire: " + str(record[1]) + " | Rank: " + str(record[2]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_S == '':
                        print_titles_S = "No shows with selected desire"
                    # frame in f3
                    label_frame_M = SFrame(f3, width=550)
                    label_frame_M.pack()
                    # info
                    print_titles_M_label = tk.Label(label_frame_M, text=print_titles_S, justify='left')
                    print_titles_M_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_S, justify='left')
                    print_desirerank_M_label.grid(row=1, column=1, padx=50, pady=40)

                # Commit changes
                conn.commit()
                #Close connection
                conn.close()

                desire_entry.delete(0, 'end') # Clear entry box
        


        ### BY RANK ###
        def byrank():
            get_rank_entry = rank_entry.get()
            if get_rank_entry != '':
                self.n.destroy()

                self.n = ttk.Notebook(self.view_frame)
                f1 = ttk.Frame(self.n) # All   
                f2 = ttk.Frame(self.n) # Movies
                f3 = ttk.Frame(self.n) # Shows
                self.n.add(f1, text='All')
                self.n.add(f2, text='Movies')
                self.n.add(f3, text='Shows')
                self.n.grid(row=0,column=0)

                # Create a database or connect to one
                conn = sqlite3.connect('MovieDesire.db')
                # Create cursor
                c = conn.cursor()

                # Query the db
                c.execute("SELECT *, oid FROM moviedesireDB WHERE watched_rank =" + str(get_rank_entry))
                records = c.fetchall() 
                #print(records)

                # Loop through results
                if len(records) == 0:
                    label_frame_A = tk.Frame(f1, width=550)
                    label_frame_A.pack()
                    print_titles_M = "No titles with selected rank"
                    print_titles_M_label = tk.Label(label_frame_A, text=print_titles_M, justify='left')
                    print_titles_M_label.pack()
                else:
                    # All
                    print_titles_A = ''
                    print_desirerank_A = ''
                    for record in records:
                        #imdb_rate = get_imdb_rating(str(record[0]))
                        print_titles_A += str(record[5]) + " : " + str(record[0]) + "\n"
                        print_desirerank_A += "Desire: " + str(record[2]) + " | Rank: " + str(record[1]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_A == '':
                        print_titles_A = "No titles with selected desire"
                    # frame in f1
                    label_frame_A = SFrame(f1, width=550)
                    label_frame_A.pack()
                    # info
                    print_titles_A_label = tk.Label(label_frame_A, text=print_titles_A, justify='left')
                    print_titles_A_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_A_label = tk.Label(label_frame_A, text=print_desirerank_A, justify='left')
                    print_desirerank_A_label.grid(row=1, column=1, padx=50, pady=40)

                    # Movies
                    print_titles_M = ''
                    print_desirerank_M = ''
                    for record in records:
                        if str(record[4]) == 'M':
                            print_titles_M += str(record[5]) + " : " + str(record[0]) + "\n"
                            print_desirerank_M += "Desire: " + str(record[2]) + " | Rank: " + str(record[1]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_M == '':
                        print_titles_M = "No movies with selected desire"
                    # frame in f2
                    label_frame_M = SFrame(f2, width=550)
                    label_frame_M.pack()
                    # info
                    print_titles_M_label = tk.Label(label_frame_M, text=print_titles_M, justify='left')
                    print_titles_M_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_M, justify='left')
                    print_desirerank_M_label.grid(row=1, column=1, padx=50, pady=40)

                    # Shows
                    print_titles_S = ''
                    print_desirerank_S = ''
                    for record in records:
                        if str(record[4]) == 'S':
                            print_titles_S += str(record[5]) + " : " + str(record[0]) + "\n"
                            print_desirerank_S += "Desire: " + str(record[2]) + " | Rank: " + str(record[1]) + " | IMDB: " + str(record[3]) + "\n"
                    if print_titles_S == '':
                        print_titles_S = "No shows with selected desire"
                    # frame in f3
                    label_frame_M = SFrame(f3, width=550)
                    label_frame_M.pack()
                    # info
                    print_titles_M_label = tk.Label(label_frame_M, text=print_titles_S, justify='left')
                    print_titles_M_label.grid(row=1, column=0, padx=30, pady=40)
                    print_desirerank_M_label = tk.Label(label_frame_M, text=print_desirerank_S, justify='left')
                    print_desirerank_M_label.grid(row=1, column=1, padx=50, pady=40)

                # Commit changes
                conn.commit()
                #Close connection
                conn.close()

                rank_entry.delete(0, 'end') # Clear entry box 


        ##### EDIT FRAME #####
        def _make_edit_frame():
            if edit_entry.get() != '':
                record_id = edit_entry.get()

                ### SUBMIT EDIT ###
                def update():
                    # Create a database or connect to one
                    conn = sqlite3.connect('MovieDesire.db')
                    # Create cursor
                    c = conn.cursor()

                    #record_id = edit_entry.get()

                    c.execute("""UPDATE moviedesireDB SET
                            movie_title = :movie,
                            movie_desire = :desire,
                            watched_rank = :rank
                            
                            WHERE oid = :oid""",
                            {
                                'movie': title_entry.get(),
                                'desire': desire_entry.get(),
                                'rank': rank_entry.get(),

                                'oid': record_id
                            })

                    # Commit changes
                    conn.commit()
                    #Close connection
                    conn.close()

                    title_entry.delete(0, 'end')
                    desire_entry.delete(0, 'end')
                    rank_entry.delete(0, 'end')

                    self._make_view_frame()
                
                ### DELETE ###
                def delete():
                    # Create a database or connect to one
                        conn = sqlite3.connect('MovieDesire.db')
                        # Create cursor
                        c = conn.cursor()

                        # Delete a record
                        c.execute("DELETE from moviedesireDB WHERE oid=" + record_id)

                        # Commit changes
                        conn.commit()
                        #Close connection
                        conn.close()

                        self._make_view_frame()


                self.gui_elements_remove(self.gui_elements)

                self.edit_frame = tk.Frame(self.main_Frame)
                self.edit_frame.pack(expand=True, fill='both')

                # Background Canvas
                self.Canvas1 = tk.Canvas(self.edit_frame)
                setheight = self.main_Frame.winfo_height() + 30
                self.Canvas1.config(bg="#203354", width = self.main_Frame.winfo_width(), height = setheight)
                self.Canvas1.pack(expand=True,fill='both')

                # Header
                self.headingFrame = tk.Frame(self.edit_frame,bg="#1c87e3",bd=5)
                self.headingFrame.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
                headingLabel = tk.Label(self.headingFrame, text="Edit Title", bg='black', fg='white', font=('Courier',15))
                headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
                self.labelFrame = tk.Frame(self.edit_frame,bg='black')
                self.labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)

                # Movie/Show Title
                title_label = tk.Label(self.labelFrame,text="Title : ", bg='black', fg='white')
                title_label.place(relx=0.05,rely=0.1, relheight=0.08)
                title_entry = tk.Entry(self.labelFrame)
                title_entry.place(relx=0.3,rely=0.1, relwidth=0.62, relheight=0.10)
                # Desire
                desire_label = tk.Label(self.labelFrame,text="Desire : ", bg='black', fg='white')
                desire_label.place(relx=0.05,rely=0.25, relheight=0.08)
                desire_entry = tk.Entry(self.labelFrame)
                desire_entry.place(relx=0.3,rely=0.25, relwidth=0.62, relheight=0.10)
                # Rank
                rank_label = tk.Label(self.labelFrame, text="Rank : ", bg='black', fg='white')
                rank_label.place(relx=0.05,rely=0.40, relheight=0.08)
                rank_entry = tk.Entry(self.labelFrame)
                rank_entry.place(relx=0.3,rely=0.40, relwidth=0.62, relheight=0.10)
                # create radio buttons for Movie or TV Show
                x_radio = tk.StringVar()
                radio_frame = ttk.Frame(self.labelFrame)
                radio_frame.place(relx=0.3, rely=0.55, relwidth=0.32, relheight=0.12)
                movie_radio = tk.Radiobutton(radio_frame, compound='left', text='M', font="none 10", variable=x_radio, value="M")
                movie_radio.grid(row=1, column=1)
                show_radio = tk.Radiobutton(radio_frame, compound='left', text='S', font="none 10", variable=x_radio, value="S")
                show_radio.grid(row=1, column=2)
                #Submit Button
                self.SubmitBtn = tk.Button(self,text="SUBMIT",bg='#d1ccc0', fg='black', command=update)
                self.SubmitBtn.place(relx=0.28,rely=0.65, relwidth=0.18,relheight=0.08)
                #Delete Button
                self.DeleteBtn = tk.Button(self, text="DELETE", bg='#f7f1e3', fg='black', command=delete)
                self.DeleteBtn.place(relx=0.53,rely=0.65, relwidth=0.18,relheight=0.08)
                #Quit Button
                self.quitBtn = tk.Button(self,text="Back",bg='#f7f1e3', fg='black', command = self._make_view_frame)
                self.quitBtn.place(relx=0.41,rely=0.75, relwidth=0.18,relheight=0.08)

                # Create a database or connect to one
                conn = sqlite3.connect('MovieDesire.db')
                # Create cursor
                c = conn.cursor()

                # Query the db
                c.execute("SELECT * FROM moviedesireDB WHERE oid =" + record_id)

                records = c.fetchall()

                for record in records:
                    title_entry.insert(0, record[0]),
                    desire_entry.insert(0,record[1]),
                    rank_entry.insert(0, record[2])
                    if record[4] == 'M':
                        movie_radio.invoke()
                    else: 
                        show_radio.invoke()
                
                # Commit changes
                conn.commit()
                #Close connection
                conn.close()

                self.gui_elements = [
                    self.edit_frame,
                    self.Canvas1,
                    self.headingFrame,
                    self.labelFrame,
                    self.SubmitBtn,
                    self.DeleteBtn,
                    self.quitBtn
                ]

        ########################
        show_lists()
        ### VIEW BUTTONS AND ENTRIES ###
        self.button_frame = tk.Frame(self.view_frame)
        self.button_frame.grid(row=1)
        highlow_button = tk.Button(self.button_frame, text="Desire High to Low", command=desire_highlow)
        highlow_button.grid(row=1, column=0)
        byrank_button = tk.Button(self.button_frame, text="Rank High to Low", command=rank_highlow)
        byrank_button.grid(row=2, column=0, ipadx=5)
        desire_entry_label = tk.Label(self.button_frame, text="Enter desire: ")
        desire_entry_label.grid(row=1, column=1, sticky='e')
        desire_entry = tk.Entry(self.button_frame, width=6)
        desire_entry.grid(row=1, column=2)
        bydesire_button = tk.Button(self.button_frame, text="Find Desire", command=bydesire)
        bydesire_button.grid(row=1, column=3)
        rank_entry_label = tk.Label(self.button_frame, text="Enter rank: ")
        rank_entry_label.grid(row=2, column=1, sticky='e')
        rank_entry = tk.Entry(self.button_frame, width=6)
        rank_entry.grid(row=2, column=2)
        byrank_button = tk.Button(self.button_frame, text="Find Rank", command=byrank)
        byrank_button.grid(row=2, column=3, ipadx=5)
        #refresh_btn = tk.Button(self.button_frame, text='Refresh')
        #refresh_btn.grid(row=3)
        button = tk.Button(self.button_frame, text="Main Menu")
        button.bind('<Button-1>', self.back_to_main)
        button.grid(row=4, pady=10)

        edit_entry = tk.Entry(self.button_frame, width=6)
        edit_entry.grid(row=4, column =3)
        edit_button = tk.Button(self.button_frame, text='Edit', command=_make_edit_frame)
        edit_button.grid(row=4,column=4)

        ### ENTER key ###
        def enter_bydesire(event):
            bydesire()
        desire_entry.bind('<Return>', enter_bydesire)

        def enter_byrank(event):
            byrank()
        rank_entry.bind('<Return>', enter_byrank)

        def enter_make_edit(event):
            _make_edit_frame()
        edit_entry.bind('<Return>', enter_make_edit)

        
        self.frame_controller = 1

        self.gui_elements = [
            self.view_frame,
            self.n,
            self.button_frame
        ]
###############

##### ADD FRAME #####
    def _make_add_frame(self):
        self.gui_elements_remove(self.gui_elements)

        self.add_frame = tk.Frame(self.main_Frame)
        self.add_frame.pack(expand=True, fill='both')

        def get_imdb_rating(record_name):
            moviesDB = imdb.IMDb()
            movies = moviesDB.search_movie(record_name)

            id = movies[0].getID()
            movie = moviesDB.get_movie(id)

            # title_imdb = movie['title']
            # year_imdb = movie['year']
            rating_imdb = movie['rating']
            # directors_imdb = movie['directors']
            # casting_imdb = movie['cast']

            return rating_imdb
        
        def submit():
            if title_entry.get() == '':
                no_entry_label = tk.Label(self.add_frame, text='No movie entered', fg='red')
                no_entry_label.place(relx=0.45, rely=0.80)
            else:
                try:
                    imdb_rating_cont = get_imdb_rating(str(title_entry.get()))
                except Exception as e:
                    imdb_rating_cont = 0.0

                # Create a database or connect to one
                conn = sqlite3.connect('MovieDesire.db')
                # Create cursor
                c = conn.cursor()

                # Insert into table
                c.execute("INSERT INTO moviedesireDB (movie_title, movie_desire, watched_rank, imdb_rating, MorTV) VALUES (:title_entry, :m_desire, :w_rank, :imdb_rating, :MorTV)",
                        {
                            'title_entry': title_entry.get(),
                            'm_desire': desire_entry.get(),
                            'w_rank' : '',
                            'imdb_rating' : imdb_rating_cont,
                            'MorTV' : x_radio.get()
                        })

                # Commit changes
                conn.commit()
                # Close Connection
                conn.close()

                # Clear the text boxes
                title_entry.delete(0, 'end')
                desire_entry.delete(0, 'end')
                
                x_radio.set(None)

        self.Canvas1 = tk.Canvas(self.add_frame)
        self.Canvas1.config(bg="#00b8ff", width = self.main_Frame.winfo_width(), height = self.main_Frame.winfo_height())
        self.Canvas1.pack(expand=True,fill='both')

        # Header and Label Frames
        self.headingFrame1 = tk.Frame(self.add_frame,bg="#0000a5",bd=5)
        self.headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        headingLabel = tk.Label(self.headingFrame1, text="Add Titles", bg='black', fg='white', font=('Courier',15))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

        self.labelFrame = tk.Frame(self.add_frame,bg='black')
        self.labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)
        # Movie/Show Title
        title_label = tk.Label(self.labelFrame,text="Title : ", bg='black', fg='white')
        title_label.place(relx=0.05,rely=0.2, relheight=0.08)
        title_entry = tk.Entry(self.labelFrame)
        title_entry.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.10)
        # Desire
        desire_label = tk.Label(self.labelFrame,text="Desire : ", bg='black', fg='white')
        desire_label.place(relx=0.05,rely=0.35, relheight=0.08)
        desire_entry = tk.Entry(self.labelFrame)
        desire_entry.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.10)
        # create radio buttons for Movie or TV Show
        x_radio = tk.StringVar()
        radio_frame = ttk.Frame(self.labelFrame)
        radio_frame.place(relx=0.3, rely=0.5, relwidth=0.32, relheight=0.12)
        movie_radio = tk.Radiobutton(radio_frame, compound='left', text='M', font="none 10", variable=x_radio, value="M")
        movie_radio.grid(row=1, column=1)
        show_radio = tk.Radiobutton(radio_frame, compound='left', text='S', font="none 10", variable=x_radio, value="S")
        show_radio.grid(row=1, column=2)
        #Submit Button
        self.SubmitBtn = tk.Button(self,text="SUBMIT",bg='#d1ccc0', fg='black', command=submit)
        self.SubmitBtn.place(relx=0.28,rely=0.70, relwidth=0.18,relheight=0.08)
        #Quit Button
        self.quitBtn = tk.Button(self,text="Back",bg='#f7f1e3', fg='black')
        self.quitBtn.bind('<Button-1>', self.back_to_main)
        self.quitBtn.place(relx=0.53,rely=0.70, relwidth=0.18,relheight=0.08)

        self.frame_controller = 2

        self.gui_elements = [
            self.add_frame,
            self.Canvas1,
            self.headingFrame1,
            self.labelFrame,
            self.SubmitBtn,
            self.quitBtn
        ]


##### BACK #####
    def back_to_main(self, event):
        if self.frame_controller == 1 or self.frame_controller == 2 or self.frame_controller == 3:
            self.gui_elements_remove(self.gui_elements)
        else:
            pass
        self._make_start_frame()
    

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()
    


    def _center_window(self):
        self.update()
        
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = (self.winfo_screenwidth() - width) // 2
        y_offset = 0

        self.geometry(
            f'{width}x{height}+{x_offset}+{y_offset}'
        )


## Added controller to same file
class Controller:
    def __init__(self):
        self.view = View(self)

    
    def main(self): 
        self.view.main()

if __name__ == '__main__':
    W2W = Controller()
    W2W.main() 
