from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Event, EventStatus, Reservation

app = FastAPI(
    title="College Event Reservation API",
    description="API for managing college events and student reservations",
    version="1.0.0"
)


# Create database tables when application starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# 1. POST /events
@app.post("/events", response_model=Event, status_code=201)
def create_event(event: Event):
    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event


# 2. GET /events
@app.get("/events", response_model=list[Event])
def get_events():
    with Session(engine) as session:
        events = session.exec(select(Event)).all()
        return events


# 3. GET /events/{event_id}
@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        return event


# 4. PUT /events/{event_id}
@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, updated_event: Event):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        event.title = updated_event.title
        event.venue = updated_event.venue
        event.capacity = updated_event.capacity
        event.organizer = updated_event.organizer
        event.status = updated_event.status

        session.add(event)
        session.commit()
        session.refresh(event)

        return event


# 5. DELETE /events/{event_id}
@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        session.delete(event)
        session.commit()

        return {
            "message": "Event deleted successfully"
        }

@app.post("/events/{event_id}/reserve", response_model=Reservation, status_code=201)
def create_reservation(event_id: int, reservation: Reservation):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        if event.status != EventStatus.Open:
            raise HTTPException(
                status_code=400,
                detail="Event is closed"
            )

        booked = session.exec(
            select(Reservation).where(
                Reservation.event_id == event_id
            )
        ).all()

        if len(booked) >= event.capacity:
            raise HTTPException(
                status_code=400,
                detail="Event is full"
            )

        reservation.event_id = event_id

        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        return reservation


@app.get("/events/{event_id}/reservations", response_model=list[Reservation])
def get_reservations(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        statement = select(Reservation).where(
            Reservation.event_id == event_id
        )

        return session.exec(statement).all()


@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)

        if reservation is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        session.delete(reservation)
        session.commit()

        return {
            "message": "Reservation cancelled successfully"
        }


@app.get("/events/{event_id}/availability")
def get_availability(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        booked = len(
            session.exec(
                select(Reservation).where(
                    Reservation.event_id == event_id
                )
            ).all()
        )

        return {
            "capacity": event.capacity,
            "booked": booked,
            "remaining": event.capacity - booked
        }
    