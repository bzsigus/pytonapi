from .models import Event

class EventAnalyzer:
    def get_joiners_multiple_meetings_method(events : Event):
        joiners_dict = {}
        #végig megy az eventeken egy szótárat hoz létre belőle és megszámolja hogy hányszor szerepel az adott emberek neve
        for event in events:
                for joiner in event.get("joiners", []):
                    name = joiner.get("name")
                    if name in joiners_dict:
                        joiners_dict[name] += 1
                    else:
                        joiners_dict[name] = 1
            #egy listagenerátorral joiners_multiple_meetings-be gyüjti azokat a neveket amik 2x vagy többször szerepelnek
                joiners_multiple_meetings = [name for name, count in joiners_dict.items() if count >= 2]

        #ha a lista üres akkor egy üzenetet ad vissza hogy nem volt olyan ember aki 2 eseményen is részt vett
        if joiners_multiple_meetings == []:
            return "No joiners attending at least 2 meetings"

        return joiners_multiple_meetings