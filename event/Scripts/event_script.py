#event type creation script
from event.models import EventTypes
import csv

def create_event_type():
    fhand = open('event/Scripts/event_type.csv')
    reader = csv.reader(fhand)
    for row in reader:
        # print(row)
        p, query_check = EventTypes.objects.get_or_create(type_name = row[0], type_decription = row[1])
