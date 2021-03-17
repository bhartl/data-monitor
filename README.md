# A non-blocking matplotlib `data-monitor`
Data Monitoring of externally manipulated data (such as sensory-data or file-data)
- non-blocking (based on multiprocessing)
- multiple channels in real-time 
- based on `matplotlib` and `FuncAnimation` in `matplotlib.animation`.

Example code how is provided in the `data_monitor.py` and can be executed in the command line via
```bash
python data_monitor.py
```

The data-monitor runs matplotlib in an extra `multiprocessing.Process`.
For a clean subprocess handling it is recommended to use DataMonitor in the with environment:

```python
from data_monitor import DataMonitor

def get_data():
    # get data in format (x, *y) from elsewhere
    ...
    return data

with DataMonitor() as dm:
     while True:
         dm.data = get_data()
         
         # do something else
```

For custom configuration consider overwriting the `DataMonitor.plot` method.
