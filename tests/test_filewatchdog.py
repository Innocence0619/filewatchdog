import unittest
import tempfile
import os
import time
import filewatchdog as watcher
import shutil



class TestWatcherJob(unittest.TestCase):

    def _run_watcher_with_timeout(self,timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            watcher.run_pending()
            time.sleep(1)
            with open(self.temp_file3, 'w') as f:
                f.write('Changed content')

    def setUp(self):
            self.temp_dir = tempfile.mkdtemp()
            self.temp_file1 = os.path.join(self.temp_dir, 'temp_file1.txt')
            self.temp_file2 = os.path.join(self.temp_dir, 'temp_file2.txt')
            self.temp_folder = os.path.join(self.temp_dir, 'temp_folder')
            os.makedirs(self.temp_folder)
            self.temp_file3 = os.path.join(self.temp_folder, 'temp_file3.txt')
            self.filelist = [self.temp_file1, self.temp_file2, self.temp_file3]
            for file_path in [self.temp_file1, self.temp_file2, self.temp_file3]:
                with open(file_path, 'w') as f:
                    f.write('Initial content')

            self.file_modified = False
            self.file_exist = False

    def job_modified(self):
        self.file_modified=True
        print("modified")

    def job_exist(self):
        self.file_exist = True

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


    def test_folder_modified(self):
        watcher.once().folder(self.temp_dir).modified.do(self.job_modified)
        self._run_watcher_with_timeout(timeout=5)
        self.assertTrue(self.file_modified)
        
    def test_file_modified(self):
        watcher.once().file(self.temp_file3).modified.do(self.job_modified)
        self._run_watcher_with_timeout(timeout=3)
        self.assertTrue(self.file_modified)
    
    # def test_list_modified(self):
    #     watcher.once().one_of(self.filelist).modified.do(self.job_modified)
    #     self._run_watcher_with_timeout(timeout=5)
    #     self.assertTrue(self.file_modified)


if __name__ == '__main__':
    unittest.main()
