import csv
import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# bubble sort based on first element in nested list
def sort_list(listt):
    leng = len(listt)

    for i in range(0, leng):

        for j in range(0, leng-i-1):

            if listt[j][0] > listt[j + 1][0]:

                tempe = listt[j]
                listt[j] = listt[j + 1]
                listt[j + 1] = tempe

    return listt


with open('event_messages.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)
    list_shorted = []
    for line in csv_reader:
        if line[4] == "Contacts Shorted":
            list_shorted.append(line)

    # put EventTime to datetime format
    for line in list_shorted:
        # transform it into datetime form and make sure it is zero-padded
        line[0] = datetime.datetime.strptime(line[0], "%m/%d/%Y %H:%M")
        line[0] = line[0].strftime("%m/%d/%Y %H:%M")
        line[0] = datetime.datetime.strptime(line[0], "%m/%d/%Y %H:%M")

    # sort the list
    list_sorted = sort_list(list_shorted)

    # divide into separate time slot

    stats = []
    count = 0
    one_minutes = datetime.timedelta(minutes=1)
    one_hour = datetime.timedelta(hours=1)
    temp = list_sorted[0][0].replace(minute=00)-one_hour

    while temp < list_sorted[-1][0]:
        for line in list_sorted:
            if temp<line[0]<=temp+one_hour:
                count+=1
        stats.append([temp + one_minutes, temp+one_hour, count])
        count=0
        temp += one_hour
    if stats[0][2] == 0:
        stats.pop(0)

    # print out the result
    for line in stats:
        if line == ["Start Time","End Time", "Counts"]:
            pass
        line[0] = line[0].strftime("%m/%d/%Y %H:%M")
        line[1] = line[1].strftime("%m/%d/%Y %H:%M")

    time_interval=[]
    counts=[]
    for line in stats:
        time_interval.append("{} to {}".format(line[0],line[1]))
        counts.append(line[2])

    time_interval_tuple=tuple(time_interval)



    # draw the bar chart
    objects = time_interval_tuple
    y_pos = np.arange(len(objects))
    performance = counts

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('counts')
    plt.title('counter for 1h')
    plt.xticks(rotation=88)

    for i, v in enumerate(performance):
        plt.text(y_pos[i] - 0.25, v + 0.01, str(v))
    plt.show()

    # stats = [["Start Time", "End Time", "Counts"]] + stats

    # print(stats)
