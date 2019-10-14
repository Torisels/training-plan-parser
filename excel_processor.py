import re


def process_training_string(input_string):
    # Find if we have to deal with intervals
    match_dict = None
    if re.search(r"odp\.?\b|odpoczynek\b", input_string) is not None:
        print("Intervals")

    else:
        print("Still training")
        match = re.search(
            r"(?:\b(?P<power_low>\d{2,3})-)?\b(?P<power_high>\d{2,3})\s?%.*kad\s\b(?P<cadence>\d{2,3}\b|\+)",
            input_string)
        match_dict = match.groupdict()
        match_dict["type"] = "SteadyState"

    return match_dict


def handle_intervals(input_string):
    m0 = re.search(r",\spo\b", input_string)
    if m0 is not None:
        print("Pattern 1")
    return 0
    # Pattern 1


if __name__ == "__main__":
    dict = handle_intervals("po 15min kad 90 @ 55% zrób 5x 3min @ 55% kad 110/odp 3min kad 90-95, 15min rozjazd @50% kad 90-95")
    print(dict)
