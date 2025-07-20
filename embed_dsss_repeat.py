import argparse, numpy as np, hashlib
from scipy.io import wavfile

def text_to_bits(text: str) -> str:
    return ''.join(f"{ord(c):08b}" for c in text) + '00000000'

def gen_prn(key: str, length: int) -> np.ndarray:
    h = hashlib.sha256(key.encode()).digest()
    seed = int.from_bytes(h[:4], 'little')
    rs = np.random.RandomState(seed)
    return rs.choice([-1.0, 1.0], size=length)

def embed(in_wav, out_wav, watermark, key, alpha, segsecs):
    rate, data = wavfile.read(in_wav)
    mono = data[:,0] if data.ndim>1 else data
    if mono.dtype.kind=='i':
        maxv = np.iinfo(mono.dtype).max
        x = mono.astype(np.float32)/maxv
    else:
        x = mono.astype(np.float32)

    bits = text_to_bits(watermark)
    seglen = int(segsecs * rate)
    total = len(bits)
    if seglen * total > len(x):
        raise ValueError("Audio too short for watermark")

    y = x.copy()
    for i, b in enumerate(bits):
        prn = gen_prn(f"{key}_{i}", seglen)
        delta = alpha * prn * (1 if b=='1' else -1)
        start = i*seglen
        y[start:start+seglen] += delta

    if mono.dtype.kind=='i':
        out = np.int16(np.clip(y * maxv, -maxv, maxv-1))
    else:
        out = y
    if data.ndim>1:
        o2 = np.zeros_like(data); o2[:,0]=out; o2[:,1]=data[:,1]; out=o2
    wavfile.write(out_wav, rate, out)

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("in_wav"); p.add_argument("out_wav"); p.add_argument("watermark")
    p.add_argument("--key",    default="secret")
    p.add_argument("--alpha",  type=float, default=0.1)
    p.add_argument("--segsecs",type=float, default=0.5)
    args = p.parse_args()
    embed(args.in_wav, args.out_wav, args.watermark,
          args.key, args.alpha, args.segsecs)
