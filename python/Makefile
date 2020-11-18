.PHONY = all install
all:
	@echo
	@echo "To install type 'make install'"
	@echo

install:
	@chmod +x trening.py
	@cp trening.py ~/.local/bin/trening
	@cp terminal.py ~/.local/lib/
	@if [ -f ~/.local/share/trening.json ]; then echo "Have user data"; \
		else cp trening.json ~/.local/share/ && echo "User data created";  fi
