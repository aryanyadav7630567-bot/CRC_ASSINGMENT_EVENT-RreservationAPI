# College Event Reservation API

A FastAPI-based REST API for managing college events and student reservations.

## Features

- Create, view, update and delete events
- Student event reservations
- Check event reservations
- Cancel reservations
- Check event seat availability
- Prevent reservations when an event is full
- Prevent reservations for closed events
- Input validation
- SQLite database using SQLModel

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLModel
- SQLite
- Pydantic

## Project Structure

```text
event-reservation-api/
├── database.py
├── models.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── screen_shot/