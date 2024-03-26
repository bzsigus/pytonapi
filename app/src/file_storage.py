import json

class EventFileManager:
    FILE_PATH = "event.json"

    def read_events_from_file(self):
                try:
                    with open(self.FILE_PATH, "r") as file:
                        events = json.load(file)
                        return events
                    
                except FileNotFoundError:
                    return []
                except Exception as e:
                    return []

    def write_events_to_file(self, events):
        with open(self.FILE_PATH, "w") as file:
            json.dump(events, file)
                        
            