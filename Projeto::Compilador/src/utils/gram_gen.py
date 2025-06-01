def extrair_docstrings(filepath):
    docstrings = []
    inside_docstring = False
    current_docstring = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('"""') and stripped.endswith('"""') and len(stripped) > 3:
                # linha única com docstring
                docstrings.append(stripped[3:-3])
            elif stripped.startswith('"""') and not inside_docstring:
                inside_docstring = True
                current_docstring.append(stripped[3:])
            elif stripped.endswith('"""') and inside_docstring:
                current_docstring.append(stripped[:-3])
                docstrings.append('\n'.join(current_docstring))
                current_docstring = []
                inside_docstring = False
            elif inside_docstring:
                current_docstring.append(line.rstrip())

    return '\n'.join(docstrings)


if __name__ == "__main__":
    caminho = "pascal_anasin.py"
    resultado = extrair_docstrings(caminho)
    print(resultado)
