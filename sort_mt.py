import shutil
import sys
from pathlib import Path
from time import time
import threading
# import concurrent.futures


IMAGES = ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC']
DOCUMENTS = ['DOC', 'DOCX', 'TXT',
             'PDF', 'XLSX', 'PPTX', 'TEX', 'BIB', 'CLS']
AUDIOS = ['MP3', 'OGG', 'WAV', 'AMR']
VIDEOS = ['AVI', 'MP4', 'MOV', 'MKV']
ARCHIVES = ['ZIP', 'GZ', 'TAR', 'RAR', 'TGZ', 'FB2']


class SortManager:
    """Sort files by categories(images, docs, videos etc."""
    __dir_ext: dict = None
    __another_path: Path = None

    def setup(self, path):
        self.__dir_ext = {self.create_dir(path, "IMAGES"): IMAGES,
                          self.create_dir(path, "DOCUMENTS"): DOCUMENTS,
                          self.create_dir(path, "AUDIOS"): AUDIOS,
                          self.create_dir(path, "VIDEOS"): VIDEOS,
                          self.create_dir(path, "ARCH"): ARCHIVES}
        self.__another_path = self.create_dir(path, "OTHER")

    def sort(self, path):
        """Recursive sort function"""
        if not self.validate_path(Path(path)):
            return f"Incorrect path provided: {path}"

        self.setup(path)
        self.__sort(Path(path))
        return f"Sort done successfully by path: {path}"

    @staticmethod
    def validate_path(path: Path):
        return path.exists() and path.is_dir()

    def __sort(self, path: Path):
        for element in path.iterdir():
            if self.is_exist_folder(element):
                continue
            if element.is_dir():
                self.__sort(element)
            else:
                self.transport_file(element)

    @staticmethod
    def create_dir(path, dir_name):
        """Create folders where files will be sort"""
        dir_name_path = Path(str(path) + f"/{dir_name}")
        if not dir_name_path.exists():
            dir_name_path.mkdir()
        return dir_name_path

    @staticmethod
    def get_name_extension(general_name):
        """Split name on 2 pieces: name & extension"""

        dot_position = general_name.rfind(".")
        if dot_position == -1:
            return general_name, ""

        name = general_name[:dot_position]
        extension = general_name[dot_position + 1:]
        return name, extension

    def transport_file(self, file):
        """Replace file in folder with needed type"""
        file_name, file_extension = self.get_name_extension(file.name)
        for key, val in self.__dir_ext.items():
            if file_extension.upper() in val:
                file.rename(str(key) + '/' + file.name)
                return

        file.rename(str(self.__another_path) + '/' + file.name)

    def is_exist_folder(self, elem):
        """Ignore folders if they are already exist"""
        for key in self.__dir_ext.keys():
            if str(elem) == str(key):
                return True
        return False


if __name__ == "__main__":
    start = time()
    scan_path = sys.argv[1]
    folder = Path(scan_path)
    folder.resolve()
    s = SortManager()
    t = threading.Thread(target=s.sort, args=(folder,))
    t.start()
    t.join()
    # s.sort(folder)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.submit(s.sort(folder))
    print('Done', time() - start)
