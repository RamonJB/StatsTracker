import datetime
from dearpygui.core import *
from dearpygui.simple import *
from gamestats import GameStats
from dbhelper import DBHelper


# Shows the info entered in the text boxes when the Retrieve button is pressed.
def retrieve_callback(sender, callback):
    show_logger()
    log_info(get_value("Date"))
    log_info(get_value("Game"))
    log_info(get_value("Game Type"))
    log_info(get_value("Variant"))
    log_info(get_value("Win or Loss"))
    log_info(get_value("Frags"))
    log_info(get_value("Deaths"))
    log_info(get_value("Assists"))


# Converts radio button values to game names.
def convert_game_value(temp_game):
    if temp_game == 0:
        temp_game = "Reach"
    elif temp_game == 1:
        temp_game = "CE"
    elif temp_game == 2:
        temp_game = "H2C"
    elif temp_game == 3:
        temp_game = "H2A"
    elif temp_game == 4:
        temp_game = "H3"
    elif temp_game == 5:
        temp_game = "H4"
    return temp_game


# Converts radio button values to game types.
def convert_game_type_value(temp_game_type):
    if temp_game_type == 0:
        temp_game_type = "8v8"
    elif temp_game_type == 1:
        temp_game_type = "4v4"
    elif temp_game_type == 2:
        temp_game_type = "FFA"
    return temp_game_type


# Converts radio button values to game results.
def convert_result(temp_result):
    if temp_result == 0:
        temp_result = "Win"
    elif temp_result == 1:
        temp_result = "Loss"
    elif temp_result == 2:
        temp_result = "Tie"
    return temp_result

# Returns a GameStats object containing the current values in the inputs.
def get_inputs():
    temp_date = get_value("Date")

     # ["Reach", "CE", "H2C", "H2A", "H3", "H4"]
    temp_game = convert_game_value(get_value("Game"))

    # ["8v8", "4v4", "FFA"]
    temp_game_type = convert_game_type_value(get_value("Game Type"))

    temp_variant = get_value("Variant")

    # ["Win", "Loss", "Tie"]
    temp_result = convert_result(get_value("Win or Loss"))

    temp_frags = get_value("Frags")
    temp_deaths = get_value("Deaths")
    temp_assists = get_value("Assists")

    # Checking if the user went flawless.
    if temp_deaths == 0:
        temp_fd_ratio = round(temp_frags / 1, 2)
    else:
        temp_fd_ratio = round(temp_frags / temp_deaths, 2)

    values = GameStats(temp_date, temp_game, temp_game_type, temp_variant, temp_result, temp_frags, temp_deaths, temp_assists, temp_fd_ratio)

    return values


# Gets the values from the fields in the Edit Tab.
def get_edits():
    temp_date = get_value("Edit Date")

     # ["Reach", "CE", "H2C", "H2A", "H3", "H4"]
    temp_game = convert_game_value(get_value("Edit Game"))

    # ["8v8", "4v4", "FFA"]
    temp_game_type = convert_game_type_value(get_value("Edit Game Type"))

    temp_variant = get_value("Edit Variant")

    # ["Win", "Loss", "Tie"]
    temp_result = convert_result(get_value("Edit Result"))

    temp_frags = get_value("Edit Frags")
    temp_deaths = get_value("Edit Deaths")
    temp_assists = get_value("Edit Assists")

    # Checking if the user went flawless.
    if temp_deaths == 0:
        temp_fd_ratio = round(temp_frags / 1, 2)
    else:
        temp_fd_ratio = round(temp_frags / temp_deaths, 2)

    values = GameStats(temp_date, temp_game, temp_game_type, temp_variant, temp_result, temp_frags, temp_deaths, temp_assists, temp_fd_ratio)

    return values


# Adds the inputted stats into the database.
def save_stats(sender, callback):
    values = get_inputs()

    # Adding the values to the database.
    db.insert_stats(values)

    reset_inputs()

    # Update the rest of the app with the newly recorded game.
    clear_table('All Games')
    clear_plot('Frag-Death-Assist Graph')
    clear_plot('Frag-Death Ratio Graph')

    populate_all_games_table()
    fda_graph()
    fdr_graph()


# Used to save the edits when the Save Edits button is pressed in the Edit Tab.
def save_edits(sender, callback):
    values = get_edits()

    # Update the DB
    db.update_stats(values, get_value("ID"))

    # Reset the edit inputs
    reset_edit_inputs()

    # Update the rest of the app with the edited game.
    clear_table('All Games')
    clear_plot('Frag-Death-Assist Graph')
    clear_plot('Frag-Death Ratio Graph')

    populate_all_games_table()
    fda_graph()
    fdr_graph()


# Used to retrieve a game's stats which populates the fields in the Edit Tab.
def retrieve_game(sender, callback):
    id = get_value("ID")
    temp_game = db.get_stats_by_id(id)

    game_edit = -1
    temp = temp_game[2]
    if temp == "Reach":
        game_edit = 0
    elif temp == "CE":
        game_edit = 1
    elif temp == "H2C":
        game_edit = 2
    elif temp == "H2A":
        game_edit = 3
    elif temp == "H3":
        game_edit = 4
    elif temp == "H4":
        game_edit = 5

    game_type_edit = -1
    temp = temp_game[3]
    if temp == "8v8":
        game_type_edit = 0
    elif temp == "4v4":
        game_type_edit = 1
    elif temp == "FFA":
        game_type_edit = 2

    game_result = -1
    temp = temp_game[5]
    if temp == "Win":
        game_result = 0
    elif temp == "Loss":
        game_result = 1
    elif temp == "Tie":
        game_result = 2

    set_value('Edit Date', temp_game[1])
    set_value('Edit Game', game_edit)
    set_value('Edit Game Type', game_type_edit)
    set_value('Edit Variant', temp_game[4])
    set_value('Edit Result', game_result)
    set_value('Edit Frags', temp_game[6])
    set_value('Edit Deaths', temp_game[7])
    set_value('Edit Assists', temp_game[8])


# Clears the inputs whenever a new game is added or the Clear button is pressed.
def reset_inputs():
    set_value('Game', 0)
    set_value('Game Type', 0)
    set_value('Variant', '') 
    set_value('Win or Loss', 0)
    set_value('Frags', 0)
    set_value('Deaths', 0)
    set_value('Assists', 0)


# Clears the edit inputs whenever a game is edited.
def reset_edit_inputs():
    set_value('ID', 0)
    set_value('Edit Date', '')
    set_value('Edit Game', 0)
    set_value('Edit Game Type', 0)
    set_value('Edit Variant', '') 
    set_value('Edit Result', 0)
    set_value('Edit Frags', 0)
    set_value('Edit Deaths', 0)
    set_value('Edit Assists', 0)


def get_current_date():
    x = datetime.datetime.now()
    return x.strftime("%x")


# Populates the Full Stats Table.
def populate_all_games_table():
    games = db.get_all_stats()

    # For printing most recent games first.
    for i in reversed(range(len(games))):
        add_row('All Games', [games[i][0], games[i][1], games[i][2], games[i][3], games[i][4], games[i][5], games[i][6], games[i][7], games[i][8], games[i][9]])


# Line graph that displays frags-deaths-assists.
def fda_graph():
    games = db.get_all_stats()

    # X-axis is the Game ID.
    data_x = []

    # Y-axis is the amount of frags/deaths/assists.
    data_frags = []
    data_deaths = []
    data_assists = []

    # Loop through all the games and add each respective stat to their respective array.
    index = 0
    for game in games:
        data_x.append(games[index][0])
        data_frags.append(games[index][6])
        data_deaths.append(games[index][7])
        data_assists.append(games[index][8])
        index += 1

    # Plot the lines on the graph.
    add_line_series("Frag-Death-Assist Graph", "Frags", data_x, data_frags, weight=2)
    add_line_series("Frag-Death-Assist Graph", "Deaths", data_x, data_deaths, weight=2)
    add_line_series("Frag-Death-Assist Graph", "Assists", data_x, data_assists, weight=2)

    # Plot the specific points on the graph.
    add_scatter_series("Frag-Death-Assist Graph", "Frags", data_x, data_frags, weight=2)
    add_scatter_series("Frag-Death-Assist Graph", "Deaths", data_x, data_deaths, weight=2)
    add_scatter_series("Frag-Death-Assist Graph", "Assists", data_x, data_assists, weight=2)


# Line graph that displays the frag/death ratio.
def fdr_graph():
    games = db.get_all_stats()

    data_fdr = []
    data_x = []

    index = 0
    for game in games:
        data_x.append(games[index][0])
        data_fdr.append(games[index][9])
        index += 1

    add_line_series("Frag-Death Ratio Graph", "Frag/Death Ratio", data_x, data_fdr, weight=2)

    add_scatter_series("Frag-Death Ratio Graph", "Frag/Death Ratio", data_x, data_fdr, weight=2)


# Setup the GUI.
set_main_window_size(1080, 720)
set_main_window_title("Stats Tracker")
with window("Main Window"):
    with tab_bar("Main Bar"):

        with tab("Input Stats"):
            add_spacing(count=2)
            add_text("Help keep track of your game stats using this tool!", bullet=True)
            add_text("Press the 'Save Stats' button to save the input values.", wrap=500, bullet=True)
            add_text("Note: An example of a Variant is Slayer, CTF, etc.", bullet=True)
            add_spacing(count=3)

            current_date = get_current_date()
            add_input_text("Date", readonly=True, default_value=current_date)
            add_spacing(count=3)

            add_text("Select the Halo game that was played:")
            add_radio_button("Game", items=["Reach", "CE", "H2C", "H2A", "H3", "H4"])
            add_spacing(count=3)

            add_text("Select the game type:")
            add_radio_button("Game Type", items=["8v8", "4v4", "FFA"])
            add_spacing(count=3)

            add_input_text("Variant")
            add_spacing(count=3)

            add_text("Select the result of the game:")
            add_radio_button("Win or Loss", items=["Win", "Loss", "Tie"])
            add_spacing(count=3)

            add_input_int("Frags")
            add_input_int("Deaths")
            add_input_int("Assists")
            add_spacing(count=3)

            # For info-retrieval/debugging purposes.
            # add_button("Retrieve", callback=retrieve_callback)

            add_button("Save Stats", callback=save_stats)
            add_spacing(count=5)

        with tab("Full Stats Table"):
            add_spacing(count=2)
            add_text("All recorded games will appear here in this table.", bullet=True)
            add_text("Most recently added games will appear at the top of this table.", bullet=True)
            add_spacing(count=3)
            # Delete button
            # Edit button
            add_table('All Games', ['Game ID', 'Date', 'Game', 'Game Type', 'Variant', 'W|L', 'Frags', 'Deaths', 'Assists', 'F/D'], height=500)

        with tab("FDA Graph"):
            add_text("This graph displays the frags, deaths, and assists from each game. Chronological order.", bullet=True)
            add_text("Each line can be enabled/disabled by pressing on the line's respective square in the graph key.", bullet=True)
            add_spacing(count=5)
            add_plot("Frag-Death-Assist Graph", height=-1, scale_min=0, x_axis_name="Game ID", y_axis_name="Amount")

        with tab("FDR Graph"):
            add_text("This graph displays the frag/death ratio from each game.", bullet=True)
            add_spacing(count=5)
            add_plot("Frag-Death Ratio Graph", height=-1, x_axis_name="Game ID", y_axis_name="Ratio")

        with tab("Edit Tab"):
            add_spacing(count=2)
            add_text("Enter the ID of the game you'd like to edit:", bullet=True)
            add_input_int("ID")
            add_button("Retrieve Game", callback=retrieve_game)
            add_spacing(count=5)

            add_input_text("Edit Date")
            add_spacing(count=3)

            add_text("Edit the Halo game that was played:")
            add_radio_button("Edit Game", items=["Reach", "CE", "H2C", "H2A", "H3", "H4"])
            add_spacing(count=3)

            add_text("Edit the game type:")
            add_radio_button("Edit Game Type", items=["8v8", "4v4", "FFA"])
            add_spacing(count=3)

            add_input_text("Edit Variant")
            add_spacing(count=3)

            add_text("Edit the result of the game:")
            add_radio_button("Edit Result", items=["Win", "Loss", "Tie"])
            add_spacing(count=3)

            add_input_int("Edit Frags")
            add_input_int("Edit Deaths")
            add_input_int("Edit Assists")
            add_spacing(count=3)

            add_button("Save Edits", callback=save_edits)



### "Main" ###

# Setup the DB.
db = DBHelper()
db.create_table()

# Populate the table and graphs.
populate_all_games_table()
fda_graph()
fdr_graph()

start_dearpygui(primary_window="Main Window")