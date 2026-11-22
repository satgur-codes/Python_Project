# 🎬 Project 16: Movie Ticket Booking System

A simple command-line Python program that lets a user view movies, see a seat map, book and cancel seats, and save all bookings to a file.

## 👥 Group Details

**Allotted Group:** Group 16

| S.No | Name             | Roll No.        |
|------|------------------|-----------------|
| 1    | Gupta Raj        | 202610101200034 |
| 2    | Harshit          | 202610101200016 |
| 3    | Satgur Singh     | 202610101200068 |
| 4    | Abhishek Tripathi| 202610101200031 |

## 🎯 Objective

To develop a program that books seats for a movie show.

## ✨ Features

1. **Movie menu** – three movies with show time and ticket price.
2. **Seat layout** – 5 rows × 8 seats stored as a list of lists and displayed as a map (`O` = open, `X` = booked).
3. **Book multiple seats** – already booked seats are blocked.
4. **Total bill calculation** – back rows (4 and 5) cost Rs. 50 extra.
5. **File saving** – all bookings are saved to `bookings.txt` and loaded again on the next run.
6. **Cancel booking** – cancel by customer name and free the seats.
7. **View bookings** – shows the first 10 bookings for a selected movie.

## 🎥 Movies

| ID | Movie             | Show Time | Base Price |
|----|-------------------|-----------|------------|
| 1  | Avengers: Endgame | 10:00 AM  | Rs. 200    |
| 2  | Inception         | 02:00 PM  | Rs. 180    |
| 3  | Interstellar      | 06:30 PM  | Rs. 250    |

> Rows 4 and 5 (back rows) add **Rs. 50** to the base price per seat.

## 📚 Key Topics Used

| Topic                      | Where it is used |
|----------------------------|------------------|
| Nested loops               | `display_seat_map()` prints the seat map and counts free seats row by row |
| Recursion                  | `count_free_in_row()` recursively counts open seats in a row |
| Sets, tuples, dictionaries | `booked_set` holds booked seats as `(row, seat)` tuples; all main data is stored in the `movie_data` dictionary |
| Lists / list of lists      | `create_seat_grid()` builds the 5×8 grid |
| File handling              | `save_to_file()` and `load_from_file()` |
| Exception handling         | `try/except` for invalid ticket quantity and missing file |
| Functions, if-else, loops, strings | Used throughout the program |

## 📁 File Structure

```
Py_Project/
├── Movie_Ticket_Booking_System.py   # Main program
├── bookings.txt                     # Saved bookings (data file)
└── README.md                        # Project documentation
```

## ▶️ How to Run

1. Make sure Python 3 is installed.
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Py_Project
   ```
3. Run the program:
   ```bash
   python Movie_Ticket_Booking_System.py
   ```

## 🖥️ Menu

```
=== MOVIE TICKET BOOKING SYSTEM ===
1. View Seat Map
2. Book Tickets
3. Cancel Booking
4. View Bookings
5. Save & Exit
```

## 🧾 Sample Output

```
--- BOOKING CONFIRMED ---
Movie: Inception (02:00 PM)
Name : Rahul
Seats: R3-S3
Total: Rs. 180.0
-------------------------
```

## 💾 Data File Format

Each line of `bookings.txt` stores one booking:

```
movie_id|customer_name|row-seat;row-seat|amount
```

Example:

```
2|Rahul|3-3;3-4|360.0
```

## 📝 Notes

- A seat map shows `O` for an open seat and `X` for a booked seat.
- Customer name cannot be empty; ticket quantity must be between 1 and 40.
- Bookings are saved automatically after every booking or cancellation, and also on **Save & Exit**.

## 🙌 Contributors

Group 16 – Gupta Raj, Harshit, Satgur Singh, Abhishek Tripathi