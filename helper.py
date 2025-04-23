import argparse
import os
import shutil
import random
import datetime
from time import sleep
from getkey import getkey, keys

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.console import Console
from rich.prompt import Prompt

CONSOLE = Console()
IDENTIFIER_LINE_FOR_LOGS = "| Date | Problem | Source | Topic | Notes | Difficulty | Solution Link |\n"
IDENTIFIER_LINE_FOR_PLANNED = "| Problem Name | Source |\n"

def get_name_and_url_from_md_link(problem):
    """
    Extract the problem name and URL from the given problem string.
    """
    problem_name_end_index = problem.find("]")
    problem_name = problem[1:problem_name_end_index]
    problem_url = problem[problem_name_end_index + 2:-1]
    return problem_name, problem_url

def find_problems(log=False, planned=True, source=False):
    """
    Find a problem in the logs or planned problems.
    """
    include_source = source
    type = ""
    if log and planned:
        type = "both finished and planned problems"
    elif log:
        type = "finished problems"
    elif planned:
        type = "planned problems"
    else:
        CONSOLE.log("[red]No problems to select from.[/red]")
        return
    
    CONSOLE.print(f"[bold yellow]Finding a problem from {type}...[/bold yellow]")

    problems = []
    process = CONSOLE.status(f"[green]Finding {type}...[/green]", spinner="dots")
    process.start()

    end_log = False
    end_planned = False
    
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

            if log and line == IDENTIFIER_LINE_FOR_LOGS:
                _ = file.readline()
                while True:
                    line = file.readline()
                    if line == "\n":
                        end_log = True
                        break
                    data = line.split("|")
                    problem = data[2].strip()
                    source = data[3].strip()
                    name, url = get_name_and_url_from_md_link(problem)
                    problems.append((name, url) if not include_source else (name, url, source))
            elif planned and line == IDENTIFIER_LINE_FOR_PLANNED:
                _ = file.readline()
                while True:
                    line = file.readline()
                    if line == "\n":
                        end_planned = True
                        break
                    data = line.split("|")
                    problem = data[1].strip()
                    source = data[2].strip()
                    name, url = get_name_and_url_from_md_link(problem)
                    problems.append((name, url) if not include_source else (name, url, source))
            elif (not log or end_log) and (not planned or end_planned):
                process.stop()
                break

    CONSOLE.print(f"[bold yellow]Found {len(problems)} problems from {type}...[/bold yellow]")

    return problems

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

    shutil.rmtree("solutions")
    os.mkdir("solutions")

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
    problems = find_problems(logs, planned, source=False)
    if not problems:
        CONSOLE.print("[red]No problems found.[/red]")
        return

    problem_name, problem_url = random.choice(problems)

    CONSOLE.print("\n")
    suspenseful_reveal()

    os.makedirs("solutions", exist_ok=True)
    folder_name = problem_name.replace(" ", "_")
    CONSOLE.print(f"[bold green]Creating folder for the problem...[/bold green]")
    if os.path.exists(f"./solutions/{folder_name}"):
        CONSOLE.print(f"[bold red]Folder for the problem already exists. Please delete it before proceeding.[/bold red]")
        return
    os.makedirs(f"./solutions/{folder_name}")
    shutil.copytree("template", f"./solutions/{folder_name}", dirs_exist_ok=True)
    CONSOLE.print(f"[bold green]Folder created successfully![/bold green]")

    problem_panel = Panel(
        f"[bold green]Problem Name:[/bold green] [yellow]{problem_name}[/yellow]\n[bold green]URL:[/bold green] [yellow]{problem_url}[/yellow]",
        title="[bold green]The Problem Is[/bold green]",
        border_style="green",
    )
    CONSOLE.print(problem_panel)
    CONSOLE.print(f"[italic]Write your solution is the ./solutions/{folder_name} folder.[/italic]")
    CONSOLE.print("[bold yellow]Good luck solving it![/bold yellow]\n", justify="center")

def get_suggested_problems(user_input, problems):
    """
    Function to get suggested problems based on user input.
    """
    if user_input == "":
        return problems
    
    user_input = user_input.lower()
    results = []
    for problem, index in problems:
        if user_input in problem[0].lower():
            results.append((problem, index))

    return results

def problems_to_display_text(problems, select=None):
    final_text = ""
    if select == None:
        select = len(problems)

    if len(problems) == 0:
        return "[red bold]No problems found. Are you sure the problem you are searching for exists?[/red bold]"

    for i, problem_info in enumerate(problems):
        color = "yellow" if i != select else "blue"
        final_text += f"[{color}][bold]Problem {problem_info[1]+1}:[/bold] {problem_info[0][0]}:{problem_info[0][1]}[/{color}]\n"
    
    return final_text

def problem_select_ui(problems):
    user_input = ""

    layout = Layout()
    layout.split_column(
        Layout(Panel(f"[green] Search for a problem using related word and use arrow key to scroll through suggested problems and enter to select the problem [/green]", title="Instructions", border_style="green"), name="Instructions", size=3),
        Layout(name="logs"),
        Layout(name="input", size=3),
    )

    problems_to_display = problems
    search_cursor = True
    selected = len(problems)

    with Live(layout, refresh_per_second=10, console=CONSOLE) as live:
        while True:
            render_map = layout.render(CONSOLE, CONSOLE.options)
            region = render_map[layout["logs"]].region
            height = region.height
            log_text = problems_to_display_text(problems_to_display[:height-2], select=selected)
            layout["logs"].update(Panel(f"[yellow]{log_text}[/yellow]", title="Suggested Problems", border_style="yellow"))
            layout["input"].update(Panel(f"[bold blue]Search for a problem:[/bold blue] {user_input}" + ("█" if search_cursor else ""), title="Input", border_style="blue"))
            
            key = getkey()
            if key.isprintable():
                user_input += key
                problems_to_display = get_suggested_problems(user_input, problems_to_display)
                selected = len(problems_to_display)
                search_cursor = True
            elif key == keys.ENTER:
                if not search_cursor and selected > -1 and selected < len(problems_to_display):
                    break
            elif key == keys.BACKSPACE:
                user_input = user_input[:-1]
                problems_to_display = get_suggested_problems(user_input, problems)
                selected = len(problems_to_display)
                search_cursor = True
            elif key == keys.UP:  
                search_cursor = False
                if selected > 0:
                    selected = selected - 1
                else:
                    selected = len(problems_to_display)
                    search_cursor = True
            elif key == keys.DOWN: 
                if search_cursor:
                    selected = -1

                search_cursor = False
                if selected < len(problems_to_display) - 1:
                    selected = selected + 1
                else:
                    selected = len(problems_to_display)
                    search_cursor = True
    
    CONSOLE.clear()
    selected_problem = problems_to_display[selected]
    CONSOLE.print(f"[yellow][bold]Selected Problem:[/bold] {selected_problem[0][0]}[/yellow]")
    return selected_problem

def mark_as_finished():
    """
    Mark a problem as finished by moving it from the planned section to the logs section.
    """
    problems = find_problems(log=False, planned=True, source=True)
    problems = [(problem, index) for index, problem in enumerate(problems)]

    selected_problem = problem_select_ui(problems)
    while True:
        user_confirmation = Prompt.ask(
            "[italic]Is the selected problem the one you want to mark as finished?[/italic]", 
            choices=["y", "n", "q"], 
            default="n"
        )
        if user_confirmation == "y":
            break
        elif user_confirmation == "n":
            selected_problem = problem_select_ui(problems)
        elif user_confirmation == "q":
            CONSOLE.print("[red]Exiting...[/red]")
            return
        else:
            CONSOLE.print("[red]Invalid input. Please try again.[/red]")
            continue
    
    problem_info, problem_index = selected_problem[0], selected_problem[1]
    problem_name, problem_url, source = problem_info

    CONSOLE.print(f"[bold green]Marking problem as finished...[/bold green]")
    CONSOLE.print(f"[bold green]Problem Name:[/bold green] {problem_name}")
    CONSOLE.print(f"[bold green]Problem URL:[/bold green] {problem_url}")

    folder_name = problem_name.replace(" ", "_")
    if not os.path.exists(f"./solutions/{folder_name}"):
        CONSOLE.print(f"[bold red]Folder for the problem does not exist. Please create a folder named {folder_name} in the solutions directory.[/bold red]")
        return
    
    CONSOLE.print(f"[bold green]Folder for the problem exists. Proceeding to mark as finished...[/bold green]")

    date = datetime.date.today()
    date_str = date.strftime("%Y-%m-%d")
    topics = Prompt.ask("[bold yellow]Enter the topics covered in this problem (comma-separated)[/bold yellow]").split(",")
    topics = ', '.join([f'`{topic.strip()}`' for topic in topics])
    notes = Prompt.ask("[bold yellow]Enter any notes you want to add[/bold yellow]", default="No notes")
    difficulty = Prompt.ask("[bold yellow]Enter the difficulty level of this problem[/bold yellow]", choices=["easy", "medium", "hard"])
    if difficulty == "easy":
        difficulty = "$${\\color{green}\\text{Easy}}$$"
    elif difficulty == "medium":
        difficulty = "$${\\color{yellow}\\text{Medium}}$$"
    elif difficulty == "hard":
        difficulty = "$${\\color{red}\\text{Hard}}$$"
    solution_link = f"[Solution](./solutions/{folder_name})"

    new_log_entry = f"| {date_str} | [{problem_name}]({problem_url}) | {source} | {topics} | {notes} | {difficulty} | {solution_link} |\n"

    with open("README.md", "r") as file, open("README.md.tmp", "w") as temp_file:
        process = CONSOLE.status("[green]Saving changes to README.md...[/green]", spinner="dots")
        process.start()

        while True:
            line = file.readline()
            if not line:
                break

            if line == IDENTIFIER_LINE_FOR_LOGS:
                temp_file.write(line)
                while True:
                    line = file.readline()
                    if line == "\n":
                        temp_file.write(new_log_entry)
                        temp_file.write(line)
                        break
                    temp_file.write(line)
            elif line == IDENTIFIER_LINE_FOR_PLANNED:
                temp_file.write(line)
                dash_line = file.readline()
                temp_file.write(dash_line)
                index = -1
                while True:
                    line = file.readline()
                    index += 1
                    if index == problem_index:
                        continue
                    temp_file.write(line)
                    if line == "\n":
                        break

            else:
                temp_file.write(line)
        process.stop()
    
    os.remove("README.md")
    os.rename("README.md.tmp", "README.md")
    CONSOLE.print("[bold green]Problem marked as finished![/bold green]")
    CONSOLE.print("[italic yellow]Congratulations on completing the problem![/italic yellow]")
    CONSOLE.print("[bold green]Happy coding![/bold green]")

def mark_as_unfinished():
    """
    Mark a problem as unfinished by moving it from the logs section to the planned problems section.
    """
    problems = find_problems(log=True, planned=False, source=True)
    problems = [(problem, index) for index, problem in enumerate(problems)]

    selected_problem = problem_select_ui(problems)
    while True:
        user_confirmation = Prompt.ask(
            "[italic]Is the selected problem the one you want to mark as unfinished?[/italic]", 
            choices=["y", "n", "q"], 
            default="n"
        )
        if user_confirmation == "y":
            break
        elif user_confirmation == "n":
            selected_problem = problem_select_ui(problems)
        elif user_confirmation == "q":
            CONSOLE.print("[red]Exiting...[/red]")
            return
        else:
            CONSOLE.print("[red]Invalid input. Please try again.[/red]")
            continue
    
    problem_info, problem_index = selected_problem[0], selected_problem[1]
    problem_name, problem_url, source = problem_info[0], problem_info[1], problem_info[2] 

    CONSOLE.print(f"[bold green]Marking problem as unfinished...[/bold green]")
    CONSOLE.print(f"[bold green]Problem Name:[/bold green] {problem_name}")
    CONSOLE.print(f"[bold green]Problem URL:[/bold green] {problem_url}")

    confirmation = Prompt.ask("[bold red]Are you sure you want to mark this problem as unfinished? Doing so will result in deletion of any related folder[/bold red]", choices=["y", "n"], default="n")
    if confirmation == "n":
        CONSOLE.print("[red]Exiting...[/red]")
        return

    folder_name = problem_name.replace(" ", "_")
    if os.path.exists(f"./solutions/{folder_name}"):
        shutil.rmtree(f"./solutions/{folder_name}")
        CONSOLE.print(f"[bold green]Folder for the problem deleted successfully.[/bold green]")

    new_planned_entry = f"| [{problem_name}]({problem_url}) | {source} |\n"

    with open("README.md", "r") as file, open("README.md.tmp", "w") as temp_file:
        process = CONSOLE.status("[green]Saving changes to README.md...[/green]", spinner="dots")
        process.start()

        while True:
            line = file.readline()
            if not line:
                break

            if line == IDENTIFIER_LINE_FOR_LOGS:
                temp_file.write(line)
                dash_line = file.readline()
                temp_file.write(dash_line)
                index = -1
                while True:
                    line = file.readline()
                    index += 1
                    if index == problem_index:
                        continue
                    temp_file.write(line)
                    if line == "\n":
                        break
            elif line == IDENTIFIER_LINE_FOR_PLANNED:
                temp_file.write(line)
                while True:
                    line = file.readline()
                    if line == "\n":
                        temp_file.write(new_planned_entry)
                        temp_file.write(line)
                        break
                    temp_file.write(line)
            else:
                temp_file.write(line)
        process.stop()
    
    os.remove("README.md")
    os.rename("README.md.tmp", "README.md")
    CONSOLE.print("[bold green]Problem marked as unfinished![/bold green]")
    CONSOLE.print("[italic yellow]Good luck with your future coding challenges![/italic yellow]")
    CONSOLE.print("[bold green]Happy coding![/bold green]")

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