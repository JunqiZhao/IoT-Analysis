import csv
import time
import datetime


with open('event_messages.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)
    list_shorted = []
    for line in csv_reader:
        if line[4] == "Contacts Shorted":
            list_shorted.append(line)

    # put EventTime to datetime format
    for line in list_shorted:

        line[0] = datetime.datetime.strptime(line[0], "%m/%d/%Y %H:%M")
        # Note: In documentation, it says the format of month must be zero-padded,
        # but it seems to work in this non-zero-padded scenario

    # divide into separate time slot
    stats = []
    temp = list_shorted[0][0]
    count = 0
    ten_minutes = datetime.timedelta(minutes=10)
    one_minutes = datetime.timedelta(minutes=1)
    one_hour = datetime.timedelta(hours=1)
    for line in list_shorted:
        if line == list_shorted[-1]:
            if temp - ten_minutes < line[0] <= temp:
                count += 1
                stats.append([temp - ten_minutes + one_minutes, temp, count])
            else:
                stats.append([temp - ten_minutes + one_minutes, temp, count])

                if line[0] < temp - ten_minutes:
                    temp = line[0]
                else:
                    temp = temp - ten_minutes
                count = 1
                stats.append([temp - ten_minutes + one_minutes, temp, count])
        elif temp-ten_minutes < line[0] <= temp:

            count += 1
        else:

            stats.append([temp-ten_minutes+one_minutes, temp, count])

            if line[0] <= temp-ten_minutes:
                temp = line[0]
            else:
                temp = temp-ten_minutes
            count = 1

    # print out the result
    for line in stats:
        if line == ["Start Time","End Time", "Counts"]:
            pass
        line[0] = line[0].strftime("%d/%m/%Y %H:%M")
        line[1] = line[1].strftime("%d/%m/%Y %H:%M")

    stats = [["Start Time", "End Time", "Counts"]] + stats

    print(stats)
