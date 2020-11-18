.PHONY = all install

all:
	@echo
	@echo "To install type 'make install'"
	@echo

install:
	@cp trening.py ~/.local/bin/trening
	@cp terminal.py ~/.local/lib/
	@(test -f ~/.local/share/trening.json) || \
	cp trening.json ~/.local/bin/ && echo "Have user data"