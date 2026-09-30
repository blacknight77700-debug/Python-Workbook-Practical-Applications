#Imports

import os, datetime


# Catalog of items

catalog_basket = {
    "Frozen Ham": 50,
    "Frozen Turkey": 50,
    "Canned Yams": 5,
    "Canned Corn": 5,
    "Canned Green Beans": 5,
    "Canned Carrots": 5, 
    "Canned Peas": 5,
    "Canned Fruit": 5,
    "Canned Pumpkin": 5,
    "Canned Milk": 5,
    "Instant Mashed Potatoes": 8,
    "Potatoes": 5,
    "Sugar": 15,
    "Flour": 10,
    "Cranberry Sauce": 5,
    "Pie Crust": 8,
    "Pie Filling": 5,
    "Stuffing Mix": 10,
    "Gravy Mix": 1,
    "Bread Mix": 5,
    "Cookie Mix": 5,
    "Cake Mix and Icing": 5,
    "Cooking Oil": 8,
    "Mac n Cheese": 2 

}


catalog_pantry = {
    "Canned Meat": 10,
    "Peanut Butter": 8,
    "Boxed Meal Kits": 5,
    "Canned Soup": 5,
    "Quick Meals": 1
}


# catalog = catalog_basket | catalog_pantry


# Testing

print()

# Rules


""" It cleans up whitespace, catches common placeholder strings
for missing data, and applies title case to valid text"""

def normalize_value(x):
    if x is None:
        return None

    if isinstance(x, (int, float)):
        return x

    if isinstance(x, str):
        x = x.strip()

        if x.lower() in ['none', 'null', 'n/a', 'na', '']:
            return None
        return x.title()
        
    return x

"""taking basket_items's raw pairs, applying the lambda sorting rules 
with tie-breakers, and slicing out the extremes"""
def sort_basket_bookends(basket_items):
    sorted_items = sorted(basket_items, key=lambda s: (s[1], s[0]))
    bottom_five = sorted_items[:5]  
    top_five = sorted_items[-5:]
    final_extremes = (bottom_five, top_five)
    return final_extremes
    

# Functions


"""Checks if file exists; if not, creates and seeds it. 
If the files exists, it reads the content into the dictionary"""

def load_inventory():
    inventory = {}

    # Checks if file exists; if not, creates and seeds it
    if  not os.path.exists('inventory.txt'):
        with open('inventory.txt', 'w') as ifile:
            for item_name in catalog_basket:
                ifile.write(f"{item_name},0\n")
                inventory[item_name] = 0

            for item_name in catalog_pantry:
                ifile.write(f"{item_name},0\n")
                inventory[item_name] = 0
    else: 
         # If the files exists, it reads the content into the dictionary
         with open('inventory.txt', 'r') as ifile:
             for line in ifile:
                 line = line.strip()
                 if line: # Skips empty lines if there is any
                     name,qty = line.split(',')
                     inventory[name] = int(qty)
    return inventory         
    

"""Persists the current inventory dictionary to 'inventory.txt'.
    Takes the active inventory dictionary and overwrites the storage file,
    writing each item and its quantity as a flat, comma-separated 
    'Name,Quantity' line."""

def save_inventory(inventory):
    with open('inventory.txt', 'w') as ifile:
        for name,qty in inventory.items():
            ifile.write(f'{name},{qty}\n')
    

"""Adds an item's quantity to a specific integer; restrict values if it would cause the total quantity to be less than 0.

If name not found, asks to add item (then set its initial non-negative quantity).

After any successful change, persists to inventory.txt."""

def update_quantity(inventory):
    raw_input = input("Enter Item: ")
    query = normalize_value(raw_input)
    

    if not query in inventory:
        raw_choice = input("Do You want to add it as a new item (yes/no): ")
        choice = normalize_value(raw_choice)

        qty = 0

        if choice in ["No","N"]:
            print("Cancelled")
            return

        else:

            while True:
                try:
                    qty = int(input("Add a new quantity"))

                    if qty < 0:
                        print("Can't be Negative, Try again")
                    else: 
                        break

                except ValueError:
                    print("Invalid value, has to be a whole number")
    else:
        qty = inventory[query] 
        action = input(" do you want to add or subtract? (add/sub): ")
        

        try:
            amount = int(input("Enter the amount: "))
            if action == "add":
                    qty += amount
                    print(f"Success! New quantity: {qty}")

            elif action == "sub" or action == "subtract":
                if amount > qty:
                    print("Error: cannot subtract more than current quantity")
                    

                else:
                    qty -= amount
                    print(f"Success! New quantity: {qty}")

            else:
                print("Invalid action. Please type 'add' or 'sub'.")
                return

        except ValueError:
            print("Invalid amount. Please enter a valid number")
            return

    
    inventory[query] = qty
    save_inventory(inventory)
    log_txn(query, qty)
    

"""sets a baseline with infinity.

It queries the inventory with a default of 0.

When it finds a new lowest quantity, it updates the minimum and resets the limiting_item list to that new item.

When it encounters a tie, it appends the extra item to the list.

Finally, it returns both your basket count (current_min) and the exact items holding you back."""

def calc_baskets(inventory):
    limiting_item = []
    current_min = float('inf')

    for basket in catalog_basket:
        qty = inventory.get(basket, 0)
        if qty < current_min:
            current_min = qty
            limiting_item = [basket]

        elif qty == current_min:
            limiting_item.append(basket)
    return current_min, limiting_item


"""It acts as the reporting engine, it isolates and displays the critical extremes 
lowest-stocked items (critical shortages) and highest-stocked items (well-stocked items),
while calculating point values and totals"""

def view_all(inventory):
    bottom_five, top_five = top_bottom_five(inventory)
    grand_total_items = 0
    
    
    cumulative_points = 0

    print("- Critical Shortages -")
    for name,qty in bottom_five:
        points = catalog_basket.get(name, 0)
        item_cumlative = points * qty

        print(f"Item: {name} | Quantity: {qty} | Points: {points} | Cumulative: {item_cumlative}")

        grand_total_items += qty

        if name in catalog_basket:
            cumulative_points += item_cumlative 

    print("- Well-Stocked Items -")
    for name,qty in top_five:
        points = catalog_basket.get(name, 0)
        item_cumlative = points * qty

        print(f"Item: {name} | Quantity: {qty} | Points: {points} | Cumulative: {item_cumlative}")

        grand_total_items += qty

        if name in catalog_basket:
            cumulative_points += item_cumlative 

    print(f"\nTotal Cumlative Points: {cumulative_points}")
    print(f"Grand Total of Items: {grand_total_items}")


"""Filters and gathers data"""

def top_bottom_five(inventory):
    basket_items = []

    for bookends in catalog_basket:
        if bookends in inventory:
            qty = inventory.get(bookends, 0)
            inventory_record = (bookends, qty)
            basket_items.append(inventory_record)

    return sort_basket_bookends(basket_items)

            


"""Allows a user to look up a single item quickly.
Asks the user for an item name.
Normalizes the input and performs a case-insensitive lookup in the inventory dictionary.
If found, displays its current quantity and cumulative points. If not found, prints a polite message letting the user know.
"""

def search_item(inventory):
    raw_input = input("Enter Item Name: ")
    query = normalize_value(raw_input)

    if query in inventory:
        print(f"Yay! Found {query}: {inventory[query]}")
    else:
        print("Sorry, Item Not Found")
    

"""Records a permanent history of inventory changes.
Pulls the current date and time using the datetime module.
Formats the timestamp into a readable string format (Month-DD-YYYY HH:MM AM/PM).
Opens transactions.txt in append mode ('a') so it adds a brand-new line to the bottom of the file without erasing past logs.
Writes a transaction record detailing what update happened to which item.
"""


def log_txn(name, qty):
    update_time = datetime.datetime.now()
    update_completed = update_time.strftime("%B-%d-%Y %I:%M %p")
    completed = f"{update_completed} - Updated {name} to quantity: {qty}"
    with open('transactions.txt', 'a') as tfile:
        tfile.write(completed + '\n')

    
# Testing Field

if __name__ == "__main__":
    # Load or initialize the inventory on startup
    current_inventory = load_inventory()
    print("Welcome to the Thanksgiving Food Drive Inventory System!")

    while True:
        print("\n--- Main Menu ---")
        print("1. View Inventory Report (Extremes & Points)")
        print("2. Update Item Quanity (Add / Subtract / New)")
        print("3. Search for a Single Item")
        print("4. Exit Program")

        choice = input("Please select an option (1-4): ").strip()

        if choice == "1":
            print("\n" + "="*40)
            view_all(current_inventory)
            print("="*40)

        elif choice == "2":
            update_quantity(current_inventory)

        elif choice == "3":
            search_item(current_inventory)

        elif choice == "4":
            print("\nExiting Program. Happy Thanksgiving!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 4.")