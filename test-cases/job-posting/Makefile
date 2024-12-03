# Default target name if not specified
TARGET_NAME ?= human-seleted-1

# Number of runs
RUNS = 3

# Create directories and run the script multiple times
.PHONY: all
all: setup
	for i in $$(seq 1 $(RUNS)); do \
		echo "Running iteration $$i..."; \
		poetry run job_posting; \
		mkdir -p $(TARGET_NAME)/$$i; \
		mv -f agentops.log $(TARGET_NAME)/$$i/ 2>/dev/null || true; \
		mv -f log.txt $(TARGET_NAME)/$$i/ 2>/dev/null || true; \
		mv -f answer.md $(TARGET_NAME)/$$i/ 2>/dev/null || true; \
	done

# Setup directory structure
.PHONY: setup
setup:
	mkdir -p $(TARGET_NAME)

# Clean up all generated directories and files
.PHONY: clean
clean:
	rm -rf $(TARGET_NAME)
