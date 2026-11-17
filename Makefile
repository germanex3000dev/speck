XXD     := xxd
PYTHON  := python3

all: null

# null.hex is the complete executable image, one byte per two hex digits.
null: null.hex
	$(XXD) -r -p $< $@
	chmod +x $@

check: null
	sha256sum -c null.sha256

test: null
	$(PYTHON) test_null.py

size: null
	@stat -c '%n: %s bytes' $<

clean:
	rm -f null

.PHONY: all check test size clean
