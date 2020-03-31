import unittest
from slideshowservice import SlideshowService
from history import History
import datetime

class TestSlideshowService(unittest.TestCase):
    def test_current_index_less_than_file_num(self):
        service = SlideshowService()
        current_index = 8
        file_num = 10
        result = service.get_next_image_index(current_index, file_num)
        expected = 9
        self.assertEqual(expected, result)
    
    def test_current_index_greater_than_equal_file_num(self):
        service = SlideshowService()
        current_index = 9
        file_num = 10
        result = service.get_next_image_index(current_index, file_num)
        expected = 0
        self.assertEqual(expected, result)

    def test_current_index_over_file_num(self):
        service = SlideshowService()
        current_index = 10
        file_num = 10
        result = service.get_next_image_index(current_index, file_num)
        expected = 0
        self.assertEqual(expected, result)

    def test_get_history_all(self):
        service = SlideshowService()
        result_list = service.get_history_all("test_history_data.csv")
        expected_list = []
        history1 = History()
        history1.file_path = "E:/picture/study/slideshow/drawing/satan/コメント 2019-03-20 113806.png"
        history1.time_limit = '60'
        history1.start_time = datetime.datetime.fromisoformat("2020-03-20T11:14:01.457398")
        history1.end_time = datetime.datetime.fromisoformat("2020-03-20T11:14:13.013391")
        history1.diff_time = "0:00:11.555993"
        history1.create_datetime = datetime.datetime.fromisoformat("2020-03-20T11:14:01.457398")
        history2 = History()
        history2.file_path = "E:/picture/study/slideshow/bean/Desktop Screenshot 2019.01.22 - 12.37.26.90.png"
        history2.time_limit = '30'
        history2.start_time = datetime.datetime.fromisoformat("2020-03-20T23:10:03.069993")
        history2.end_time = datetime.datetime.fromisoformat("2020-03-20T23:10:07.726150")
        history2.diff_time = "0:00:04.656157"
        history2.create_datetime = datetime.datetime.fromisoformat("2020-03-20T23:10:03.069993")
        history3 = History()
        history3.file_path = "E:/picture/study/slideshow/bean/Desktop Screenshot 2019.01.22 - 12.39.24.18.png"
        history3.time_limit = '30'
        history3.start_time = datetime.datetime.fromisoformat("2020-03-20T23:10:07.845971")
        history3.end_time = datetime.datetime.fromisoformat("2020-03-20T23:10:08.399897")
        history3.diff_time = "0:00:00.553926"
        history3.create_datetime = datetime.datetime.fromisoformat("2020-03-20T23:10:07.845971")
        expected_list.append(history1)
        expected_list.append(history2)
        expected_list.append(history3)

        for i in range(len(result_list)):
            self.assertEqual(result_list[i].file_path, expected_list[i].file_path)
            self.assertEqual(result_list[i].time_limit, expected_list[i].time_limit)
            self.assertEqual(result_list[i].start_time, expected_list[i].start_time)
            self.assertEqual(result_list[i].end_time, expected_list[i].end_time)
            self.assertEqual(result_list[i].diff_time, expected_list[i].diff_time)
            self.assertEqual(result_list[i].create_datetime, expected_list[i].create_datetime)

    def test_get_report(self):
        
        pass

    def test_practice_time_distribution(self):
        service = SlideshowService()
        history_list = service.get_history_all("test_history_data.csv")
        history_dict = service.practice_time_distribution(history_list)

        self.assertEqual(len(history_dict[11]), 1)
        self.assertEqual(len(history_dict[23]), 2)




if __name__ == "__main__":
    unittest.main()
