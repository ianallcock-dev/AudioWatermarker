import argparse
import numpy as np
import hashlib
from scipy.io import wavfile

#Convert data into text, stopping at the first null byte (00000000).
def bits_to_text(bits: str) -> str:
    chars = []
    #Process bits in 8-bit cblocks
    for i in range(0, len(bits), 8):
        byte = bits[i : i + 8]
        #Stop at null terminator or if chunk is incomplete
        if byte == '00000000' or len(byte) < 8:
            break
        # Convert 8-bit binary string to character
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

#Use shared secret to generate random noise
def gen_prn(key: str, length: int) -> np.ndarray:
    # Hash the key to get a seed
    h = hashlib.sha256(key.encode()).digest()
    seed = int.from_bytes(h[:4], 'little')
    rs = np.random.RandomState(seed)
    # Return an array of ±1 values
    return rs.choice([-1.0, 1.0], size=length)

#Function to Read WAV and embed watermark
def extract(in_wav, key, alpha, segsecs):
    rate, data = wavfile.read(in_wav)
    #Convert to mono if stereo
    mono = data[:,0] if data.ndim > 1 else data
    #Normalize integer samples to float in [-1, 1]
    if mono.dtype.kind == 'i':
        maxv = np.iinfo(mono.dtype).max
        x = mono.astype(np.float32) / maxv
    else:
        x = mono.astype(np.float32)

    #Determine segment length in samples
    seglen = int(segsecs * rate)
    #How many full segments fit
    nsegs = len(x) // seglen

    bits = []
    #For each segment, regenerate the same PRN and compute correlation
    for i in range(nsegs):
        seg = x[i*seglen : (i+1)*seglen]
        prn = gen_prn(f"{key}_{i}", seglen)
        corr = np.dot(seg, prn)
        bits.append('1' if corr > 0 else '0')

    #Convert the recovered bitstream to text
    wm = bits_to_text(''.join(bits))
    if wm:
        print("Extracted watermark:", wm)
    else:
        print("No watermark found")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Extract DSSS watermark from WAV")
    p.add_argument("in_wav", help="Path to watermarked WAV file")
    p.add_argument("--key",    default="secret",
                   help="Shared secret key for PRN generation")
    p.add_argument("--alpha",  type=float, default=0.1,
                   help="Embedding strength (unused in extraction)")
    p.add_argument("--segsecs",type=float, default=0.5,
                   help="Seconds per bit segment (must match embed)")
    args = p.parse_args()

    extract(args.in_wav, args.key, args.alpha, args.segsecs)
