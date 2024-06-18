# Import PySimpleGUI
import PySimpleGUI as sg
import csv 

# Partner Class
class Partner:
    def __init__(self, name, type, resources, contact):
        self.name = name
        self.type = type
        self.resources = resources
        self.contact = contact
    
    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'resources': self.resources,
            'contact': self.contact
        }

# A list of dictionaries to store information about business and community partners
partners = []

# A function to search by a given keyword
def search(keyword):
    # Convert the keyword to lowercase
    keyword = keyword.lower()
    # Create an empty list to store the matching results
    results = []
    # Loop through each partner in the list
    for partner in partners:
        # Loop through each key and value in the partner dictionary
        if keyword in partner.name.lower() or \
           keyword in partner.type.lower() or \
           keyword in partner.resources.lower() or \
           keyword in partner.contact.lower(): 
            results.append(partner)
    # Return the results list
    return results

# A function to display the information in a formatted way
def display(partner):
    # Create an empty string to store the output
    output = ""
    # Add the partner information
    output += f"Name: {partner.name}\n"
    output += f"Type: {partner.type}\n"
    output += f"Resources: {partner.resources}\n"
    output += f"Contact: {partner.contact}\n"
    # Return the output string
    return output

# A function to add a partner and its details to the database
def add(name, type, resources, contact):
    # Create a Partner object 
    partner = Partner(name, type, resources, contact)
    # Append the partner to the partners list
    partners.append(partner)
    # Return a message that the partner was added successfully
    return f"Partner {name} was added successfully."

# Function to sort alphabetically
def sort_alphabetical(partners):
    return sorted(partners, key=lambda x: x.name)

# Function to sort reverse alphabetically
def sort_reverse_alphabetical(partners):
    return sorted(partners, key=lambda x: x.name, reverse=True)

def load_partners(filename="partners.csv"):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                partners.append(Partner(**row))
    except FileNotFoundError:
        print("Partner data not found. Starting with a new list.")
    return partners

def save_partners(partners, filename="partners.csv"):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['name', 'type', 'resources', 'contact']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for partner in partners:
            # Pass the dictionary directly 
            writer.writerow(partner.to_dict())  

# Index of order of partner
order_added_index = 0 

# Define the window layout using a list of lists of elements
layout = [
    [sg.Text("Welcome to HSC's partner program.")],
    [sg.Text("You can search and filter the information about business and community partners by entering a keyword.")],
    [sg.Text("To add a new partner to the database, click 'Add'.")],
    [sg.InputText(size=(20, 1), key="-SEARCH-"), sg.Button("Search")],
    [sg.Text("Filter Options:"), 
     sg.Button("Alphabetical"), 
     sg.Button("Reverse Alphabetical"), 
     sg.Button("Order Added"), 
     sg.Button("Reverse Order Added")],
    [sg.Listbox([p.name for p in partners], size=(40, 10), key="-LIST-", enable_events=True)],
    [sg.Button("Add"), sg.Button("Edit", key="-EDIT-"), sg.Button("Remove", key="-REMOVE-"), sg.Button("Exit")]
]

# Create a window object using the layout and a title
window = sg.Window("Partner Program", layout, finalize=True)

# Load the partner data on startup
partners = load_partners() 

window["-LIST-"].update([p.name for p in partners]) 

# Start an event loop to handle user interactions
while True:
    # Read the window events and values
    event, values = window.read()
    # Check if the user wants to exit or close the window
    if event == sg.WINDOW_CLOSED or event == "Exit":
        # Break the loop
        break
    # Check if the user wants to add a partner
    elif event == "Add":
        popup_layout = [
        [sg.Text("Enter the partner name:"), sg.Input(key="-NAME-")],
        [sg.Text("Enter the partner type:"), sg.Input(key="-TYPE-")],
        [sg.Text("Enter the partner resources:"), sg.Input(key="-RESOURCES-")],
        [sg.Text("Enter the partner contact:"), sg.Input(key="-CONTACT-")],
        [sg.Button("OK"), sg.Button("Cancel")]
        ]

        # Create the pop up window using the layout and a title
        popup_window = sg.Window("Enter the partner details", popup_layout, modal=True)

        # Read the pop up window events and values
        popup_event, popup_values = popup_window.read()

        # Close the pop up window
        popup_window.close()

        # Check if the user pressed OK
        if popup_event == "OK":
            # Get the values from the pop up window
            name = popup_values["-NAME-"]
            type = popup_values["-TYPE-"]
            resources = popup_values["-RESOURCES-"]
            contact = popup_values["-CONTACT-"]
            # Validate the input
            if not name or not type or not resources or not contact:
                # Show an error message in a popup window
                sg.popup_error("Invalid input. Please enter non-empty values for all fields.", title="Input Error", keep_on_top=True)
            else:
                # Call the add function and print the result
                print(add(name, type, resources, contact))
                # Update the listbox element with the new partner name
                window["-LIST-"].update([p.name for p in partners])
                # Save the updated partners list
                save_partners(partners)  
        # Check if the user pressed Cancel or closed the pop up window
        elif popup_event in (None, "Cancel"):
            # Skip the rest of the code
            pass

       

    # Check if the user wants to search
    elif event == "Search":

         # Get the keyword from the search field and strip spaces
        keyword = values["-SEARCH-"].strip()
        # Validate the input  
        if keyword: 
            # Call the search function and get the results 
            results = search(keyword)
        else:  
            # Reset to the full list if the search field is empty
            results = partners 
        # Update the listbox element with the matching partner names 
        window["-LIST-"].update([p.name for p in results])  # Update the listbox

    # Check if the user selected a partner name from the listbox
    elif event == "-LIST-":
        if values["-LIST-"]:
            # Get the selected name from the listbox
            name = values["-LIST-"][0]
            # Loop through the partners list to find the matching partner
            for partner in partners:
                # Check if the partner name matches the selected name
                if partner.name == name:
                    # Display the partner details using a pop up window  
                    sg.popup(f"Name: {partner.name}\nType: {partner.type}\nResources: {partner.resources}\nContact: {partner.contact}", title=partner.name, keep_on_top=True)
                    # Break the loop
                    break
        else:
            # Handle the case where the list is empty
            sg.popup("No partner selected.", title="Info", keep_on_top=True) 

    # Check if the user wants to remove a partner
    elif event == "-REMOVE-":
        # Get the selected names from the listbox
        names = values["-LIST-"]
        # Validate the selection
        if not names:
            # Show an error message in a popup window
            sg.popup_error("Invalid selection. Please select one to remove.", title="Selection Error", keep_on_top=True)
        else:
            # Create a confirmation pop up window
            confirm = sg.popup_ok_cancel(f"Are you sure you want to remove this partner from the database?", title="Confirmation", keep_on_top=True)
            # Check if the user pressed OK
            if confirm == "OK":
                # Loop through the selected names
                for name in names:
                    # Loop through the partners list to find the matching partner
                    for partner in partners:
                        # Check if the partner name matches the selected name
                        if partner.name == name:
                            # Remove the partner from the partners list
                            partners.remove(partner)
                            save_partners(partners)
                            # Break the inner loop
                            break
                # Update the listbox element with the new partner names
                window["-LIST-"].update([p.name for p in partners])
            # Check if the user pressed Cancel
            elif confirm == "Cancel":
                # Do nothing
                pass
            else:
                # The user closed the pop up window
                # Do nothing
                pass

    elif event == "-EDIT-":
        try: 
            name = values["-LIST-"][0]  

            for partner in partners:
                if partner.name == name:
                    found_partner = partner  
                    break
            else:  
                    raise ValueError("Partner not found. This shouldn't happen!")

            layout = [
                [sg.Text("Name"), sg.Input(default_text=found_partner.name, key="-NAME-")],
                [sg.Text("Type"), sg.Input(default_text=found_partner.type, key="-TYPE-")],
                [sg.Text("Resources"), sg.Input(default_text=found_partner.resources, key="-RESOURCES-")],
                [sg.Text("Contact"), sg.Input(default_text=found_partner.contact, key="-CONTACT-")],
                [sg.Button("Save"), sg.Button("Cancel")]
            ]

            # Create the editable popup window (layout remains the same)
            edit_window = sg.Window("Edit the partner details:", layout, keep_on_top=True)
            edit_event, edit_values = edit_window.read()
            edit_window.close()  

            if edit_event == "Save":
                # No more alphanumeric check - only check for empty fields
                if not edit_values["-NAME-"] or not edit_values["-TYPE-"] or not edit_values["-RESOURCES-"] or not edit_values["-CONTACT-"]:
                    sg.popup_error("Invalid input. Please enter non-empty values for all fields.", title="Input Error", keep_on_top=True)
                else:
                    # Update the partner details 
                    found_partner.name = edit_values["-NAME-"]
                    found_partner.type = edit_values["-TYPE-"]
                    found_partner.resources = edit_values["-RESOURCES-"]
                    found_partner.contact = edit_values["-CONTACT-"]
                    
                    window["-LIST-"].update([p.name for p in partners]) 
                    # Save the updated partners list
                    save_partners(partners)  

        except IndexError:
            sg.popup_error("Please select a partner to edit.", title="Selection Error", keep_on_top=True)
        except ValueError as e:
            sg.popup_error(f"Editing error: {e}", title="Error", keep_on_top=True)

    # Filter handlers
    elif event == "Alphabetical":
        filtered_partners = sort_alphabetical(partners)
        window["-LIST-"].update([p.name for p in filtered_partners])

    elif event == "Reverse Alphabetical":
        filtered_partners = sort_reverse_alphabetical(partners)
        window["-LIST-"].update([p.name for p in filtered_partners])

    elif event == "Order Added":
        window["-LIST-"].update([p.name for p in partners])  # Reset to original order

    elif event == "Reverse Order Added":
        # Reverse existing order
        partners.reverse() 
        window["-LIST-"].update([p.name for p in partners])

    elif event == sg.WINDOW_CLOSED or event == "Exit":
        # Save data before exiting
        save_partners(partners)  
        break  


# Close the window
window.close()
