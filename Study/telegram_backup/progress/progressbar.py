from rich.progress import Progress
from rich.progress import SpinnerColumn, DownloadColumn, TransferSpeedColumn, TimeElapsedColumn
'''
class progress_bar_old:
    def __init__(self) :
        self.total = None
        self.progress = Progress(SpinnerColumn(),     
                    *Progress.get_default_columns(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeElapsedColumn())

    def create_task(self):
        self.task = self.progress.add_task("[cyan]Uploading...", total=self.total)  
        self.progress.start()

    def update_progress(self,current_progress,total):
        # with self.progress:
        if(self.total==None):
            self.total = total
            self.create_task()
        # task = self.task
        # task = self.progress.add_task("[cyan]Uploading...", total=self.total)

        # Update progress with the current progress value and display transfer speed and ETA
        self.progress.update(self.task, completed=current_progress, transfer_speed="auto", eta="auto")

        # You can also display additional information using 'console.print'
        # console.print(f"Custom information: {i}", style="yellow", end="\r")

    def __del__(self):
        self.progress.stop()
'''

class progress_bar:
    def __init__(self,total,description="Uploading...",color="cyan") :
        self.total = total # total size of file
        self.progress = Progress(SpinnerColumn(),     
                    *Progress.get_default_columns(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeElapsedColumn())
        self.task = self.progress.add_task(f"[{color}]{description}", total=self.total)  
        self.progress.start()
        self.max_seg_prog = 0 # max progress of the current segment
        self.base_prog = 0 # max progress of a file
        # self.flag = False

    def update_base_progress(self):
        self.base_prog += self.max_seg_prog
        # self.flag = True
        self.max_seg_prog = 0

    def update_progress(self,current_progress,total):

        if(self.max_seg_prog>current_progress ):
            self.update_base_progress()
                
        self.max_seg_prog = current_progress    
        

        # Update progress with the current progress value and display transfer speed and ETA
        self.progress.update(self.task, completed=self.base_prog + current_progress, transfer_speed="auto", eta="auto")

        # You can also display additional information using 'console.print'
        # console.print(f"Custom information: {i}", style="yellow", end="\r")

    def __del__(self):
        self.progress.stop()