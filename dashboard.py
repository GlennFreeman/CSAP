import sqlite3
import dearpygui.dearpygui as dpg

def stringify_tuple(x):
    return str(x)[2:-3].title()

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    dpg.add_tab(label=stringify_tuple(user_data), parent="tab bar")


con = sqlite3.connect("app.db")
cur = con.cursor()
sql = "SELECT topic FROM scores ORDER BY score DESC"
res = cur.execute(sql)
topics = res.fetchall()

dpg.create_context()

with dpg.window(tag="Primary Window"):
    dpg.add_tab_bar(tag="tab bar")
    with dpg.tab(label="main", parent="tab bar"):          
            buttons = []
            longest = 0
            for x in range(10):
                label = stringify_tuple(topics[x])
                buttons.append(dpg.add_button(label=label, user_data=topics[x], callback=button_callback))

dpg.create_viewport(title="CSAP")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()   