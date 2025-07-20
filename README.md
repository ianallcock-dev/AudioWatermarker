# Secure Audio Watermarking Tool

This repository implements a simple audio watermarking utility using Least Significant Bit (LSB) encoding. It allows embedding a short text watermark into a WAV file and extracting it reliably without perceptible audio artifacts.

## Project Structure

```
/audio-watermarking-tool
│
├── README.md
├── requirements.txt
├── embed_watermark.py
├── extract_watermark.py
├── utils.py
└── samples/
    ├── original.wav
    └── watermarked.wav
```

---

## 1. README.md

````markdown
# Secure Audio Watermarking Tool

This tool embeds and extracts hidden text watermarks in WAV audio files using LSB encoding.

## Features

- Embed arbitrary text watermarks into WAV files.
- Extract watermarks from watermarked files.
- Inaudible to human ears for short messages.

## Installation

```bash
pip install -r requirements.txt
````

## Usage

### Embed Watermark

```bash
python embed_watermark.py \
    --input samples/original.wav \
    --output samples/watermarked.wav \
    --watermark "TOP-SECRET-123"
```

### Extract Watermark

```bash
python extract_watermark.py \
    --input samples/watermarked.wav
```

## Future Work

* Encrypt watermark before embedding.
* Spread-spectrum and frequency-domain methods.
* Robustness against compression and trimming.
* Stereo-channel support.
* Web UI.

```

---

## 2. requirements.txt

```

numpy scipy pydub

````

---

## 3. utils.py

```python
import numpy as np

def text_to_bits(text: str) -> str:
    """
    Convert a string to a binary string representation.
    Each character to 8 bits, and append a null terminator.
    """
    bits = ''.join(format(ord(c), '08b') for c in text)
    return bits + '00000000'


def bits_to_text(bits: str) -> str:
    """
    Convert a binary string (multiple of 8 bits) to text,
    stopping at the null terminator.
    """
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == '\x00':
            break
        chars.append(char)
    return ''.join(chars)
````

---

## 4. embed\_watermark.py

```python
import argparse
import numpy as np
from scipy.io import wavfile
from utils import text_to_bits


def embed_watermark(input_wav: str, output_wav: str, watermark: str) -> None:
    # Read audio
    rate, data = wavfile.read(input_wav)

    # Use mono (left channel) if stereo
    if data.ndim > 1:
        data = data[:, 0]

    # Prepare bits
    watermark_bits = text_to_bits(watermark)

    if len(watermark_bits) > len(data):
        raise ValueError("Audio file too short to embed watermark.")

    # Embed bits into LSB of samples
    watermarked = np.array(data, copy=True)
    for i, bit in enumerate(watermark_bits):
        sample = watermarked[i]
        watermarked[i] = (sample & ~1) | int(bit)

    # Save result
    wavfile.write(output_wav, rate, watermarked.astype(data.dtype))
    print(f"Watermark embedded: '{watermark}' into {output_wav}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Embed text watermark into WAV file')
    parser.add_argument('--input', required=True, help='Path to original WAV')
    parser.add_argument('--output', required=True, help='Path to save watermarked WAV')
    parser.add_argument('--watermark', required=True, help='Text watermark')
    args = parser.parse_args()
    embed_watermark(args.input, args.output, args.watermark)
```

---

## 5. extract\_watermark.py

```python
import argparse
import numpy as np
from scipy.io import wavfile
from utils import bits_to_text


def extract_watermark(input_wav: str) -> str:
    rate, data = wavfile.read(input_wav)

    if data.ndim > 1:
        data = data[:, 0]

    # Extract LSBs
    bits = ''.join(str(sample & 1) for sample in data)

    # Convert to text
    watermark = bits_to_text(bits)
    return watermark


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract text watermark from WAV file')
    parser.add_argument('--input', required=True, help='Path to watermarked WAV')
    args = parser.parse_args()
    wm = extract_watermark(args.input)
    print(f"Extracted watermark: '{wm}'")
```

---

## 6. Getting Started

1. Place an audio file (`original.wav`) in `samples/`.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Embed a watermark:

   ```bash
   python embed_watermark.py --input samples/original.wav --output samples/watermarked.wav --watermark "TOP-SECRET-123"
   ```
4. Extract the watermark:

   ```bash
   python extract_watermark.py --input samples/watermarked.wav
   ```

Enjoy your secure audio watermarking MVP!


License
MIT License © 2025 Ian Allcock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
