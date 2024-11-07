CC = gcc
CFLAGS = -Wall -Wextra

all: fork_example

fork_example: fork_example.c
	$(CC) $(CFLAGS) -o $@ $<

run: fork_example
	./fork_example

clean:
	rm -f fork_example

.PHONY: all run clean

