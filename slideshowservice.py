import datetime
import os
import matplotlib.pyplot as plt
from history import History
import numpy as np

class SlideshowService:
    def __init__(self):
        pass

    def get_next_image_index(self, current_index, file_num):
        return 0 if current_index+1 >= file_num else current_index + 1

    def get_history_all(self, history_file_name):
        save_filename = history_file_name
        history_file_path = "history/{}".format(save_filename)
        history_list = []
        with open(history_file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                csv = line.rstrip(os.linesep).split(",")
                history = History()
                history.file_path = csv[0]
                history.time_limit = csv[1]
                history.start_time = datetime.datetime.fromisoformat(csv[2])
                history.end_time = datetime.datetime.fromisoformat(csv[3])
                history.diff_time = csv[4]
                history.create_datetime = datetime.datetime.fromisoformat(csv[5])
                history_list.append(history)

        return history_list

    def get_report(self, history_list):
        history_dict = {}
        for i in history_list:
            if not i.create_datetime.date() in history_dict:
                value_list = []
                value_list.append(i)
                history_dict.update({i.create_datetime.date():value_list})
            else:
                history_dict[i.create_datetime.date()].append(i)

        return history_dict

    def create_graph(self, history_dict):
        fig = plt.Figure()
        x=np.array([key for key in history_dict.keys()])
        y=np.array([len(i[1]) for i in history_dict.items()])
        ax = fig.add_subplot()
        ax.plot(x, y)
        ax.grid()

        return fig

    def practice_time_distribution(self, history_list):
        history_dict = {0:[],1:[],2:[],3:[],4:[],5:[]
                       ,6:[],7:[],8:[],9:[],10:[],11:[]
                       ,12:[],13:[],14:[],15:[],16:[],17:[]
                       ,18:[],19:[],20:[],21:[],22:[],23:[]}

        for i in history_list:
            history_dict[i.create_datetime.hour].append(i)

        return history_dict

