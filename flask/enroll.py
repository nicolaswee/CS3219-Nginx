import sys, csv, dotenv
from mongoengine import connect
from models import *
from io import TextIOWrapper

def main(file):
    csv_file = TextIOWrapper(file, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
    erorr_list = []
    success_row_count = 0

    for row_count, row in enumerate(csv_reader):
        if row_count == 0:
            continue

        email = row[0].strip()
        name = row[1]
        section = row[2]

        print(email, name, section)

        if is_empty(email, name, section):
            message = "Empty field in row {}".format(row_count + 1)
            erorr_list.append(message)
            continue

        
        if not(validate_email(email)):
            message = "Invalid Email in row {}".format(row_count + 1)
            erorr_list.append(message)
            continue

        try:
            section_object = Section.objects.get(section=section)
            user = User(email=email, name=name, section_enrolled=section_object, user_type='student')
            user.save()
            success_row_count += 1

        except Exception as e:
            message = "Invalid Section in row {}".format(row_count + 1)
            erorr_list.append(message)
            continue
        

    # must remember to add 1 for row count
    print("Total Row Processed: {}".format(row_count))
    print("Total Row Passed: {}".format(success_row_count))
    print(erorr_list)
    return (row_count, success_row_count, erorr_list)

def is_empty(email, name, section):
    return not(email) or not(name) or not(section)

def validate_email(email):
    return '@' in email and 'smu.edu.sg' in email


if __name__ == "__main__":
    main(sys.argv[1])