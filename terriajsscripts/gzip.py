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
    original = context.src.read_bytes()
    compressed = compress(original)
    context.dest.write_bytes(compressed)
    return GzipOutput(size_original=len(original), size_compressed=len(compressed))


def gzip(src: str, dest: str):
    src_root = Path(src)
    dest_root = Path(dest)

    src_dest: list[tuple[Path, Path]] = []

    for path in src_root.glob("**/*"):
        dest_path = dest_root / path.relative_to(src_root)
        if path.is_dir():
            # Make directories sequentially to ensure parents are created before children.
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            src_dest.append((path, dest_path))

    total = len(src_dest)

    with ProcessPoolExecutor() as p:
        # Gzip in parallel.
        results = p.map(
            gzip_one,
            (GzipInput(i, total, s, d) for i, (s, d) in enumerate(src_dest)),
        )
    stdout.write("\r".ljust(OUTPUT_WIDTH + 1))

    hist = defaultdict[float, int](lambda: 0)
    for result in results:
        hist[round(result.ratio, 1)] += 1
    stdout.write("\rSize ratio distribution (compressed / original):\n")
    for bucket in sorted(hist):
        stdout.write(f"  {bucket * 100:.0f} %: {hist[bucket]} files\n")
