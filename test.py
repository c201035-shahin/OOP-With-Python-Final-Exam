import random
last_4_digits = random.randint(0, 9999)
last_4_digits_str = f"{last_4_digits:06d}"

seven_digit_number = f"303{last_4_digits_str}"

print(seven_digit_number)
