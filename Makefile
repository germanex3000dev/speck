XXD     := xxd

all: speck

# speck.hex is the complete executable image, one byte per two hex digits.
speck: speck.hex
	$(XXD) -r -p $< $@
	chmod +x $@

size: speck
	@stat -c '%n: %s bytes' $<

clean:
	rm -f speck

.PHONY: all check size clean
