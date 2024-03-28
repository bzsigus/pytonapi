from .models import Event
##nincs még kész
class EventAnalyzer:
    def get_joiners_multiple_meetings_method(events : Event):
        joiners_dict = {}
        
        for event in events:
            for joiner in event.get("joiners", []):
                email = joiner.get("email")
                if email in joiners_dict:
                    joiners_dict[email] += 1
                else:
                    joiners_dict[email] = 1
        
        joiners_multiple_meetings = [email for email, count in joiners_dict.items() if count >= 2]
        

        if joiners_multiple_meetings == []:
            return "No joiners attending at least 2 meetings"


        return joiners_multiple_meetings