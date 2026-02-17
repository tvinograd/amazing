# To be added:

# - install: Install project dependencies using pip, uv, pipx, or any other package manager of your choice.
# - run: Execute the main script of your project (e.g., via Python interpreter).
# - debug: Run the main script in debug mode using Python’s built-in debugger (e.g., pdb).
# - clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the project environment clean.
# - lint: Execute the commands flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
# - lint-strict (optional): Execute the commands flake8 . and mypy . --strict

DIRS_TO_CLEAN = __pycache__ .mypy_cache
FILES_TO_CLEAN = *.pyc

install:
	uv pip install flake8 mypy

run:
	python3 a_maze_ing.py

debug:
	python3 -m pdb a_maze_ing.py

clean:
	@echo cleaning... "\n"removing $(DIRS_TO_CLEAN) $(FILES_TO_CLEAN)
	@find . -mindepth 1 \( \
		-type d \( $(foreach d,$(DIRS_TO_CLEAN),-name "$(d)" -o ) -false \) -o \
		-type f \( $(foreach f,$(FILES_TO_CLEAN),-name "$(f)" -o ) -false \) \
	\) -exec rm -rf {} +
	@echo ...cleaning is finished!

lint:
	flake8 . --exclude venv,.venv,env,.env
	mypy . --exclude venv,.venv,env,.env --warn-return-any \
		   --warn-unused-ignores --ignore-missing-imports \
		   --disallow-untyped-defs --check-untyped-defs
	# if there are no issues we reach the following line
	@echo There are no issues!

lint-strict:
	flake8 . --exclude venv,.venv,env,.env
	mypy . --exclude venv,.venv,env,.env --strict
	# if there are no issues we reach the following line
	@echo There are no issues!

.PHONY: install run debug clean lint lint-strict
