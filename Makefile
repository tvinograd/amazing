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
	@echo Checking with flake8...
	@flake8 . --exclude venv,.venv,env,.env
	@echo Success: no issues found by flake8

	@echo Checking with mypy...
	@mypy . --exclude venv,.venv,env,.env --warn-return-any \
		   --warn-unused-ignores --ignore-missing-imports \
		   --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo Checking with flake8...
	@flake8 . --exclude venv,.venv,env,.env
	@echo Success: no issues found by flake8

	@echo Checking with mypy --strict...
	@mypy . --exclude venv,.venv,env,.env --strict
	@# if there are no issues we reach the following line

.PHONY: install run debug clean lint lint-strict
