from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer


router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
#osztélyt példányosít és beolvassa az összes eseményt amit a file tartalmaz majd vissza adja azt
    managger = EventFileManager()
    return managger.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
  manager = EventFileManager()
  events = manager.read_events_from_file()
  filtered_events = []

#végigiterál az eventeken amit az osztály visszaadott neki és megnézi hogy minden feltétel teljesül e ha igyen hozzáadja 
#a filtered_events listához és a végén azt adja vissza ha nem volt ilyen akkor üres listát ad vissza
  for event in events:
        minden_igaz = True
        if event['date'] != date:
            minden_igaz = False
        if  event["organizer"]["name"] != organizer:
            minden_igaz = False
        if event["status"] != status:
            minden_igaz = False
        if event["type"] != event_type:
            minden_igaz = False

        if minden_igaz == True:
            filtered_events.append(event)
    
  return filtered_events
 


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    manager = EventFileManager()
    events = manager.read_events_from_file()
#végigiterál a eventeken amit az osztály adott neki és vissza adja azokat az eventeket aminek az id-a a keresett 
#mivel az id-nak egyedinek kell lennie (createevent-ben is) ezért csak 1et találhat belőle nem kell a ciklust végigvinnie ha megtatláta
    for event in events:
        if event['id'] == event_id:
            return event
        
    raise HTTPException(status_code=404, detail="Event not found")



@router.post("/events", response_model=Event)
async def create_event(event: Event):
    manager = EventFileManager()
    events = manager.read_events_from_file()
#megnézi hogy a megadott id szerepel e mér az adatbázisban ha igen hibát dob
    for existing_event in events:
        if existing_event['id'] == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exists")
#ha egyedi az id akkor hozzáfűzi az eredetei listához és kiirja a file-ba
    events.append(event.model_dump())

    manager.write_events_to_file(events)
##miután kiírta vissza is adja a listát
    return event  
    

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    manager = EventFileManager()
    events = manager.read_events_from_file()
#végig iterál az eseményeken azonosító alapján megkeresi amit meg kell találnia ha megtalálja akkor felülirja ha nem hibát dob
    for i, existing_event in enumerate(events):
        if existing_event['id'] == event_id:
            events[i] = event.model_dump()
            manager.write_events_to_file(events)
            return event  
    
    raise HTTPException(status_code=404, detail="Event not found")


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    manager = EventFileManager()
    events = manager.read_events_from_file()
#megkeresi a listában az id-val megegyező eseményt ha megtalálja törli ha nem akkor hibát dob vissza
    for i, event in enumerate(events):
        if event['id'] == event_id:
            del events[i]
            manager.write_events_to_file(events)
            return 'Event deleted successfully'
    
    raise HTTPException(status_code=404, detail="Event not found")

@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
#meghívja az eventanalizer osztályt a EventFileManager által visszaadott eseményekkel és a get_joiners_multiple_meetings_method-ját és kiírja az eredményét
    manager = EventFileManager()
    events = manager.read_events_from_file()
  
    joiners_multiple_meetings = EventAnalyzer.get_joiners_multiple_meetings_method(events)
    
    return  joiners_multiple_meetings
