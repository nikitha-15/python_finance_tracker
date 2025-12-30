from datetime import datetime

category_data = {'I': 'Income','E':'Expense'}

def get_datetime(prompt,allow_default=False):
    date_time = input(prompt)
    if allow_default and not date_time:
        return datetime.today("%m-%d-%Y")
    try:
        valid_date = datetime.strptime(date_time, "%m-%d-%Y")
        return valid_date.strftime("%m-%d-%Y")
    except ValueError:
        print("Invalid date. Make sure the date is in mm-dd-yyyy format")
        return get_datetime(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount you want to add?"))
        if amount <= 0:
            raise ValueError("Amount must be non-negative non-zero value")
        return amount
    except ValueError as e:
        print(str(e))
        return get_amount()

def get_category():
    try:
        category = input(("Enter the category of the amount: 'I' for Income, 'E' for Expense: ").upper())
        if category in category_data:
            return category_data[category]
        print('Invalid category.')
        return get_category()
    except ValueError as e:
        print(str(e))

def get_description():
    description = input("Enter a description(optional)")
    return description
