// news-image-20261123 — entrypoint.
// The picture itself is drawn by build_image.py (Pillow) and committed as
// entry.png next to this file. At run time we only have to deliver that PNG
// to the directory make.fun points us at, byte for byte — and prove it.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);

// Verify what landed: a truncated or swapped file must fail loudly here
// rather than surface later as a broken entry image.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const expected = readFileSync(source);
const delivered = readFileSync(target);
if (delivered.length !== expected.length) {
  throw new Error(
    `entry.png copy mismatch: wrote ${delivered.length} bytes, source has ${expected.length}`,
  );
}
for (let i = 0; i < PNG_SIGNATURE.length; i++) {
  if (delivered[i] !== PNG_SIGNATURE[i]) {
    throw new Error(`entry.png copy is not a PNG (bad signature byte ${i})`);
  }
}
console.log(`news-image-20261123: entry.png delivered to ${target} (${delivered.length} bytes, verified)`);
