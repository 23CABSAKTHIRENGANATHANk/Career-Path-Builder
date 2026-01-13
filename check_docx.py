import sys
try:
    import docx
    import PyPDF2
    import numpy
    with open('docx_check.txt', 'w') as f:
        f.write("SUCCESS: docx, PyPDF2, and numpy imported")
except Exception as e:
    with open('docx_check.txt', 'w') as f:
        f.write(f"FAILURE: {e}")
