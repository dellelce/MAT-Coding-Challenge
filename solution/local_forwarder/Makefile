# Testing & Building standalone service

NAME    = $$(basename $$PWD)

help:
	@cat help.txt

build: Dockerfile
	@docker build -t $(NAME) .

# run here is expected only to be used for testing
run: build
	@docker run --rm  --name $(NAME) $(NAME)

kill:
	@docker kill $(NAME)

all: build run
