#Alec Lienhard
#11/16/2023
from nicegui import events, ui
import csv, os

columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
            {'name': 'Patching_Task_Name', 'label': 'Task Name', 'field': 'Patching_Task_Name'},
            {'name': 'Location', 'label': 'Location', 'field': 'Location'},
            {'name': 'Start_Time_IST', 'label': 'Start IST', 'field': 'Start_Time_IST'},
            {'name': 'End_Time_IST', 'label': 'End IST', 'field': 'End_Time_IST'},
            {'name': 'Start_Time_EST', 'label': 'Start EST', 'field': 'Start_Time_EST'},
            {'name': 'End_Time_EST', 'label': 'End EST', 'field': 'End_Time_EST'},
            {'name': 'Total_Hours', 'label': 'Total Hours', 'field': 'Total_Hours'},
            {'name': 'Team', 'label': 'Team', 'field': 'Team'},
            {'name': 'Sys_Admin', 'label': 'Sys Admin', 'field': 'Sys_Admin'},
            {'name': 'Servers_Count', 'label': 'Servers Count', 'field': 'Servers_Count'},
            {'name': 'Status', 'label': 'Status', 'field': 'Status'},
            {'name': 'cancelled_server_count', 'label': 'Cancelled Servers Count', 'field': 'cancelled_server_count'},
            {'name': 'PCI_NonPCI', 'label': 'PCI/Non-PCI', 'field': 'PCI_NonPCI'},
            {'name': 'success_server_count', 'label': 'Success Servers Count', 'field': 'success_server_count'},
            {'name': 'failed_server_count', 'label': 'Failed Servers Count', 'field': 'failed_server_count'},
            {'name': 'Ticket_number', 'label': 'Ticket Number', 'field': 'Ticket_number'},
            {'name': 'PreSEN_Date', 'label': 'PreSEN Date', 'field': 'PreSEN_Date'},
            {'name': 'Task_Notes', 'label': 'Task Notes', 'field': 'Task_Notes'},
            {'name': 'EAC Job ID', 'label': 'EAC Job ID', 'field': 'EAC Job ID'}
]

# Read data from a CSV file
def read_csv(file):
    if isinstance(file, str):
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    else:
        content = file.read().decode('utf-8')
        reader = csv.DictReader(content.splitlines())
        return list(reader)

# Update rows with data from CSV
csv_file_path = 'patchroster.csv'  
rows = read_csv(csv_file_path)

def add_row():
    new_id = str(max(int(dx['id']) for dx in rows) + 1)
    rows.append({'id': new_id, 'Patching_Task_Name': 'Patch Group Name', 'Location': 'New Location', 'Start_Time_IST': 'Start Time IST', 'End Time IST': 'End Time IST',
             'Start_Time_EST': 'Start Time EST', 'End_Time_EST': 'End Time EST', 'Total_Hours': 'Total Hours', 'Team': 'TeamX', 'Sys_Admin': 'AdminX', 'Servers_Count': 'Servers Count',
             'Status': 'Planned/Unplanned', 'cancelled_server_count': 'Cancelled Server Count', 'PCI_NonPCI': 'PCI/Non-PCI', 'success_server_count': 'Success Count', 'failed_server_count': 'Failed Count',
             'Ticket_number': '', 'PreSEN_Date': '', 'Task_Notes': '', 'EAC Job ID': ''})
    table.rows = rows  # Update the table.rows
    table.update()
    ui.notify(f'Added new row with ID {new_id}')

def rename(e: events.GenericEventArguments):
    for row in rows:
        if row['ID'] == e.args['ID']:
            row.update(e.args)
    ui.notify(f'Updated rows to: {table.rows}')
    table.update()

def delete(e: events.GenericEventArguments) -> None:
    rows[:] = [row for row in rows if row["id"] != e.args["id"]]
    ui.notify(f"Delete {e.args['id']}")
    table.update()

def export_csv():
    output_file_path = 'output_data.csv'
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = [col['name'] for col in columns]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    ui.notify(f'Data exported to {output_file_path}')
    ui.download(output_file_path)
    


def import_csv(file_path):
    global rows
    new_rows = read_csv(file_path)

    # Find the maximum ID in the existing rows
    max_existing_id = max(int(dx['id']) for dx in rows)

    # Update the ID for the new rows
    for row in new_rows:
        row['id'] = str(int(row['id']) + max_existing_id)

    # Combine the existing rows and new rows
    rows = rows + new_rows

    table.rows = rows  # Update the table.rows
    table.update()
    ui.notify(f'Data imported from {file_path}')
   



def handle_upload(e: events.UploadEventArguments):
    global rows
    content = e.content.read().decode('utf-8')
    with open('uploaded.csv', 'w') as f:
        f.write(content)
    rows = read_csv('uploaded.csv')
    import_csv('uploaded.csv')
    ui.notify(f'Data imported from the uploaded file')

def append_csv_data(file_path):
    global rows
    new_rows = read_csv(file_path)
    
    # Find the highest current ID
    max_id = max(int(dx['id']) for dx in rows)
    
    # Adjust the ID of the new rows to avoid duplicates
    for row in new_rows:
        max_id += 1
        row['id'] = str(max_id)
    
    # Append the new rows to the current rows
    rows.extend(new_rows)
    
    # Update the table.rows and refresh the table
    table.rows = rows
    table.update()
    ui.notify(f'Data appended from {file_path}')

def delete_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        ui.notify(f'Error deleting file {file_path}: {e}')

def toggle_dark_mode(_):
    global counter
    counter += 1
    if counter % 2 == 0:
        dark.enable()
    else:
        dark.disable()

def open_upload_dialog():
    upload_dialog.open()
# Create a flex container for the header
with ui.row().classes('flex items-center justify-between w-full'):
    ui.image('C:\\Users\\alelienh\\Documents\\NiceGui\\Trademark_All_Blue_Logo_2023.png').style("width: 200px")

    # Create a flex container for the switch and menu button
    with ui.row().classes('flex items-center space-x-2'):
        darkswitch = ui.switch('Dark/Light', value=True, on_change=toggle_dark_mode)
        with ui.button(icon='tune'):
            with ui.menu() as menu:
                ui.menu_item('Export CSV', lambda: export_csv())
                ui.menu_item('Upload CSV', open_upload_dialog)
                ui.menu_item('Close', on_click=menu.close)

# Add custom dialog for uploading CSV
with ui.dialog() as upload_dialog, ui.card():
    ui.upload(label="Choose CSV file", on_upload=handle_upload).props("accept=.csv")
    ui.button("Close", on_click=upload_dialog.close)


table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")

table.add_slot(
    "header",
    r"""
    <q-tr :props="props">
        <q-th auto-width />
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
        </q-th>
    </q-tr>
""",
)

table.add_slot(
    "body",
    r"""
    <q-tr :props="props">
        <q-td auto-width >
            <q-btn size="sm" color="warning" round dense icon="delete" :props="props"
                @click="() => $parent.$emit('delete', props.row)" >
        </q-td>
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ props.row[col.field] }}
            <q-popup-edit v-model="props.row[col.field]" v-slot="scope" 
                @update:model-value="() => $parent.$emit('rename', props.row)" >
                <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
        </q-td>
    </q-tr>
    """,
)

table.add_slot(
    "bottom-row",
    r"""
    <q-tr :props="props">
        <q-td colspan="3" class="text-center">
            <q-btn color="accent" icon="add" class="w-full" @click="() => $parent.$emit('addrow')"/>
        </q-td>
    </q-tr>
    """,
)

table.on("rename", rename)
table.on("delete", delete)
table.on("addrow", add_row)

counter = 0

# Set dark mode by default
dark = ui.dark_mode()
dark.enable()

  

ui.run(port = 8081)
table.update()  # Ensure the table is initially updated
ui.run()
