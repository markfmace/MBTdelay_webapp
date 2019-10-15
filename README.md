# MBTdelay_webapp
MBTdelay_webapp is the web-app interface for delay forecasting on the MBTA's Green Line using LightGBM based models and DarkSky weather predictions. Currently deployed on an AWS EC2 instance. 


### Prerequisites

Need to ``pip install``

```
arrow, io, flask, lightgbm, numpy, pandas, requests
```

## Deployment

Once all libraries are installed, to run, the ``BASE`` directory must be established in ``mbtdelay/my_app.py`` and ``mbtdelay/views.py`` . A DarkSky dev API key, ``MY_DS_KEY``,  must be specified in ``mbtdelay/my_app.py``.

Then to run
```
./run.sh
```

Note that for running on an AWS instance, in ``run.py``
```
app.run(debug=True)
```
must be changed to
```
app.run(debug=True,host='0.0.0.0')
```

## Author
* **Mark Mace** - [email](mailto:mark.f.mace@gmail.com) - [GitHub](https://github.com/markfmace) - [Website](https://mbtdelay.xyz)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
MIT License

Copyright (c) 2019 Mark Mace

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
