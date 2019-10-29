import xml.etree.ElementTree as E
from config import zwift_config as zc

WORKOUT_TYPE_INTERVAL = 'Intervals'
WORKOUT_TYPE_STEADY = 'Steady'

PACE = zc["Pace"]
OVER_UNDER = "1"


def generate_workout_segment_dictionary_steady(input_dict):
    ret_dict = dict(Duration=input_dict["Duration"], Power=input_dict["Power"], Pace=PACE)
    try:
        ret_dict["Cadence"] = input_dict["Cadence"]
    except KeyError:
        print("No cadence in still training")
    return ret_dict


def generate_workout_segment_dictionary_intervals(input_list):
    # Repeat, First interval duration, Second interval duration, FI power, SI power, FI Cadence, SI Cadence
    return_dict = dict(Repeat=input_list[0], OnDuration=input_list[1], OffDuration=input_list[2], OnPower=input_list[3],
                       OffPower=input_list[4], Pace=PACE, OverUnder=OVER_UNDER)
    if input_list[4] is not "0":
        return_dict["Cadence"] = input_list[5]
    if input_list[5] is not "0":
        return_dict["CadenceResting"] = input_list[6]
    return return_dict


def generate_workout_file(output_filename, workout_name, list_of_parameters_dictionaries, description="", author=zc['Author'],
                          sport_type=zc['Sport_type'],custom_tags_dict = None):
    workout_file = E.Element("workout_file")

    author_field = E.SubElement(workout_file, "author")
    author_field.text = author

    workout_name_field = E.SubElement(workout_file, "name")
    workout_name_field.text = workout_name

    description_field = E.SubElement(workout_file, "description")
    description_field.text = description

    sport_type_field = E.SubElement(workout_file, "sportType")
    sport_type_field.text = sport_type

    tags_field = E.SubElement(workout_file, "tags")
    E.SubElement(tags_field, "tag", {'name': "Created by Python generator"})
    try:
        E.SubElement(tags_field, 'tag',custom_tags_dict)
    except TypeError:
        print("No custom_tags_dict")

    workout_field = E.SubElement(workout_file, "workout")
    if_added_interval_tag_field = False
    for sub_dict in list_of_parameters_dictionaries:
        if sub_dict["type"] == WORKOUT_TYPE_STEADY:
            E.SubElement(workout_field, "SteadyState", generate_workout_segment_dictionary_steady(sub_dict))
        elif sub_dict[0] == WORKOUT_TYPE_INTERVAL:
            E.SubElement(workout_field, "IntervalsT", generate_workout_segment_dictionary_intervals(sub_dict))
            if if_added_interval_tag_field is False:
                tag_field = E.SubElement(tags_field, "tag", {'name': "INTERVALS"})
                if_added_interval_tag_field = True
    E.ElementTree(workout_file).write(output_filename, "utf-8")
    return E.tostring(workout_file)
