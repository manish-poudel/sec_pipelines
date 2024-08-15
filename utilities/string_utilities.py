def format_cik(cik: int) -> str:
    # Convert the integer to a string and pad with leading zeros to ensure a length of 10 characters
    return str(cik).zfill(10)
