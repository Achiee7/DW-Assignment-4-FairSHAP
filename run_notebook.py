"""Execute the notebook from start to finish and retain its outputs."""
from pathlib import Path
import asyncio
import sys
import nbformat
from nbclient import NotebookClient

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

root = Path(__file__).parent
path = root / 'Assignment 4 FairSHAP.ipynb'
notebook = nbformat.read(path, as_version=4)
def completed(cell, cell_index, **kwargs):
    print(f'Completed cell {cell_index + 1}', flush=True)
client = NotebookClient(notebook, timeout=2400, kernel_name='python3',
                        resources={'metadata': {'path': str(root)}},
                        on_cell_executed=completed)
try:
    client.execute()
finally:
    nbformat.write(notebook, path)
print('Saved executed notebook', flush=True)
