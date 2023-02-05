import sqlite3
import arcade
import arcade.gui
from alien_game import *

# This was for passing the leaderboard, but I couldn't get it all to work.
rows_pasted = []

con = sqlite3.connect('leaderboard_score.db')

cur = con.cursor()


#cur.execute('''CREATE TABLE leaderboard (ID INTEGER PRIMARY KEY AUTOINCREMENT, level real, initials real)''')

# Allows player to put in their score.

def input_player_info(player_score):
    con = sqlite3.connect('leaderboard_score.db')

    cur = con.cursor()

    num_rows = cur.execute(('select * from leaderboard'))
    length_rows = len(num_rows.fetchall())

    if length_rows != 0:
        score_standard = cur.execute('select MIN(level) from leaderboard')
        on_board = score_standard.fetchall()

    # If the leaderboard isn't full then it will always put one in otherwise it has to beat a high score.
    if length_rows < 10 or player_score > on_board[0][0]:

        initials = input("Insert initials: ")

        info_list = [(player_score), (initials)]

        cur.execute("INSERT INTO leaderboard (level, initials) VALUES (?,?)", info_list)

    
    #This needs to be redone so that it can have the new number of rows.
    num_rows = cur.execute(('select * from leaderboard'))
    length_rows = len(num_rows.fetchall())


    count = 0
    # This deletes the lowest score on the leaderboard when a higher one gets put in.
    if length_rows > 10:
        for row in cur.execute('select * from leaderboard order by level DESC, ID ASC'):
            count += 1
            if count > 10:

                row_list = list(row)

                row_id = [str(row_list[0])]
 
                cur.execute('DELETE FROM leaderboard WHERE ID == ?', row_id)

    con.commit()
    for row in cur.execute('select * from leaderboard order by level DESC, ID ASC'):
        print(row)
        rows_pasted.append(row)
   

    con.close()

    return rows_pasted

# This allows for modifying the leaderboards' initials.

def modify_leaderboard():
    con = sqlite3.connect('leaderboard_score.db')

    cur = con.cursor()

    update_y_n = input("Do you want to change the value of the leaderboard (y) (n): ")

    if update_y_n == 'y':
        ID = input('Which row do you wish to change: ')
        initials = input('What is the new initials: ')

        update_leaderboard = [(initials), (ID)]

        cur.execute('''UPDATE leaderboard SET initials = ? WHERE ID = ?''', update_leaderboard)

        con.commit()

        print('New Leaderboard: ')
        for row in cur.execute('select * from leaderboard order by level DESC, ID ASC'):
            print(row)

        con.close()

    else:
        pass




con.commit()

con.close()