# Tuple containing available movies: (Title, Showtime, Base Price)
MOVIES = (
    ("Avengers: Endgame", "10:00 AM", 200.0),
    ("Inception", "02:00 PM", 180.0),
    ("Interstellar", "06:30 PM", 250.0),
)


def create_seat_grid():
    """Creates a 5-row by 8-column seat map where every seat starts as 'O' (Open)."""
    grid = []
    for _ in range(5):
        row = ["O", "O", "O", "O", "O", "O", "O", "O"]
        grid.append(row)
    return grid


def count_free_in_row(row):
    """Recursively counts how many open ('O') seats are left in a given row."""
    if len(row) == 0:
        return 0
    if row[0] == "O":
        return 1 + count_free_in_row(row[1:])
    else:
        return count_free_in_row(row[1:])


def get_seat_price(base_price, row_num):
    """Calculates ticket price, adding Rs. 50 extra for back rows (4 and 5)."""
    if row_num >= 4:
        return base_price + 50.0
    else:
        return base_price


def display_seat_map(grid):
    """Prints the visual seat layout, free seat counts per row, and total seats left."""
    print("\n--- SCREEN THIS WAY ---")
    print("       1 2 3 4 5 6 7 8")
    total_free = 0

    for r in range(5):
        row_num = r + 1
        row_text = f"Row {row_num}: " + " ".join(grid[r])
        free = count_free_in_row(grid[r])
        total_free += free

        if row_num >= 4:
            tag = "(Back +50)"
        else:
            tag = "(Normal)"

        print(f"{row_text}  | Free: {free} {tag}")

    print("Total Available Seats:", total_free)
    print("-----------------------")







# Harshit Code-----


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


#Satgur-Singh Code-----
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
