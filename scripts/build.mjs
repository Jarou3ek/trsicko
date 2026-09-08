import { cp, mkdir, readFile, readdir, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = path.join(root, 'public');
const output = path.join(root, 'dist');
const files = await readdir(source, { recursive: true });
let checked = 0;
for (const file of files.filter(f => f.endsWith('.html'))) {
  const html = await readFile(path.join(source, file), 'utf8');
  if (!html.includes('lang="cs"') || !html.includes('name="viewport"')) throw new Error(`Missing document metadata: ${file}`);
  if ((html.match(/<h1\b/g) || []).length !== 1) throw new Error(`Expected one h1: ${file}`);
  for (const [, link] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    if (/^(https?:|mailto:|tel:|data:)/.test(link)) continue;
    const [pathname, fragment] = link.split('#');
    const target = path.resolve(source, path.dirname(file), decodeURIComponent(pathname || path.basename(file)));
    if (!target.startsWith(source + path.sep)) throw new Error(`Link outside public: ${link}`);
    const info = await stat(target).catch(() => { throw new Error(`Broken link in ${file}: ${link}`); });
    if (!info.isFile()) throw new Error(`Not a file: ${link}`);
    if (fragment && target.endsWith('.html')) {
      const text = await readFile(target, 'utf8');
      if (!text.includes(`id="${fragment}"`)) throw new Error(`Missing anchor: ${link}`);
    }
    checked++;
  }
}
await mkdir(output, { recursive: true });
await cp(source, output, { recursive: true });
console.log(`Build OK: ${files.length} entries, ${checked} local links checked. Output: dist`);
