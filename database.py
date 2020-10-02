from tkinter import *
import sqlite3


root = Tk()
root.title('My Movie Desire')
#root.geometry("600x400")


# Databases

'''
# Create a database or connect to one
conn = sqlite3.connect('MovieDesire.db')
# Create cursor
c = conn.cursor()


# Commit changes
conn.commit()
#Close connection
conn.close()
'''


# Create a database or connect to one
conn = sqlite3.connect('MovieDesire.db')


# Create cursor
c = conn.cursor()


# Create table
# only have to do once 
'''
c.execute("""CREATE TABLE moviedesireDB (
        movie_title text,
        movie_desire integer,
        watched_rank integer
        )""")
'''


# Create edit function to update record
def update():
    # Create a database or connect to one
    conn = sqlite3.connect('MovieDesire.db')
    # Create cursor
    c = conn.cursor()

    record_id = delete_box.get()

    c.execute("""UPDATE moviedesireDB SET
            movie_title = :movie,
            movie_desire = :desire,
            watched_rank = :rank
    
            WHERE oid = :oid""",
            {
                'movie': m_title_editor.get(),
                'desire': m_desire_editor.get(),
                'rank': w_rank_editor.get(),

                'oid': record_id
            })

    # Commit changes
    conn.commit()
    #Close connection
    conn.close()

    delete_box.delete(0, END)
    editor.destroy()



def edit():
    record_id = delete_box.get()
    if record_id == '':
        delete_label1 = Label(root, text= "No ID selected from list to update", fg='red')
        delete_label1.grid(row= 12, column=1, sticky=W)
    else:
        global editor
        editor = Tk()
        editor.title('Update Movie')
        editor.geometry("400x250")

        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        # Query the db
        c.execute("SELECT * FROM moviedesireDB WHERE oid =" + record_id)

        records = c.fetchall()

        # Create global variables for text box names
        global m_title_editor
        global m_desire_editor
        global w_rank_editor

        # Create text boxes
        m_title_editor = Entry(editor, width=30)
        m_title_editor.grid(row=0, column=1, padx=20, pady=(10,0))
        m_desire_editor = Entry(editor, width=30)
        m_desire_editor.grid(row=1, column=1, padx=20)
        w_rank_editor = Entry(editor, width=30)
        w_rank_editor.grid(row=2, column=1, padx=20)

        # Create text box labels
        m_title_label = Label(editor, text="Movie Title")
        m_title_label.grid(row=0, column=0, pady=(10,0))
        m_desire_label = Label(editor, text="Movie Desire")
        m_desire_label.grid(row=1, column=0)
        w_rank_label = Label(editor, text="Watched Rank")
        w_rank_label.grid(row=2, column=0)



        # Loop through results
        for record in records:
            m_title_editor.insert(0, record[0])
            m_desire_editor.insert(0, record[1])
            w_rank_editor.insert(0, record[2])

        # Create save button
        save_btn = Button(editor, text="Save", command=update)
        save_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=145)

# Create function to delete a record
def delete():
    record_id = delete_box.get()
    if record_id == '':
        delete_label1 = Label(root, text= "No ID selected from list to delete", fg='red')
        delete_label1.grid(row= 12, column=1, sticky=W)

    else:
        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        # Delete a record
        c.execute("DELETE from moviedesireDB WHERE oid=" + record_id)


        deleted_label = Label(root, text= "Movie with ID: " + record_id + " deleted from list")
        deleted_label.grid(row= 12, column=1, sticky=W)

        # Commit changes
        conn.commit()
        #Close connection
        conn.close()

        delete_box.delete(0, END)

# Create submit function for db
def submit():
    if m_title.get() == '':
        label1 = Label(root, text= "No movie entered", fg='red')
        label1.grid(row= 6, column=1, ipadx=5, sticky=W)
    else:
        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        # Insert into table
        c.execute("INSERT INTO moviedesireDB (movie_title, movie_desire, watched_rank) VALUES (:m_title, :m_desire, :w_rank)",
                {
                    'm_title': m_title.get(),
                    'm_desire': m_desire.get(),
                    'w_rank' : ''
                })


        # Commit changes
        conn.commit()
        # Close Connection
        conn.close()

        # Clear the text boxes
        m_title.delete(0, END)
        m_desire.delete(0, END)


# Create query function
def query():
    if 'frame1' in locals():
            frame1.destroy()
    frame1 = Frame(root)
    frame1.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=50, sticky=NW)
    # Create a database or connect to one
    conn = sqlite3.connect('MovieDesire.db')
    # Create cursor
    c = conn.cursor()

    # Query the db
    c.execute("SELECT *, oid FROM moviedesireDB")
    records = c.fetchall() # fetchone, fetchmany(50)
    #print(records)

    # Loop through results
    print_titles = ''
    print_desirerank = ''
    for record in records:
        #print_records += str(record[0]) + " | " + " Desire: " + str(record[1]) + "\t" + " My Score: " +  str(record[2]) + "\t" + " ID: " + str(record[3]) + "\n"
        print_titles += str(record[0]) + "\n"
        print_desirerank += "Desire: " + str(record[1]) + "  | My Rank: " + str(record[2]) + "  | ID: " + str(record[3]) + "\n"

    
    def highlow():
        if 'frame1' in locals():
            frame1.destroy()
        frame1 = Frame(root)
        frame1.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=50, sticky=W)
        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT *, oid FROM moviedesireDB ORDER BY movie_desire DESC")
        highlow_var = c.fetchall()

        print_titlesHL = ''
        print_desirerankHL = ''
        for x in highlow_var:
            print_titlesHL += str(x[0]) + "\n"
            print_desirerankHL += "Desire: " + str(x[1]) + " | My Rank: " + str(x[2]) + " | ID: " + str(x[3]) + "\n"
        print_titlesHL_label = Label(frame1, text=print_titlesHL, justify=LEFT, anchor=NW)
        print_titlesHL_label.grid(row=1, column=1, padx=20, pady=10)
        print_desirerankHL_label = Label(frame1, text=print_desirerankHL, justify=LEFT, anchor=NW)
        print_desirerankHL_label.grid(row=1, column=2, ipadx=20)

        # Commit changes
        conn.commit()
        #Close connection
        conn.close()

    def bydesire():
        if 'frame1' in locals():
            frame1.destroy()
        frame1 = Frame(root)
        frame1.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=50, sticky=NW)
        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        get_desire_entry = desire_entry.get()
        if get_desire_entry != '':
        
            c.execute("SELECT *, oid FROM moviedesireDB WHERE movie_desire =" + str(get_desire_entry))
            bydesire_var = c.fetchall()

            print_bydesire_titles =''
            print_bydesire_info=''
            
            if len(bydesire_var) == 0:
                print_bydesire_titles += "No movies with selected desire"
                print_bydesire_info += ""
            else:
                for i in bydesire_var:
                    if i[0] == '':
                        print_bydesire_titles += "No movies with selected desire"
                    else:
                        print_bydesire_titles += str(i[0]) + "\n"
                        print_bydesire_info += "Desire: " + str(i[1]) + " | Rank: " + str(i[2]) + " | ID: " + str(i[3]) + "\n"
        else:
            print_bydesire_titles = "No desire entered"

        print_bydesire_titles_label = Label(frame1, text=print_bydesire_titles, justify=LEFT, anchor=NW)
        print_bydesire_titles_label.grid(row=1, column=0, padx=30, pady=40)
        print_bydesire_info_label = Label(frame1, text=print_bydesire_info, justify=LEFT, anchor=NW)
        print_bydesire_info_label.grid(row=1, column=1, padx=30, pady=40)

        # Commit changes
        conn.commit()
        #Close connection
        conn.close()
    
    def rank_highlow():
        if 'frame1' in locals():
            frame1.destroy()
        frame1 = Frame(root)
        frame1.grid(row=1, column=0, columnspan=2, ipadx=30, ipady=50, sticky=NW)

        # Create a database or connect to one
        conn = sqlite3.connect('MovieDesire.db')
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT *, oid FROM moviedesireDB ORDER BY watched_rank DESC")
        rank_highlow_var = c.fetchall()
        print_titlesrankHL = ''
        print_rankHL = ''
        for x in rank_highlow_var:   
            if str(x[2]) != '':
                print_titlesrankHL += str(x[0]) + "\n"
                print_rankHL += "Rank: " + str(x[2]) + " | Desire: " + str(x[1]) + " | ID: " + str(x[3]) + "\n"
        print_titlesrankHL_label = Label(frame1, text=print_titlesrankHL, justify=LEFT, anchor=NW)
        print_titlesrankHL_label.grid(row=1, column=0, padx=30, pady=30)
        print_rankHL_label = Label(frame1, text=print_rankHL, justify=LEFT, anchor=W)
        print_rankHL_label.grid(row=1, column=1, pady=30)


        # Commit changes
        conn.commit()
        #Close connection
        conn.close()

    frame1 = Frame(root)
    frame1.grid(row=1, column=0, columnspan=2, padx=20, sticky=NW)

    print_titles_label = Label(frame1, text=print_titles, justify=LEFT)
    print_titles_label.grid(row=1, column=0)
    print_desirerank_label = Label(frame1, text=print_desirerank, justify=LEFT)
    print_desirerank_label.grid(row=1, column=1, ipadx=35)
    
    button_frame = Frame(root, bd=2)
    button_frame.grid(row=1, column=3, sticky=NW)

    highlow_button = Button(button_frame, text="Desire High to Low", command=highlow)
    highlow_button.grid(row=1, column=1, padx=(0,10), pady=10, sticky=NW )
    byrank_button = Button(button_frame, text="Rank High to Low", command=rank_highlow)
    byrank_button.grid(row=2, column=1, padx=(0,10), pady=2, sticky=W)
    desire_entry_label = Label(button_frame, text="Enter desire: ")
    desire_entry_label.grid(row=3, column=1, sticky=NW)
    desire_entry = Entry(button_frame, width=6)
    desire_entry.grid(row=4, column=1, sticky=W)
    bydesire_button = Button(button_frame, text="View By Desire", command=bydesire)
    bydesire_button.grid(row=5, column=1, ipadx=7, pady=2, sticky=W)
    

    ### ENTER key ###
    def enter_bydesire(event):
        bydesire()
    desire_entry.bind('<Return>', enter_bydesire)

    # Commit changes
    conn.commit()
    #Close connection
    conn.close()


### ####

# Create text boxes
m_title = Entry(root, width=30)
m_title.grid(row=3, column=1, padx=20, pady=(10,0))
m_desire = Entry(root, width=30)
m_desire.grid(row=4, column=1, padx=20)
#w_rank = Entry(root, width=30)
#w_rank.grid(row=5, column=1, padx=20)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1)

# Create text box labels
m_title_label = Label(root, text="Movie Title")
#m_title_label.grid(row=0, column=0, pady=(10,0))
m_title_label.grid(row=3, column=0, pady=(10,0))
m_desire_label = Label(root, text="Movie Desire")
#m_desire_label.grid(row=1, column=0)
m_desire_label.grid(row=4, column=0)
delete_box_label = Label(root, text="Select ID")
#delete_box_label.grid(row=5, column=0, pady=(0,5))
delete_box_label.grid(row=9, column=0, pady=(0,5))

# Create submit button
submit_btn = Button(root, text="Add Movie to Database", command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=110)


# Create a Query Button
query_btn = Button(root, text="Show My List", command=query)
#query_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=137)
query_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipadx=137)


# Create an Update Button
update_btn = Button(root, text="Edit Desire/Rank", command=edit)
update_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=130)


# Create a Delete Button
delete_btn = Button(root, text="Delete Movie", command=delete)
delete_btn.grid(row=11, column=0, columnspan=2, padx=10, pady=10, ipadx=137)


########
### ENTER key ###
def enter_movie_title(event):
    submit()
m_title.bind('<Return>', enter_movie_title)

def enter_movie_desire(event):
    submit()
m_desire.bind('<Return>', enter_movie_desire)




# Commit changes
conn.commit()


# Close Connection
conn.close()

root.mainloop()