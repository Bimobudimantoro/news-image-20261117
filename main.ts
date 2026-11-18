import { copyFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
copyFileSync(new URL('./entry.png', import.meta.url), join(outputDir, 'entry.png'));