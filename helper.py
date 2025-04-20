import argparse
import os
import random
from time import sleep

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.align import Align

CONSOLE = Console()

def reset_progress():
    """
    Reset the progress of AlgoDailyDose by removing all entries from the logs part of 
    README.md and moving them to Planned problems to complete someday.
    """
    with open("README.md", "r") as file, open("README.md.tmp", "w") as temp_file:
        CONSOLE.print("[bold red]Resetting progress...[/bold red]")
        
        # Find all the problems in the logs section
        start_log = False
        finished_log = False
        start_planned = False
        finished_planned = False
        problems_to_move = []

        process = CONSOLE.status("[green]Finding logs section...[/green]", spinner="dots")
        process.start()
        
        while True:
            line = file.readline()
            if not line:
                if not start_log:
                    CONSOLE.log("[red]No logs section found in README.md.[/red]")
                    CONSOLE.print("[red]Please make sure README.md has the correct format.[/red]")
                    return
                elif not start_planned:
                    CONSOLE.log("[red]No planned problems section found in README.md.[/red]")
                    CONSOLE.print("[red]Please make sure README.md has the correct format.[/red]")
                    return
                break

            if not finished_log:                
                if not start_log:
                    if line == "| Date | Problem | Source | Topic | Notes | Difficulty | Solution Link |\n":
                        temp_file.write(line)
                        line = file.readline()
                        start_log = True
                        
                        process.stop()
                        CONSOLE.log("[yellow]Found logs section.[/yellow]")
                        process = CONSOLE.status("[green]Saving problems from logs section...[/green]", spinner="dots")
                        process.start()
                    
                    temp_file.write(line)
                else:
                    if line == "\n":
                        temp_file.write(line)
                        finished_log = True
                        
                        process.stop()
                        CONSOLE.log("[yellow]All problems from logs section saved.[/yellow]")
                        process = CONSOLE.status("[green]Finding planned problems section...[/green]", spinner="dots")
                        process.start()
                    else:
                        data = line.split("|")
                        problem = data[2].strip()
                        source = data[3].strip()
                        problems_to_move.append((problem, source))
            elif not finished_planned:
                if not start_planned:
                    if line == "| Problem Name | Source |\n":
                        temp_file.write(line)
                        line = file.readline()
                        start_planned = True
                        
                        process.stop()
                        CONSOLE.log("[yellow]Found planned problems section.[/yellow]")
                        process = CONSOLE.status("[green]Finding the end of planned problems table...[/green]", spinner="dots")
                        process.start()
                else:
                    if line == "\n":
                        CONSOLE.log("[yellow]Found the end of planned problem section.[/yellow]")
                        process.stop()
                        process = CONSOLE.status("[green]Saving problems to planned problems section...[/green]", spinner="dots")
                        
                        for problem, source in problems_to_move:
                            temp_file.write(f"| {problem} | {source} |\n")
                        
                        process.stop()
                        CONSOLE.log("[yellow]All problems moved to planned problems section.[/yellow]")
                        process = CONSOLE.status("[green]Saving rest of the file...[/green]", spinner="dots")
                        process.start()
                        
                        temp_file.write(line)
                        finished_planned = True
                temp_file.write(line)
            else:
                temp_file.write(line)

    os.remove("README.md")
    os.rename("README.md.tmp", "README.md")
    process.stop()
    CONSOLE.log("[yellow]Finished saving changes to README.md.[/yellow]")
    CONSOLE.print("[bold green]Progress reset successfully![/bold green]")

def suspenseful_reveal():
    """Creates a suspenseful reveal sequence using rich."""

    with Progress(
        SpinnerColumn(spinner_name="earth"), 
        TextColumn("[bold blue]{task.description}", justify="center"),
        transient=True,
        console=CONSOLE
    ) as progress:
        task_id = progress.add_task(description="Initializing suspense...", total=None)
        sleep(1)
        progress.update(task_id, description="Peeking into the problem pool...")
        sleep(1.5)
        progress.update(task_id, description="Shuffling through possibilities...")
        sleep(1)

    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[bold yellow]{task.description}", justify="center"),
        transient=True,
        console=CONSOLE
    ) as progress:
        task_id = progress.add_task(description="Narrowing down the options...", total=None)
        sleep(1)
        progress.update(task_id, description="Closing in on the perfect challenge...")
        sleep(1.5)

def get_random_problem(logs=False, planned=True):
    """
    Get a random problem from the logs or planned problems.
    """
    type = ""
    if logs and planned:
        type = "both finished and planned problems"
    elif logs:
        type = "finished problems"
    elif planned:
        type = "planned problems"
    else:
        CONSOLE.log("[red]No problems to select from.[/red]")
        CONSOLE.print("[bold red] Try to solve this: 'Is P=NP?'[/bold red]")
        return
    
    CONSOLE.print(f"[bold yellow]Getting a random problem from {type}...[/bold yellow]")

    problems = []
    process = CONSOLE.status(f"[green]Finding {type}...[/green]", spinner="dots")
    process.start()
    with open("README.md", "r") as file:
        while True:
            line = file.readline()
            if not line:
                process.stop()
                if not problems:
                    CONSOLE.log("[red]No problems found in README.md.[/red]")
                    CONSOLE.print("[red]Please make sure README.md has the correct format.[/red]")
                    return
                break

            if logs and line == "| Date | Problem | Source | Topic | Notes | Difficulty | Solution Link |\n":
                _ = file.readline()
                while True:
                    line = file.readline()
                    if line == "\n":
                        break
                    data = line.split("|")
                    problem = data[2].strip()
                    problems.append(problem)
            elif planned and line == "| Problem Name | Source |\n":
                _ = file.readline()
                while True:
                    line = file.readline()
                    if line == "\n":
                        break
                    data = line.split("|")
                    problem = data[1].strip()
                    problems.append(problem)
    
    CONSOLE.print(f"[bold yellow]Selecting a random problem from {len(problems)}...[/bold yellow]")

    problem = random.choice(problems)

    problem_name_end_index = problem.find("]")
    problem_name = problem[1:problem_name_end_index]
    problem_url = problem[problem_name_end_index + 2:-1]

    CONSOLE.print("\n")
    suspenseful_reveal()

    problem_panel = Panel(
        f"[bold green]Problem Name:[/bold green] [yellow]{problem_name}[/yellow]\n[bold green]URL:[/bold green] [yellow]{problem_url}[/yellow]",
        title="[bold green]The Problem Is[/bold green]",
        border_style="green",
    )
    CONSOLE.print(problem_panel)
    CONSOLE.print("[bold yellow]Good luck solving it![/bold yellow]\n", justify="center")

def mark_as_finished():
    pass

def mark_as_unfinished():
    pass

def main():
    parser = argparse.ArgumentParser(description="Helper script to manage AlgoDailyDose.")
    parser.add_argument(
        "--action", 
        choices=[
            "reset", # To reset the progress
            "random_unfinished_problem", # To get a randomly selected unfinished problem
            "random_finished_problem", # To get a randomly selected finished problem
            "random_any_problem", # To get a randomly selected problem
            "mark_as_finished", # To move a problem to the finished list
            "mark_as_unfinished", # To move a problem to the unfinished list
        ],
        required=True,
        help="Specify the action to perform. Options are: " \
            "'reset', 'random_unfinished_problem', 'random_finished_problem', " \
            "'random_any_problem', 'mark_as_finished', 'mark_as_unfinished'."
    )

    args = parser.parse_args()
    action = args.action

    if action == "reset":
        reset_progress()
    elif action == "random_unfinished_problem":
        get_random_problem(logs=False, planned=True)
    elif action == "random_finished_problem":
        get_random_problem(logs=True, planned=False)
    elif action == "random_any_problem":
        get_random_problem(logs=True, planned=True)
    elif action == "mark_as_finished":
        mark_as_finished()
    elif action == "mark_as_unfinished":
        mark_as_unfinished()
    else:
        CONSOLE.print("[red]Invalid action specified.[/red]")
        parser.print_help()
        return

if __name__ == '__main__':
    main()