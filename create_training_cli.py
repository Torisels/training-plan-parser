import click
import datetime
from zwift_generator import ZwiftGenerator
# from google_sheet_handler import SheetHandler
import excel_processor as proc

ZWIFT_PATH = "C:/Users/Gustaw/Documents/Zwift/Workouts/875923/"


@click.command()
@click.argument('workout_type')
@click.argument('name')
@click.option('--times', '-t', default=0)
@click.option('--filename', '-fn', default=0)
@click.option('--date', '-d', default=0)
def main(workout_type, name, times, filename, date):
    # Sh = SheetHandler("credentials.json")
    if date is not 0:
        pass
        # training_string = Sh.get_training_for_day(datetime.datetime(day=24, month=11, year=2019))
        # workout_type = proc.determine_type(training_string)
        # print(f"Detected workout type is: {workout_type}")

    # times = 0 => times, duration[s], power [%FTP], cadence [RPM]
    # times > 0 => times, duration_0[s], power_0 [%FTP], cadence_0 [RPM], duration_1[s], power_1 [%FTP], cadence_1 [RPM]

    workout_type = str.lower(workout_type)
    if filename is 0:
        filename = name + ".zwo"

    if workout_type == "steady":
        generator = ZwiftGenerator(ZwiftGenerator.WORKOUT_TYPE_STEADY, ZWIFT_PATH)
        blocks = list(input_routine("STEADY segment: "))
        generator.generate_workout_file(filename, name, [["0"] + blocks])
    elif workout_type == "intervals" or workout_type == "int":
        generator = ZwiftGenerator(ZwiftGenerator.WORKOUT_TYPE_INTERVAL, ZWIFT_PATH)
        blocks = interval_routine(times)
        print(generator.generate_workout_file(filename, name, blocks))

    else:
        print("Please specify correct type (steady|(int)ervals)")


def interval_routine(times):
    print(f"Interval routine, You have chosen {times} times: ")
    parameters = list()
    warm_up = input_routine("Warm-up parameters [leave length empty to omit this]: ", True)
    lower_interval = list(input_routine("\nParameters for the first segment of the interval: "))
    higher_interval = list(input_routine("\nParameters for the second segment of the interval: "))
    cool_down = input_routine("\nCool-down parameters [leave length empty to omit this]: ", True)
    if warm_up:
        parameters.append(["0"] + list(warm_up))
    parameters.append([str(times)] + lower_interval + higher_interval)
    if cool_down:
        parameters.append(["0"] + list(cool_down))
    return parameters

def input_routine(header_text, omit=False):
    print(header_text)
    duration = input("Length (mm|mm:ss): ")
    if len(duration) == 0 and omit:
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


if __name__ == "__main__":
    main()
