from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager


router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    managger = EventFileManager()
    return managger.read_events_from_file()




@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
  manager = EventFileManager()
  events = manager.read_events_from_file()
  filtered_events = []

  for event in events:
        if date and event['date'] != date:
            continue
        if organizer and event["organizer"]["name"] != organizer:
            continue
        if status and event["status"] != status:
            continue
        if event_type and event["type"] != event_type:
            continue

        filtered_events.append(event)
    
  return filtered_events
 


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    manager = EventFileManager()
    events = manager.read_events_from_file()

    for event in events:
        if event['id'] == event_id:
            return event
        
    raise HTTPException(status_code=404, detail="Event not found")



@router.post("/events", response_model=Event)
async def create_event(event: Event):
    manager = EventFileManager()
    events = manager.read_events_from_file()
    
    for existing_event in events:
        if existing_event['id'] == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exists")
    
    events.append(event.model_dump())

    manager.write_events_to_file(events)

    return event  
    

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    manager = EventFileManager()
    events = manager.read_events_from_file()

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
    
    for i, event in enumerate(events):
        if event['id'] == event_id:
            del events[i]
            manager.write_events_to_file(events)
            return 'Event deleted successfully'
    
    raise HTTPException(status_code=404, detail="Event not found")


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
