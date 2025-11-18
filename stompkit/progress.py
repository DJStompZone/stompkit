class Blocks:
    light, med, dark = [chr(9617+ea) for ea in range(3)]

def progress_bar(percent_filled, width=20):
    if type(percent_filled) not in [int, float]:
        raise TypeError("Incorrect type for percent_filled: {type(percent_filled)}, expected str or float.")
    if not 0 <= percent_filled <= 100:
        raise ValueError("percent_filled must be a numerical value between 0 and 100 (inclusive)")
    return f'[{str(f"{Blocks.dark}"*int(width*(percent_filled/100))).ljust(width, Blocks.light)}]'