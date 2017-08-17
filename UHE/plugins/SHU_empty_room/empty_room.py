'''
Find Empty Room
'''
import json
import os

from UHE.utils import this_course, this_term, this_week, this_year
# from flask import current_app

JSON_FILE = open('classroomdata.json')
CLASSROOM_DICT = json.load(JSON_FILE)


def get_room_schedule(room):
    """
    return a schedule of a given room in this semster
    """
    return CLASSROOM_DICT.get(room)


def is_room_empty(room, week, day, time):
    """
    confirm weather the room is empty at the time
    """
    return CLASSROOM_DICT[room][week - 1][day - 1][time - 1] == 1


def get_emptyroom_now():
    """
    uses present time to get a list contain all free rooms
    """
    week = schooltime.this_week()
    day = schooltime.this_day()
    time = schooltime.this_class()
    return get_emptyroom(week, day, time)


def get_emptyroom(week, day, time):
    """
    use custom time to get a list contain all free rooms
    """
    emptyroom_list = []
    if time == 0 or day == 0 or day == 6:
        return emptyroom_list
    for classroom in CLASSROOM_DICT.keys():
        if CLASSROOM_DICT[classroom][week - 1][day - 1][time - 1] == 1:
            emptyroom_list.append(classroom)
    return sorted(emptyroom_list)
