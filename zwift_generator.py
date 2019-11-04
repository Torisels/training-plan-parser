import xml.etree.ElementTree as ElmntTree
import math
import enum
import re
import pathlib


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

    def __init__(self, workout_type, zwift_path, cadence_mode=CadenceModes.Round_Floor):
        self.workout_type = workout_type
        self.default_cadence_mode = cadence_mode
        self.zwift_path = zwift_path
        if self.check_if_path_exists() is False:
            raise FileNotFoundError("Please specify correct Zwift Path")

    def check_if_path_exists(self):
        return pathlib.Path(self.zwift_path).is_dir()

    def handle_cadence(self, cadence_str, mode):
        if mode is None:
            mode = self.default_cadence_mode
        if "-" in cadence_str:
            cadences = cadence_str.split("-")
            lower = int(cadences[0])
            higher = int(cadences[1])
            if mode is CadenceModes.Higher:
                return higher
            elif mode is CadenceModes.Lower:
                return lower
            elif mode is CadenceModes.Round_Floor:
                return (lower + higher) // 2
            return math.ceil((lower + higher) / 2)
        return int(cadence_str)

    def process_steady_block(self, input_dict):
        ret_dict = dict(Duration=input_dict["Duration"], Power=input_dict["Power"], Pace=self.PACE)
        try:
            cadence = input_dict["Cadence"]
            cadence_mode = None
            if "Cadence_mode" in input_dict:
                cadence_mode = input_dict["Cadence_mode"]
            ret_dict["Cadence"] = str(self.handle_cadence(cadence, cadence_mode))
        except KeyError:
            print("No cadence in still training")
        return ret_dict

    def process_interval_block(self, input_dict):
        # Repeat, First interval duration, Second interval duration, FI power, SI power, FI Cadence, SI Cadence
        return_dict = dict(Repeat=input_dict["Repeat"], OnDuration=input_dict["F_Duration"],
                           OffDuration=input_dict["S_Duration"],
                           OnPower=input_dict["F_Power"], OffPower=input_dict["S_Power"],
                           Pace=self.PACE, OverUnder=self.OVER_UNDER)

        f_cadence_mode = input_dict["F_Cadence_Mode"] if "F_Cadence_Mode" in input_dict else None
        s_cadence_mode = input_dict["S_Cadence_Mode"] if "S_Cadence_Mode" in input_dict else None

        if "F_Cadence" in input_dict:
            return_dict["Cadence"] = str(self.handle_cadence(input_dict["F_Cadence"], f_cadence_mode))
        if "S_Cadence" in input_dict:
            return_dict["CadenceResting"] = str(self.handle_cadence(input_dict["S_Cadence"], s_cadence_mode))
        return return_dict

    def generate_workout_file(self, output_filename, workout_name, workout_dicts, description="",
                              custom_tags_dict=None):
        # main element
        workout_file = ElmntTree.Element("workout_file")
        # author field
        author_field = ElmntTree.SubElement(workout_file, "author")
        author_field.text = self.AUTHOR
        # workout name field
        workout_name_field = ElmntTree.SubElement(workout_file, "name")
        workout_name_field.text = workout_name
        # description of the workout
        description_field = ElmntTree.SubElement(workout_file, "description")
        description_field.text = description
        # sport type: bike or run
        sport_type_field = ElmntTree.SubElement(workout_file, "sportType")
        sport_type_field.text = self.SPORT_TYPE
        # custom tags
        tags_field = ElmntTree.SubElement(workout_file, "tags")
        ElmntTree.SubElement(tags_field, "tag", {'name': "Created by Python generator by @Torisels"})
        if self.workout_type == self.WORKOUT_TYPE_INTERVAL:
            ElmntTree.SubElement(tags_field, "tag", {'name': "Intervals"})

        try:
            ElmntTree.SubElement(tags_field, 'tag', custom_tags_dict)
        except TypeError:
            print("No custom_tags_dict")

        workout_field = ElmntTree.SubElement(workout_file, "workout")

        for block_dict in workout_dicts:
            if block_dict["type"] == self.WORKOUT_TYPE_STEADY:
                ElmntTree.SubElement(workout_field, "SteadyState",
                                     self.process_steady_block(block_dict))
            elif block_dict["type"] == self.WORKOUT_TYPE_INTERVAL:
                ElmntTree.SubElement(workout_field, "IntervalsT", self.process_interval_block(block_dict))
        # output the file
        output_str = self.add_newlines_to_xml_string(ElmntTree.tostring(workout_file))
        with open(output_filename, "w") as f:
            f.write(output_str)
        return output_str

    @staticmethod
    def add_newlines_to_xml_string(input_str):
        regex = r"((<workout_file>)|(<\/.*?>)|(<\w*?\s\/>))"
        p = re.compile(regex)
        return p.sub(r'\g<1>\n', input_str.decode("UTF-8"))
