from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from gzip import compress
from pathlib import Path
from sys import stdout


OUTPUT_WIDTH = 24


@dataclass
class GzipInput:
    index: int
    total: int
    src: Path
    dest: Path


@dataclass
class GzipOutput:
    size_original: int
    size_compressed: int

    @property
    def ratio(self):
        return self.size_compressed / self.size_original


def gzip_one(context: GzipInput):
    stdout.write("\r" + (f"{context.index} / {context.total}".rjust(OUTPUT_WIDTH)))
    if context.src.is_dir():
        context.dest.mkdir(parents=True, exist_ok=True)
        return None
    else:
        original = context.src.read_bytes()
        compressed = compress(original)
        context.dest.write_bytes(compressed)
        return GzipOutput(size_original=len(original), size_compressed=len(compressed))


def gzip(src: str, dest: str):
    src_root = Path(src)
    src_items = list(src_root.glob("**/*"))
    dest_root = Path(dest)
    total = len(src_items)

    with ProcessPoolExecutor() as p:
        results = p.map(
            gzip_one,
            (
                GzipInput(i, total, src, dest_root / src.relative_to(src_root))
                for i, src in enumerate(src_items)
            ),
        )
    stdout.write("\r".ljust(OUTPUT_WIDTH + 1))

    hist = defaultdict[float, int](lambda: 0)
    for result in results:
        if result:
            hist[round(result.ratio, 1)] += 1
    stdout.write("\rSize ratio distribution (compressed / original):\n")
    for bucket in sorted(hist):
        stdout.write(f"  {bucket * 100:.0f} %: {hist[bucket]} files\n")
