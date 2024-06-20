import sqlite3
import dearpygui.dearpygui as dpg

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    dpg.add_tab(label=(user_data[0].title()), parent="tab bar", closable=True)


con = sqlite3.connect("app.db")
cur = con.cursor()
sql = "SELECT topic, score FROM scores ORDER BY score DESC"
res = cur.execute(sql)
topics = res.fetchall()

dpg.create_context()

with dpg.window(tag="Primary Window"):
    with dpg.tab_bar(tag="tab bar", reorderable=True):
        with dpg.tab(label="main", parent="tab bar", closable=False, order_mode=dpg.mvTabOrder_Leading):          
                buttons = []
                longest = 0
                for x in range(10):
                    label = f'{x+1:>2}. {topics[x][0].title():<30}{topics[x][1]:>5.2f}'
                    buttons.append(dpg.add_button(label=label, user_data=topics[x], callback=button_callback))

dpg.create_viewport(title="CSAP")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()   