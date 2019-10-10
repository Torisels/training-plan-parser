import re


def process_training_string(input_string):
    is_with_interval = False
    # Find if we have to deal with intervals
    if re.search(r"odp\.?\b|odpoczynek\b", input_string) is not None:
        is_with_interval = True
        print("true")

    #basic training
    match = re.search(r"(?:\b(?P<power_low>\d{2,3})-)?\b(?P<power_high>\d{2,3})\s?%.*kad\s\b(?P<cadence>\d{2,3})", input_string)
    if match is not None:
        print(match.groupdict())


if __name__ == "__main__":
    process_training_string("Trenażer/Szosa 1030 % FTP, kad 1035    +")
