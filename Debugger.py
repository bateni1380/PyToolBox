import inspect
import time
from typing import Any, Callable, Dict, Iterable, List, Literal, Tuple
import numpy as np
import matplotlib.pyplot as plt


class Debugger:
    '''
        This class is a class to observe status of the code. 

        You can create an instance of this class by (debugger = Debugger())
            and whenever you want to print something to see the status of you're code, 
            you can use debugger.log(description: str) to print status.

        This class provides you many tools in order to observe the status of you're program better.
        - 1st, you can print all of you'r debugging-related logs with debugger.log() and
            you have the ability to turn on/of all of the debugging-related logs by changing
            textual_debug/visual_debug in the line that you instantiated the Debugger object.
        - 2nd, you can see the line/file that the log function has been called by setting
            show_file/show_line parameter's to True in constructor.
        - 3rd, you can specify categories in each log's and categorize log's, then you can 
            change categories parameter in constructor to see the related logs.
        - 4th, you can specify processes using log_start and log_end, and then you can
            see the passed time of each process in logs. If you use log_end or log, you will see 
            the passed time since last non finished process started.
        - 5th, you can ilustrate np array images using log_image (for one image) and 
            log_images (for multiple images).

    '''
    def __init__(self, categories=[], textual_debug: bool = False, visual_debug: bool = False,
                 show_file: bool = False, show_line: bool = False):
        '''
            categories parameter is the tool to categorize you're debugging-related logs. you can
                specify some categories here and in log function you can specify some categories too,
                then the log will be printed only if this two set's have some elements in common.
            textual_debug parameter is the tool to turn of/on all of the logs (not visual ones) at
                one shot.
            visual_debug parameter is the tool to turn of/on all of the visual logs at one shot.
            show_file is the tool to show the file that the log funtion is running at in each log.
            show_line is the tool to show the line that the log funtion is running at in each log.

        '''
        self.__visual_debug: bool = visual_debug
        self.__textual_debug: bool = textual_debug
        self.__show_file: bool = show_file
        self.__show_line: bool = show_line
        self.__categories: List[str] = categories
        self.__time_stack: List[Tuple[str, float]] = []
        self.__start_tabs: int = 0
        self.__frame = inspect.getouterframes(inspect.currentframe())[1].frame
        self.__log_start('Debugger init')

    def log(self, desc: str, categories: List[str] = []):
        '''
            You can use this function to log an event in console.
            You just have two parameters here. desc is the description
                of your event and categories is the list of events, that
                this log is related to (then you can set categories parameter
                in constructor to see every log from some specific categories)
            - desc is the description of the log.
            - categories is a list or set of some strings that specifies the
                categories that this log belong's to them.
        '''
        self.__frame = inspect.getouterframes(inspect.currentframe())[1].frame
        _ , last_time = self.__time_stack[-1]
        if self.__textual_debug and self.__is_in_categories(categories):
            self.__print(desc, self.__get_line_info(),
                         Debugger.__get_time_info(time.time()-last_time))


    def log_start(self, desc: str, categories: List[str] = []):
        '''
            This funtion is like a simple log but here, you are specifying that
                some process has been started. Then you see passed time of all logs after 
                that, with respect to this log.
            - desc is the description of the log.
            - categories is like categories in log function.

        '''
        self.__frame = inspect.getouterframes(inspect.currentframe())[1].frame
        self.__log_start(desc, categories)

    def log_end(self, categories: List[str] = []):
        '''
            This funtion is like a simple log but here, you are specifying that
                last process has been ended. We don't have any description as 
                you see the description of the process that have been ended.
            - categories is like categories in log function.
        '''
        self.__frame = inspect.getouterframes(inspect.currentframe())[1].frame
        if self.__start_tabs == 0:
            raise Exception('There is no proccess to end it ' +
                            self.__get_line_info())
        self.__start_tabs -= 1

        last_desc, last_time = self.__time_stack.pop()
        if self.__textual_debug and self.__is_in_categories(categories):
            self.__print(last_desc + ' ended', self.__get_line_info(),
                         Debugger.__get_time_info(time.time()-last_time))

    def log_image(self, desc: str, image: np.ndarray, categories: List[str] = []):
        '''
            This funtion is like a simple log but here, you show some picture too.
            - desc is the title of the image.
            - image is the image that you want to show as a np array format.
            - categories is like categories in log function.
        '''
        self.log(desc, categories)
        if self.__visual_debug and self.__is_in_categories(categories):
            plt.imshow(image)
            plt.title(desc)
            plt.show()

    def log_images(self, images: List[np.ndarray], descs: List[str] = None, dim: Tuple = None, categories: List[str] = []):
        '''
            This funtion is like a simple log but here, you feed some pictures as
                a list of np arrays.
            - images is the list of np arrays.
            - descs is title of those images.
            - dim is dimentions of the grid that you want to see the pictures in it (by default,
                log_images show the images in a 1-row grid)
            - categories is like categories in log function.
        '''
        self.log('', categories)
        if self.__visual_debug and self.__is_in_categories(categories):
            fig = plt.figure()
            for i in range(len(images)):
                if dim is None:
                    fig.add_subplot(1, len(images), i+1)
                else:
                    fig.add_subplot(dim[0], dim[1], i+1)
                plt.imshow(images[i])
                plt.axis('off')
                if descs is not None and len(descs) > i:
                    plt.title(descs[i])
            plt.show()

    def __del__(self):
        self.log_end()

    def __is_in_categories(self, categories: Iterable):
        if categories is None or len(categories) == 0:
            return True
        elif len(set(categories).intersection(set(self.__categories))) > 0:
            return True
        else:
            return False

    def __get_line_info(self):
        file_name, line_num = self.__frame.f_code.co_filename, self.__frame.f_lineno
        result = '/{}'.format(
            file_name[file_name.rfind('\\')+1:]) if self.__show_file else ""
        result += '/line {}'.format(line_num) if self.__show_line else ""
        result = result[1:]
        if len(result) == 0:
            return ""
        return '['+result+']'

    def __get_time_info(t):
        return ('time = {:.4f}'.format(t))

    def __print(self, desc: str = '', line_info: str = '', time_info: str = ''):
        tabs = self.__start_tabs*'\t'
        print(tabs + line_info + ' ' + desc + ' ' + time_info)

    def __log_start(self, desc: str, categories: List[str] = []):
        self.__time_stack.append((desc, time.time()))
        if self.__textual_debug and self.__is_in_categories(categories):
            self.__print(desc + ' started', self.__get_line_info())
        self.__start_tabs += 1

    