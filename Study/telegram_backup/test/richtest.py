from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from time import sleep

progress = Progress(
    # *Progress.get_default_columns(),
    BarColumn(),
    TextColumn("[bold blue]{task.percentage:>3.0f}%"),
    "ETA:",
    TimeRemainingColumn(),
)

with progress as progress:
    inner_task = progress.add_task("Inner Task", total=4)
    outer_task = progress.add_task("Outer Task", total=100)

    for i in range(100):
        sleep(0.1)
        progress.update(outer_task, advance=1)

        if i % 25 == 0:
            for j in range(4):
                sleep(0.2)
                progress.update(inner_task, advance=1)
