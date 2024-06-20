import sqlite3
import dearpygui.dearpygui as dpg

def button_callback(sender, app_data, user_data):
    dpg.add_tab(label=(user_data[0].title()), parent="tab bar", closable=True, tag=user_data[0])
    dpg.set_value("tab bar", user_data[0])


con = sqlite3.connect("app.db")
cur = con.cursor()
sql = "SELECT topic, score FROM scores ORDER BY score DESC"
res = cur.execute(sql)
topics = res.fetchall()

dpg.create_context()

with dpg.window(tag="Primary Window"):
    with dpg.tab_bar(tag="tab bar", reorderable=True):
        with dpg.tab(label="main", parent="tab bar", closable=False, order_mode=dpg.mvTabOrder_Leading):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(tag="list window"):
                        for x in range(20):
                            label = f'{x+1:>2}. {topics[x][0].title():<30}{topics[x][1]:>5.2f}'
                            dpg.add_button(label=label, user_data=topics[x], callback=button_callback)
                    with dpg.child_window(tag="right half"):
                        with dpg.table(header_row=False):
                            dpg.add_table_column()
                            with dpg.table_row():
                                with dpg.child_window(height=300):
                                    ...
                                    # dpg.plot()
                            with dpg.table_row():
                                with dpg.child_window():
                                    dpg.add_button(label="test")

dpg.create_viewport(title="CSAP")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()   