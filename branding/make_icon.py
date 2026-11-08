#!/usr/bin/env python3
"""Resizes the original Mikajy logo (branding/logo-512.png) to logo-1024.png, preserving its artwork. Mikajy Max has its own: make_max_icon.py."""
from pathlib import Path
from PIL import Image
here=Path(__file__).resolve().parent
original=Image.open(here/'logo-512.png').convert('RGB')
original.resize((1024,1024),Image.Resampling.LANCZOS).save(here/'logo-1024.png',optimize=True)
# The launcher icon of this branch is the Mikajy Max logo: run make_max_icon.py for it (this script no longer overwrites it).
print('logo-1024 updated')
