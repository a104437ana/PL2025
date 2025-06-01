TEX_FILE = Relatorio.tex
BUILD_DIR = build
PDF_FILE = $(BUILD_DIR)/$(TEX_FILE:.tex=.pdf)
LATEX = pdflatex

ifeq ($(OS), Windows_NT)
	detected_OS := Windows
else
	detected_OS := $(shell uname)
endif

ifeq ($(detected_OS), Windows)
	RMDIR := cmd /c "rmdir /S /Q $(BUILD_DIR)"
endif
ifeq ($(detected_OS), Linux)
	RMDIR := rm -rf $(BUILD_DIR)
endif

all: $(PDF_FILE)

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

$(PDF_FILE): $(TEX_FILE) | $(BUILD_DIR)
	$(LATEX) -output-directory=$(BUILD_DIR) $(TEX_FILE)
	$(LATEX) -output-directory=$(BUILD_DIR) $(TEX_FILE)
	$(LATEX) -output-directory=$(BUILD_DIR) $(TEX_FILE)

clean:
	$(RMDIR)

.PHONY: all clean