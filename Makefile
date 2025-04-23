random_problem:
	@./venv/bin/python3 helper.py --action random_any_problem

mark_finished:
	@./venv/bin/python3 helper.py --action mark_as_finished

mark_unfinished:
	@./venv/bin/python3 helper.py --action mark_as_unfinished

reset:
	@./venv/bin/python3 helper.py --action reset

setup:
	@python3 -m venv venv
	@. venv/bin/activate && pip install -r requirements.txt