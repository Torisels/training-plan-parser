import xml.etree.ElementTree as E
from config import config as zc
import math
import enum


class CadenceModes(enum.Enum):
    Lower = 1
    Higher = 2
    Round_Floor = 3
    Round_Ceiling = 4


class ZwiftGenerator:
    WORKOUT_TYPE_INTERVAL = 'Intervals'
    WORKOUT_TYPE_STEADY = 'Steady'
    PACE = "0"
    OVER_UNDER = "1"
    AUTHOR = "Gustaw D."
    SPORT_TYPE = "bike"

    def __init__(self, workout_type, cadence_mode=CadenceModes.Round_Floor):
        self.workout_type = workout_type
        self.default_cadence_mode = cadence_mode

    def handle_cadence(self, cadence_str, mode):
        if mode is None:
            mode = self.default_cadence_mode
        if "-" in cadence_str:
            cadences = cadence_str.split("-")
            lower = cadences[0]
            higher = cadences[1]
            if mode is CadenceModes.Higher:
                return higher
            elif mode is CadenceModes.Lower:
                return lower
            elif mode is CadenceModes.Round_Floor:
                return (lower + higher) // 2
            return math.ceil((lower + higher) / 2)
        return int(cadence_str)

    def generate_workout_segment_dictionary_steady(self, input_dict):
        ret_dict = dict(Duration=input_dict["Duration"], Power=input_dict["Power"], Pace=self.PACE)
        try:
            cadence = input_dict["Cadence"]
            cadence_mode = None
            if "Cadence_mode" in input_dict:
                cadence_mode = input_dict["Cadence_mode"]
            ret_dict["Cadence"] = self.handle_cadence(cadence, cadence_mode)
        except KeyError:
            print("No cadence in still training")
        return ret_dict

    # def generate_workout_segment_dictionary_intervals(input_list):
    #     # Repeat, First interval duration, Second interval duration, FI power, SI power, FI Cadence, SI Cadence
    #     return_dict = dict(Repeat=input_list[0], OnDuration=input_list[1], OffDuration=input_list[2],
    #                        OnPower=input_list[3],
    #                        OffPower=input_list[4], Pace=PACE, OverUnder=OVER_UNDER)
    #     if input_list[4] is not "0":
    #         return_dict["Cadence"] = input_list[5]
    #     if input_list[5] is not "0":
    #         return_dict["CadenceResting"] = input_list[6]
    #     return return_dict

    def generate_workout_file(self, output_filename, workout_name, workout_dicts, description="",
                              custom_tags_dict=None):
        # main element
        workout_file = E.Element("workout_file")
        # author field
        author_field = E.SubElement(workout_file, "author")
        author_field.text = self.AUTHOR
        # workout name field
        workout_name_field = E.SubElement(workout_file, "name")
        workout_name_field.text = workout_name
        # description of the workout
        description_field = E.SubElement(workout_file, "description")
        description_field.text = description
        # sport type: bike or run
        sport_type_field = E.SubElement(workout_file, "sportType")
        sport_type_field.text = self.SPORT_TYPE
        # custom tags
        tags_field = E.SubElement(workout_file, "tags")
        E.SubElement(tags_field, "tag", {'name': "Created by Python generator by @Torisels"})
        if self.workout_type == self.WORKOUT_TYPE_INTERVAL:
            E.SubElement(tags_field, "tag", {'name': "Intervals"})

        try:
            E.SubElement(tags_field, 'tag', custom_tags_dict)
        except TypeError:
            print("No custom_tags_dict")

        workout_field = E.SubElement(workout_file, "workout")

        for segment_dict in workout_dicts:
            if segment_dict["type"] == self.WORKOUT_TYPE_STEADY:
                E.SubElement(workout_field, "SteadyState",
                             self.generate_workout_segment_dictionary_steady(segment_dict))
            elif segment_dict["type"] == self.WORKOUT_TYPE_INTERVAL:
                E.SubElement(workout_field, "IntervalsT", generate_workout_segment_dictionary_intervals(segment_dict))
        # output the file
        E.ElementTree(workout_file).write(output_filename, "utf-8")
        return E.tostring(workout_file)
