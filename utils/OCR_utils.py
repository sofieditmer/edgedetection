#!/usr/bin/env python
"""
Stores OCR function to use when performing object-character recognition with Pytesseract. This code was developed for use in class and has been adapted for this project.
"""

def replace(string):
    """
    Method that takes a string and performs basic preprocessing steps. 
    """
    processed = string.replace("\n"," ")\
    .replace("\n\n"," ")\
    .replace("__"," ")\
    .replace(" - "," ")\
    .replace('-""' ," ")\
    .replace("|", "")\
    .replace("!", "")\
    .replace("\s"," ")\
    .lstrip()

    return " ".join(processed.split())