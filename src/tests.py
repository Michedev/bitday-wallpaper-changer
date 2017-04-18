import unittest

from src import wallpaper_changer


class Mytime:
    def __init__(self, hour=None, minute=None, second=None):
        self.second = second
        self.minute = minute
        self.hour = hour


class Tests(unittest.TestCase):
    def get_filename(self, path_img) -> str:
        return path_img.rpartition('/')[2]

    def test_remaining_second_hour_pair_zero_minutes_seconds(self):
        time = Mytime(4, 0, 0)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 2 * 60 * 60)

    def test_remaining_seconds_hour_pair_15_minutes_0_seconds(self):
        time = Mytime(4, 15, 0)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 60 * 60 + 45 * 60)

    def test_remaining_seconds_hour_pair_30_minutes_20_seconds(self):
        time = Mytime(4, 30, 20)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 60 * 60 + 29 * 60 + 40)

    def test_remaining_seconds_hour_pair_50_minutes_50_seconds(self):
        time = Mytime(8, 50, 50)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 60 * 60 + 9 * 60 + 10)

    def test_remaining_seconds_hour_dispair_30_minutes_20_seconds(self):
        time = Mytime(5, 30, 20)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 29 * 60 + 40)

    def test_remaining_seconds_only_one_second(self):
        time = Mytime(5, 59, 59)
        self.assertEqual(wallpaper_changer.seconds_to_next_img(time), 1)

    def test_get_img_path_by_hour1(self):
        hour = 4
        path_img = wallpaper_changer.get_img_path_by_hour(hour)
        filename = self.get_filename(path_img)
        self.assertTrue(filename.startswith("12"))

    def test_get_img_path_by_hour2(self):
        hour = 5
        path_img = wallpaper_changer.get_img_path_by_hour(hour)
        filename = self.get_filename(path_img)
        self.assertTrue(filename.startswith("12"))

    def test_get_img_path_by_hour3(self):
        hour = 6
        path_img = wallpaper_changer.get_img_path_by_hour(hour)
        filename = self.get_filename(path_img)
        self.assertTrue(filename.startswith("01"))

    def test_get_img_path_by_hour4(self):
        hour = 12
        path_img = wallpaper_changer.get_img_path_by_hour(hour)
        filename = self.get_filename(path_img)
        self.assertTrue(filename.startswith("04"))
