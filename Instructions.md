# 🛠️ How to Dominate This Repo Like a Pro

Welcome, `AlgoDailyDose`! Ready to crush your daily grind and flex those problem-solving muscles? This repo is your ultimate sidekick. Let’s get you set up for algorithmic glory. 🚀

## ✨ Fork It, Clone It, Own It

Want this repo to be yours? Fork it, clone it, and you're good to go. You know the drill. Just remember to run:
```bash
make setup
make reset
```
The `make setup` command sets up your environment, and `make reset` clears all preexisting solutions, resets the log table, and moves all problems to the planned state. Boom, you're ready to roll.

## 🛠️ Makefile Magic: Automate Everything

This repo comes with a `Makefile` that’s basically your personal assistant. Here’s the cheat sheet:

### 🛠️ **Set It Up**
New machine? Fresh start? Run:
```bash
make setup
```
and you’re back in business.

### 🎲 **Summon a Random Problem**
Feeling lucky? Let the repo pick your next challenge:
```bash
make random_problem
```
- A random problem folder will appear like magic, complete with a `README.md` and `solution.py`. Customize the `template` folder if you want to add your own flair.

### 🔄 **Revisit the Pain**
Not satisfied with your solution? Mark it as unfinished:
```bash
make mark_unfinished
```

This command helps you organize and document your progress. When you run `make mark_finished`, it will:

1. Prompt you to select the problem you want to mark as finished.
2. Check if a solution folder exists for the selected problem.
3. Ask follow-up questions, such as:
   - The difficulty level of the problem.
   - The topics it covered.
   - Any personal notes you'd like to add for future reference.
4. Once all the details are provided, it will:
   - Move the problem from the "Planned" table to the "Log" table, keeping your progress tracker up to date.

### 🔄 **Revisit the Pain**
Not satisfied with your solution? Mark it as unfinished:
```bash
make mark_unfinished
```

This command helps you revisit problems that need more work. When you run `make mark_unfinished`, it will:

1. Prompt you to select the problem you want to mark as unfinished.
2. Remove any related solution files for the selected problem.
3. Move the problem from the "Log" table back to the "Planned" table, giving you a fresh start.

Use this to refine your skills and tackle challenges with a new perspective.

### 🧹 **Nuke It All**
Want a clean slate? Reset everything (logs, solutions, the works):
```bash
make reset
```
Use this wisely—there’s no undo button.


---

## 🖋️ Pimp Your Template

The `template` folder is your playground. Want every new problem to come with a motivational quote? Go for it. Make it yours.

## 🧩 Pro Tips for Algorithm Domination

- **Consistency is Key**: One problem a day keeps the rust away.
- **Document Like a Boss**: Use the `README.md` to jot down your genius ideas.
- **Track Your Wins**: Update the logs in the main `README.md` to show off your progress.

## 🤝 Contribute or Die Trying

Think you can make this repo better? Prove it:
- Add cooler `Makefile` commands.
- Upgrade the `template` folder.
- Share your algorithm hacks.

## 🧃 Final Words of Wisdom

This repo is your dojo. Customize it, automate it, and make it your own. Now go forth and conquer those algorithms like the legend you are. 💪
