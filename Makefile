.PHONY = all install
all:
	@echo
	@echo "To install type 'make install'"
	@echo

install:
	@pip3 install columnar >/dev/null
	@pip3 install colored >/dev/null
	@cp trening.py ~/.local/bin/trening
	@if [ -f ~/.local/share/trening.json ]; then echo "Have user data"; \
		else cp trening.json ~/.local/share/ && echo "User data created";  fi
