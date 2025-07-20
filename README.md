\# Audio DSSS Watermark



Embed and extract a simple DSSS (Direct-Sequence Spread Spectrum) watermark in WAV files.



\## Installation



No Git required—just upload these files to a new GitHub repo.



Install dependencies:

```bash

pip install -r requirements.txt



\*\*Usage\*\*

Embed



python embed\_dsss\_repeat.py samples/sample.wav samples/wm.wav "TOP-SECRET-123" --key mysecret --alpha 0.1 --segsecs 0.5



Extract

python extract\_dsss\_repeat.py samples/wm.wav --key mysecret --segsecs 0.5



MIT License



Copyright (c) 2025 Ian Allcock



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

