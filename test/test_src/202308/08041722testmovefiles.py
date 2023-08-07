import os
import shutil
from playerlib.video.video_class import *
from playerlib.video.video_searcher import *
from playerlib.utils.utils import *
from playerlib.constants import *

class MoveCommand:
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def execute(self):
        shutil.move(self.src_path, self.dest_path)

    def undo(self):
        shutil.move(self.dest_path, self.src_path)


class MoveManager:
    def __init__(self):
        self.commands = []
        self.current_index = -1

    def execute_command(self, command):
        command.execute()
        self.commands.append(command)
        self.current_index += 1

    def undo(self):
        if self.current_index >= 0:
            command = self.commands[self.current_index]
            command.undo()
            self.current_index -= 1

    def redo(self):
        if self.current_index < len(self.commands) - 1:
            command = self.commands[self.current_index + 1]
            command.execute()
            self.current_index += 1


def move_video_from_here_to_there(_from_folder: str, _to_folder: str):
    from_folder = os.path.abspath(_from_folder)
    to_folder = os.path.abspath(_to_folder)
    vs = VideoSearcher(from_folder)
    video_list = vs.get_video_path()

    move_manager = MoveManager()  # 创建MoveManager对象

    for video_path in video_list:
        filename = os.path.basename(video_path)
        destination = os.path.join(to_folder, filename)

        command = MoveCommand(video_path, destination)  # 创建MoveCommand对象
        move_manager.execute_command(command)  # 执行命令


# 示例用法
_from_folder = '/path/to/source_folder'
_to_folder = '/path/to/destination_folder'

move_video_from_here_to_there(_from_folder, _to_folder)


#todo 我希望能够设计一种行为类，可以实现所有的undo redo以及行为日志记录。回头有空研究一下
