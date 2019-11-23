# cli.py
import click
from zwift_generator import ZwiftGenerator

ZWIFT_PATH = "C:/Users/Gustaw/Documents/Zwift/Workouts/875923/"


@click.command()
@click.argument('type')
@click.argument('name')
@click.option('--times', '-t', default=0)
@click.option('--filename', '-fn', default=0)
def main(type, name, times, filename):
    click.echo("{}, {}".format(type, times))
    type = str.lower(type)
    if filename is 0:
        filename = name + ".zwo"

    if type == "steady":
        generator = ZwiftGenerator(ZwiftGenerator.WORKOUT_TYPE_STEADY, ZWIFT_PATH)
        duration, power, cadence = input_routine("STEADY segment: ")
        parameters = [dict(type=ZwiftGenerator.WORKOUT_TYPE_STEADY, Duration=duration, Power=power, Cadence=cadence)]
        generator.generate_workout_file(filename, name, parameters)
    elif type == "intervals" or type == "int":
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
        seconds = int(duration)

    power = int(power) / 100
    cadence = 0 if len(cadence) == 0 else int(cadence)

    return str(seconds), str(power), str(cadence)

def tuple_to_dict(input_tuple):
    duration = input_tuple[0]
    power = input_tuple[1]
    cadence = input_tuple[2]
    return dict(Duration=duration, Power=power, Cadence=cadence)



if __name__ == "__main__":
    main()
