import sqlite3
import dearpygui.dearpygui as dpg

MAX_ITEMS = 50

def button_callback(sender, app_data, user_data):
    dpg.add_tab(label=(user_data[0].title()), parent="tab bar", closable=True, tag=user_data[0])
    dpg.set_value("tab bar", user_data[0])


def show_info(title, message, selection_callback):

    # guarantee these commands happen in the same frame
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label=title, modal=True, no_close=True, show=False, tag="modal") as modal_id:
            dpg.add_text(message)
            dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=selection_callback)


    # guarantee these commands happen in another frame
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])

    # skips the frame where the modal shows up in the top left
    dpg.split_frame()
    dpg.configure_item(item="modal", show=True)


def on_selection(sender, unused, user_data):

    if user_data[1]:
        dpg.set_clipboard_text("testing")

    # delete window
    dpg.delete_item(user_data[0])


con = sqlite3.connect("app.db")
cur = con.cursor()
sql = "SELECT topic, score FROM scores ORDER BY score DESC"
res = cur.execute(sql)
topics = res.fetchall()

dpg.create_context()
dpg.create_viewport(title="CSAP")

with dpg.window(tag="Primary Window", no_scrollbar=True):
    with dpg.tab_bar(tag="tab bar", reorderable=True):
        with dpg.tab(label="Home", parent="tab bar", closable=False, order_mode=dpg.mvTabOrder_Leading):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=dpg.get_viewport_width()//2, height=dpg.get_viewport_height()-47):
                    dpg.add_input_text(hint="Enter propt to generate product idea")
                    with dpg.table(header_row=True):
                        dpg.add_table_column(label="Topic", )
                        dpg.add_table_column(label="Score")
                        for x in range(MAX_ITEMS):
                            label = f'{x+1:>2}. {topics[x][0].title()}'
                            with dpg.table_row():
                                dpg.add_selectable(label=label, user_data=topics[x], callback=button_callback, tag=f'tooltip{x}')
                                with dpg.tooltip(parent=f'tooltip{x}'):
                                    dpg.add_text(topics[x][0].title())
                                dpg.add_text(f"{topics[x][1]:>5.2f}")
                with dpg.child_window():
                    # put in data plot based on topics
                    with dpg.plot(label="Topic Visualizer", width=dpg.get_viewport_width()//2-70):
                        dpg.add_plot_axis(dpg.mvXAxis)
                        ticks = []
                        for x in range(1,11):
                            ticks.append((x, x*10))
                        dpg.set_axis_ticks(dpg.last_item(), ticks)
                        dpg.add_plot_axis(dpg.mvYAxis, label="SCORE", tag="y_axis")
                        # for x in range(MAX_ITEMS):
                        dpg.add_bar_series(list(range(5, MAX_ITEMS*5+5, 5)), [topic[1] for topic in topics], parent="y_axis")
                    dpg.add_button(label="Open Messagebox", callback=lambda:show_info("Message Box", "Do you wish to proceed?", on_selection))



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()   