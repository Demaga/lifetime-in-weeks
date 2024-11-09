from datetime import date


def weeks_between_two_dates(date_1: date, date_2: date) -> int:
    import logging

    delta = abs(date_2 - date_1)
    week_number = 1
    i = 1
    for _ in range(1, delta.days + 1):
        if week_number > 50 and week_number < 55:
            logging.error(f"{week_number}, {i}")
        if week_number % 52 == 0 and week_number > 0 and i % 8 == 0:
            week_number += 1
            i = 0
        elif week_number % 52 != 0 and i % 7 == 0:
            week_number += 1
            i = 0
        i += 1
    logging.error(f"{date_1}, {date_2}, {delta}, {week_number}")
    return week_number
