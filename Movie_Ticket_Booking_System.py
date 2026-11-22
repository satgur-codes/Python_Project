MOVIES = (
    ("Border 2", "10:00 AM", 200.0),
    ("Satluj", "02:00 PM", 180.0),
    ("Pushpa 2", "06:30 PM", 250.0)
)


def create_seat_grid():
    grid = []
    for r in range(5):
        row = ["O", "O", "O", "O", "O", "O", "O", "O"]
        grid.append(row)
    return grid
# Creates a 5-row by 8-column seat map where every seat starts as 'O' (Open).


def count_free_in_row(row):
    if len(row) == 0:
        return 0
    if row[0] == "O":
        return 1 + count_free_in_row(row[1:])
    else:
        return count_free_in_row(row[1:])
# Counts how many open ('O') seats are left in a row using simple if-else steps.


def get_seat_price(base_price, row_num):
    if row_num >= 4:
        return base_price + 50.0
    else:
        return base_price
# Calculates the ticket price, adding Rs. 50 extra for back rows (4 and 5).


def display_seat_map(grid):
    print("\n--- SCREEN THIS WAY ---")
    print("     1 2 3 4 5 6 7 8")
    total_free = 0
    for r in range(5):
        row_text = "Row " + str(r + 1) + ": " + " ".join(grid[r])
        free = count_free_in_row(grid[r])
        total_free = total_free + free
        if r + 1 >= 4:
            tag = "(Back +50)"
        else:
            tag = "(Normal)"
        print(row_text, " | Free:", free, tag)
    print("Total Available Seats:", total_free)
    print("-----------------------")
# Prints the visual seat layout, free seat counts per row, and total seats left.


def format_seats(seats):
    parts = []
    for r, c in seats:
        parts.append("R" + str(r) + "-S" + str(c))
    return ", ".join(parts)
# Turns a list of seat coordinates like [(1, 2)] into readable text like "R1-S2".


def select_movie(movie_data):
    print("\n--- AVAILABLE MOVIES ---")
    for m_id in movie_data:
        name, time, price = movie_data[m_id]["info"]
        print(str(m_id) + ".", name, "| Time:", time, "| Base Price: Rs.", price)
    choice = input("Select Movie (1-3): ").strip()
    if choice in ("1", "2", "3"):
        return int(choice)
    else:
        return 0
# Shows all available movies and returns the chosen movie ID (or 0 if invalid).


def book_tickets(movie_data, movie_id):
    data = movie_data[movie_id]
    display_seat_map(data["grid"])

    name = input("Enter customer name: ").strip().title()
    if name == "":
        print("Name cannot be empty!")
        return False

    try:
        qty = int(input("How many tickets do you want to book? "))
    except ValueError:
        print("Please enter a valid number.")
        return False

    if qty < 1 or qty > 40:
        print("Please enter a number between 1 and 40.")
        return False

    chosen = []
    total_bill = 0.0
    while len(chosen) < qty:
        print("\nSelecting seat", len(chosen) + 1, "of", qty)
        r_in = input("Enter Row (1-5): ").strip()
        c_in = input("Enter Seat (1-8): ").strip()

        if not (r_in.isdigit() and c_in.isdigit()):
            print("Enter numbers only!")
            continue

        r = int(r_in)
        c = int(c_in)
        if r < 1 or r > 5 or c < 1 or c > 8:
            print("Out of range! Row must be 1-5 and Seat 1-8.")
        elif (r, c) in data["booked_set"] or (r, c) in chosen:
            print("Sorry! Seat already booked. Pick another.")
        else:
            chosen.append((r, c))
            total_bill = total_bill + get_seat_price(data["info"][2], r)

    for r, c in chosen:
        data["grid"][r - 1][c - 1] = "X"
        data["booked_set"].add((r, c))

    chosen.sort()
    data["bookings"].append({"name": name, "seats": chosen, "amount": total_bill})
    print("\n--- BOOKING CONFIRMED ---")
    print("Movie:", data["info"][0], "(" + data["info"][1] + ")")
    print("Name :", name)
    print("Seats:", format_seats(chosen))
    print("Total: Rs.", total_bill)
    print("-------------------------")
    return True
# Handles the full booking flow: checks user input, picks open seats, updates the grid, and prints a receipt.


def cancel_booking(movie_data, movie_id):
    data = movie_data[movie_id]
    if len(data["bookings"]) == 0:
        print("No bookings found for this movie.")
        return False

    name = input("Enter customer name to cancel: ").strip().lower()
    for rec in data["bookings"]:
        if rec["name"].lower() == name:
            for r, c in rec["seats"]:
                data["grid"][r - 1][c - 1] = "O"
                data["booked_set"].discard((r, c))
            data["bookings"].remove(rec)
            print("Booking cancelled for", rec["name"])
            return True

    print("No booking found under that name.")
    return False
# Finds a customer's booking by name, frees up their seats back to 'O', and deletes the record.


def view_bookings(movie_data, movie_id):
    data = movie_data[movie_id]
    print("\n=== Bookings for", data["info"][0], "===")
    if len(data["bookings"]) == 0:
        print("No bookings yet.")
        return
    count = 1
    for rec in data["bookings"][:10]:
        print(str(count) + ".", rec["name"], "| Seats:", format_seats(rec["seats"]), "| Paid: Rs.", rec["amount"])
        count = count + 1
# Displays up to the first 10 customer bookings using a simple counter.


def save_to_file(movie_data, filename):
    with open(filename, "w") as f:
        for m_id in movie_data:
            for rec in movie_data[m_id]["bookings"]:
                seat_parts = []
                for r, c in rec["seats"]:
                    seat_parts.append(str(r) + "-" + str(c))
                seats_str = ";".join(seat_parts)
                line = str(m_id) + "|" + rec["name"] + "|" + seats_str + "|" + str(rec["amount"]) + "\n"
                f.write(line)
# Saves all current bookings across all movies into a text file so data isn't lost on exit.


def load_from_file(movie_data, filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")
                m_id = int(parts[0])
                name = parts[1]
                raw_seats = parts[2].split(";")
                amount = float(parts[3])

                seats = []
                for s in raw_seats:
                    rc = s.split("-")
                    r = int(rc[0])
                    c = int(rc[1])
                    seats.append((r, c))
                    movie_data[m_id]["grid"][r - 1][c - 1] = "X"
                    movie_data[m_id]["booked_set"].add((r, c))

                movie_data[m_id]["bookings"].append({"name": name, "seats": seats, "amount": amount})
    except FileNotFoundError:
        pass
# Reads saved bookings from the text file when the program starts and marks those seats as booked ('X').


def main():
    filename = "bookings.txt"
    movie_data = {
        1: {"info": MOVIES[0], "grid": create_seat_grid(), "booked_set": set(), "bookings": []},
        2: {"info": MOVIES[1], "grid": create_seat_grid(), "booked_set": set(), "bookings": []},
        3: {"info": MOVIES[2], "grid": create_seat_grid(), "booked_set": set(), "bookings": []}
    }
    load_from_file(movie_data, filename)

    while True:
        print("\n=== MOVIE TICKET BOOKING SYSTEM ===")
        print("1. View Seat Map")
        print("2. Book Tickets")
        print("3. Cancel Booking")
        print("4. View Bookings")
        print("5. Save & Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "5":
            save_to_file(movie_data, filename)
            print("Saved. Goodbye!")
            break
        elif choice in ("1", "2", "3", "4"):
            m_id = select_movie(movie_data)
            if m_id == 0:
                print("Invalid movie choice!")
                continue
            if choice == "1":
                display_seat_map(movie_data[m_id]["grid"])
            elif choice == "2":
                if book_tickets(movie_data, m_id):
                    save_to_file(movie_data, filename)
            elif choice == "3":
                if cancel_booking(movie_data, m_id):
                    save_to_file(movie_data, filename)
            elif choice == "4":
                view_bookings(movie_data, m_id)
        else:
            print("Invalid option! Enter 1 to 5.")
# Runs the main menu loop, connecting user choices to viewing, booking, cancelling, and saving data.


main()