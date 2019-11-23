# cli.py
import click
import datetime
from zwift_generator import ZwiftGenerator
from google_sheet_handler import SheetHandler
import excel_processor as proc
ZWIFT_PATH = "C:/Users/Gustaw/Documents/Zwift/Workouts/875923/"


@click.command()
@click.argument('workout_type')
@click.argument('name')
@click.option('--times', '-t', default=0)
@click.option('--filename', '-fn', default=0)
@click.option('--date', '-d', default=0)
def main(workout_type, name, times, filename, date):
    Sh = SheetHandler("credentials.json")
    if date is not 0:
        training_string = Sh.get_training_for_day(datetime.datetime(day=24, month=11, year=2019))
        workout_type = proc.determine_type(training_string)
        print(f"Detected workout type is: {workout_type}")

    # times = 0 => times, duration[s], power [%FTP], cadence [RPM]
    # times > 0 => times, duration_0[s], power_0 [%FTP], cadence_0 [RPM], duration_1[s], power_1 [%FTP], cadence_1 [RPM]
    workout_type = str.lower(workout_type)
    if filename is 0:
        filename = name + ".zwo"

    if workout_type == "steady":
        generator = ZwiftGenerator(ZwiftGenerator.WORKOUT_TYPE_STEADY, ZWIFT_PATH)
        params = list(input_routine("STEADY segment: "))
        generator.generate_workout_file(filename, name, [["0"] + params])
    elif workout_type == "intervals" or workout_type == "int":
        print("TBD")
        generator = ZwiftGenerator(ZwiftGenerator.WORKOUT_TYPE_INTERVAL, ZWIFT_PATH)

    else:
        print("Please specify correct type (steady|(int)ervals)")


def interval_routine(times):
    print(f"Interval routine, You have chosen {times} times: ")
    workout_parms = list()
    warm_up = tuple_to_dict(input_routine("Warm-up parameters: "))
    warm_up["type"] = ZwiftGenerator.WORKOUT_TYPE_STEADY
    f_dur, f_pow, f_cad = input_routine("Parameters for the first segment of the interval: ")
    s_dur, s_pow, s_cad = input_routine("Parameters for the second segment of the interval: ")
    cool_down = input_routine("Cool-down parameters [leave length empty to omit this]: ")


def input_routine(header_text):
    print(header_text)
    duration = input("Length (mm|mm:ss): ")
    if len(duration) == 0:
        return False

    power = input("Power (%FTP): ")
    cadence = input("Cadence (RPM) leave empty for None: ")

    if ":" in duration:
        minutes, seconds = duration.split(":")
        minutes = int(minutes)
        seconds = int(seconds)
        seconds += minutes * 60
    else:
        seconds = int(duration) * 60

    power = int(power) / 100
    cadence = 0 if len(cadence) == 0 else cadence

    return str(seconds), str(power), str(cadence)

def tuple_to_dict(input_tuple):
    duration = input_tuple[0]
    power = input_tuple[1]
    cadence = input_tuple[2]
    return dict(Duration=duration, Power=power, Cadence=cadence)



if __name__ == "__main__":
    main()
