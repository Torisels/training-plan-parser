import xml.etree.ElementTree as E
from config import config

WORKOUT_TYPE_INTERVAL = 'Intervals'
WORKOUT_TYPE_STEADY = 'Steady'

PACE = config["pace"]
OVER_UNDER = "1"


def generate_workout_segment_dictionary_steady(input_list):
    # Duration, Power, Cadence
    if input_list[2] == "0":
        return dict(Duration=input_list[0], Power=input_list[1], pace=PACE)
    else:
        return dict(Duration=input_list[0], Power=input_list[1], pace=PACE, Cadence=input_list[2])


def generate_workout_segment_dictionary_intervals(input_list):
    # Repeat, First interval duration, Second interval duration, FI power, SI power, FI Cadence, SI Cadence
    return_dict = dict(Repeat=input_list[0], OnDuration=input_list[1], OffDuration=input_list[2], OnPower=input_list[3],
                       OffPower=input_list[4], Pace=PACE, OverUnder=OVER_UNDER)
    if input_list[4] is not "0":
        return_dict["Cadence"] = input_list[5]
    if input_list[5] is not "0":
        return_dict["CadenceResting"] = input_list[6]
    return return_dict


def generate_workout_file(output_filename, workout_name, parameters_list, description="", author=config['author'],
                          sportType=config['sportType']):
    workout_file = E.Element("workout_file")

    author_field = E.SubElement(workout_file, "author")
    author_field.text = author

    workout_name_field = E.SubElement(workout_file, "name")
    workout_name_field.text = workout_name

    description_field = E.SubElement(workout_file, "description")
    description_field.text = description

    sport_type_field = E.SubElement(workout_file, "sportType")
    sport_type_field.text = sportType

    tags_field = E.SubElement(workout_file, "tags")
    E.SubElement(tags_field, "tag", {'name': "Created by Python generator"})

    workout_field = E.SubElement(workout_file, "workout")

    added_tag_field = 0
    for sub_list in parameters_list:

        if sub_list[0] == WORKOUT_TYPE_STEADY:
            sub_list.pop(0)
            E.SubElement(workout_field, "SteadyState", generate_workout_segment_dictionary_steady(sub_list))
        elif sub_list[0] == WORKOUT_TYPE_INTERVAL:
            sub_list.pop(0)
            E.SubElement(workout_field, "IntervalsT", generate_workout_segment_dictionary_intervals(sub_list))
            if added_tag_field == 0:
                tag_field = E.SubElement(tags_field, "tag", {'name': "INTERVALS"})
                added_tag_field = 1
    E.ElementTree(workout_file).write(output_filename, "utf-8")
    return E.tostring(workout_file)
