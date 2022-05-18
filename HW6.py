import shutil
import sys
from asyncio import run, gather
from pathlib import Path
from aiopath import AsyncPath
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

    async def sort(self, path):
        """Recursive sort function"""
        if not self.validate_path(Path(path)):
            return f"Incorrect path provided: {path}"
        async for element in path.iterdir():
            if await element.is_dir():
                await self.sort(element)
            else:
                await self.transport_file(element)        
        return f"Sort done successfully by path: {path}"

    @staticmethod
    def validate_path(path: Path):
        return path.exists() and path.is_dir()

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

    async def transport_file(self, file):
        """Replace file in folder with needed type"""
        file_name, file_extension = self.get_name_extension(file.name)
        for key, val in self.dir_ext.items():
            if file_extension.upper() in val:
                await file.replace(str(key) + '/' + file.name)
                return

        await file.replace(str(self.another_path) + '/' + file.name)

    @staticmethod
    async def handle_folder(folder: Path):
        try:
            await folder.rmdir()
        except OSError:
            print(f"Can not delete folder {folder}")

    @staticmethod
    async def scan_for_folders(folder: Path):
        async for item in folder.iterdir():
            if await item.is_dir():
                if item.name not in ("IMAGES", "DOCUMENTS", "AUDIOS", "VIDEOS", "OTHER", "ARCH"):
                    FOLDERS.append(item)
                continue


if __name__ == "__main__":
    start = time()
    scan_path = sys.argv[1]
    folder = AsyncPath(scan_path)
    folder.resolve()
    s = SortManager()
    s.setup(folder)
    async def main():
        scrapers = (s.sort(folder),s.scan_for_folders(folder), *[s.handle_folder(f) for f in FOLDERS])
        await gather(*scrapers)
    run(main())
    print('Done', time() - start)
