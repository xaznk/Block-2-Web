import sys
from pathlib import Path
from time import time
import concurrent.futures


IMAGES = ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC', 'TIF']
DOCUMENTS = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX',
             'PPTX', 'TEX', 'BIB', 'CLS', 'RTF', 'PPT', 'CSV']
AUDIOS = ['MP3', 'OGG', 'WAV', 'AMR', 'M4A', 'AAC']
VIDEOS = ['AVI', 'MP4', 'MOV', 'MKV']
ARCHIVES = ['ZIP', 'GZ', 'TAR', 'RAR', 'TGZ', 'FB2']
FOLDERS = []


class SortManager:
    """Sort files by categories (images, docs, videos etc.)"""
    dir_ext: dict = None
    another_path: Path = None

    def setup(self, path):
        self.dir_ext = {self.create_dir(path, "IMAGES"): IMAGES,
                        self.create_dir(path, "DOCUMENTS"): DOCUMENTS,
                        self.create_dir(path, "AUDIOS"): AUDIOS,
                        self.create_dir(path, "VIDEOS"): VIDEOS,
                        self.create_dir(path, "ARCH"): ARCHIVES}
        self.another_path = self.create_dir(path, "OTHER")

    def sort(self, path):
        """Recursive sort function"""
        if not self.validate_path(Path(path)):
            return f"Incorrect path provided: {path}"

        self.setup(path)
        self.sort_files(Path(path))
        return f"Sort done successfully by path: {path}"

    @staticmethod
    def validate_path(path: Path):
        return path.exists() and path.is_dir()

    def sort_files(self, path: Path):
        for element in path.iterdir():
            if element.is_dir():
                self.sort_files(element)
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
        for key, val in self.dir_ext.items():
            if file_extension.upper() in val:
                file.replace(str(key) + '/' + file.name)
                return

        file.replace(str(self.another_path) + '/' + file.name)

    @staticmethod
    def handle_folder(folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f"Can not delete folder {folder}")

    @staticmethod
    def scan_for_folders(folder: Path):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ("IMAGES", "DOCUMENTS", "AUDIOS", "VIDEOS", "OTHER", "ARCH"):
                    FOLDERS.append(item)
                continue


if __name__ == "__main__":
    start = time()
    scan_path = sys.argv[1]
    folder = Path(scan_path)
    folder.resolve()
    s = SortManager()
    # s.sort(folder)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(s.sort(folder))
        s.scan_for_folders(folder)
        for f in FOLDERS:
            s.handle_folder(f)
    print('Done', time() - start)
