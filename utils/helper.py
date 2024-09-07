import pandas as pd
import json
from functools import wraps
import time
from utils.log import logger
from datetime import datetime
import pytz
import re


def file_reader(file_path):
    """
    The `file_reader` function reads and loads data from Excel, CSV, or JSON files based on the file
    format specified in the file path.

    :param file_path: The `file_reader` function you provided reads different types of files (Excel,
    CSV, JSON) based on the file extension in the `file_path`. If the file extension is `.xlsx`, it
    reads an Excel file using `pd.read_excel`, if it's `.csv`, it reads a CSV
    """
    if file_path.endswith("xlsx"):
        data = pd.read_excel(file_path)

        return data
    elif file_path.endswith("csv"):
        data = pd.read_csv(file_path)
        return data
    elif file_path.endswith("json"):
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    else:
        return (
            "ERROR: Unsupported file format. Upload .xlsx, .csv, or .json file format."
        )


def parse_abbreviated_value(value):
    """
    The `parse_abbreviated_value` function converts abbreviated numeric values (e.g., '1.5k', '3.2M') to
    their full numeric representation in Python.

    :param value: It looks like you have provided a code snippet for a function
    `parse_abbreviated_value` that takes an abbreviated numeric value as input and converts it to a full
    numeric value. The function handles abbreviations like 'k' for thousands and 'm' for millions. It
    also logs the conversion process
    :return: The `parse_abbreviated_value` function returns the converted numeric value based on the
    input value with abbreviated notation. If the input value contains 'k', it converts the value to
    thousands, if it contains 'm', it converts the value to millions, and if there is no abbreviation,
    it returns the numeric value as is.
    """
    value = str(value).lower()  # Handle both 'k' and 'K', 'm' and 'M'
    logger.debug(f"Converting value: {value}")

    if "k" in value:
        # Remove 'k' and convert to float (thousands)
        numeric_part = re.sub(r"[^\d.]", "", value)  # Allow for decimal points
        result = float(numeric_part) * 1000
        logger.debug(f"Converted {value} to {result}")
        return result
    elif "m" in value:
        # Remove 'm' and convert to float (millions)
        numeric_part = re.sub(r"[^\d.]", "", value)  # Allow for decimal points
        result = float(numeric_part) * 1000000
        logger.debug(f"Converted {value} to {result}")
        return result
    else:
        # Handle numeric values without abbreviation
        numeric_part = re.sub(r"[^\d.]", "", value)  # Allow for decimal points
        result = float(numeric_part) if numeric_part else 0
        logger.debug(f"Converted {value} to {result}")
        return result


def get_max_formatted_value(matches):
    """
    The function `get_max_formatted_value` takes a list of matches, extracts numeric values, finds the
    maximum value, formats it based on magnitude, and returns the formatted maximum value.

    :param matches: matches: [ '2.5M', '750K', '10L', '1.2Cr' ]
    :return: The function `get_max_formatted_value` returns a formatted string representing the maximum
    value found in the input list of matches. The formatting is based on the magnitude of the maximum
    value, with abbreviations such as 'Cr' for Crore, 'M' for Million, 'L' for Lakh, and 'K' for
    Thousand used to represent large numbers. If the maximum value is below
    """
    logger.info(f"Found matches: {matches}")
    numeric_values = [parse_abbreviated_value(value) for value in matches]
    max_value = max(numeric_values)
    logger.info(f"Numeric values: {numeric_values}")
    logger.info(f"Max value: {max_value}")

    if max_value >= 10000000:
        formatted_max_value = f"{max_value / 10000000:.1f}Cr"  # Crore (Cr)
    elif max_value >= 1000000:
        formatted_max_value = f"{max_value / 1000000:.1f}M"  # Million (M)
    elif max_value >= 100000:
        formatted_max_value = f"{max_value / 100000:.1f}L"  # Lakh (L)
    elif max_value >= 1000:
        formatted_max_value = f"{max_value / 1000:.1f}K"  # Thousand (K)
    else:
        formatted_max_value = str(int(max_value))

    logger.info(f"Formatted max value: {formatted_max_value}")
    return formatted_max_value


def datetimefix(datestr):
    """
    The `datetimefix` function takes a date string in UTC format, converts it to Indian Standard Time
    (IST), and returns the formatted IST time string.

    :param datestr: The `datestr` parameter should be a string representing a date and time in the
    format: "Day Month Date Hour:Minute:Second Timezone Year"
    :return: The `datetimefix` function takes a date string in UTC format, converts it to Indian
    Standard Time (IST), and then returns the formatted IST time in the format "YYYY-MM-DD HH:MM:SS".
    """
    utc_time = datetime.strptime(datestr, "%a %b %d %H:%M:%S %z %Y")
    # Convert to Indian Standard Time (IST)
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = utc_time.astimezone(ist)

    # Format the IST time as needed
    formatted_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except:
            logger.error("error in function - {}".format(func.__name__))
            raise
        end = time.time()
        time_taken = end - start
        if time_taken >= 1:
            logger.warning("{} ran in {}s".format(func.__name__, round(time_taken, 2)))
        else:
            logger.info("{} ran in {}s".format(func.__name__, round(time_taken, 2)))
        return result

    return wrapper
