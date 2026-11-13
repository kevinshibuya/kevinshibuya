// Usage: node capture.mjs stills | loop
import { chromium } from 'playwright-core'
import { mkdirSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { homedir } from 'node:os'

const here = dirname(fileURLToPath(import.meta.url))
const mode = process.argv[2] ?? 'stills'
const exe = join(homedir(), 'Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell')
const DARK = [0x0d / 255, 0x11 / 255, 0x17 / 255]
const TUNE = JSON.parse(process.env.TUNE ?? '{}')

const browser = await chromium.launch({
  executablePath: exe,
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
})
const page = await browser.newPage({ viewport: { width: 1280, height: 440 }, deviceScaleFactor: 1 })
page.on('console', m => console.log('[page]', m.text()))
page.on('pageerror', e => console.log('[pageerror]', e.message))
await page.goto('file://' + join(here, 'render.html'))
await page.evaluate(() => document.fonts.ready)
const stage = page.locator('#stage')

if (mode === 'stills') {
  mkdirSync(join(here, 'stills'), { recursive: true })
  const seeds = (process.argv[3] ?? '0.37,0.11,0.62,0.83').split(',').map(Number)
  const t0s = (process.argv[4] ?? '12').split(',').map(Number)
  for (const seed of seeds) for (const t0 of t0s) {
    await page.evaluate(c => { setup(c); frame(999) }, { w: 1280, h: 440, seed, t0, fps: 12, frames: 96, xfade: 0, dissolveStart: 0, page: DARK, ...TUNE })
    await stage.screenshot({ path: join(here, 'stills', `s${seed}-t${t0}.png`) })
  }
} else {
  const seed = Number(process.argv[3]), t0 = Number(process.argv[4])
  // H: paint-only frames at half size for the hybrid SVG
  const H = { w: 832, h: 286, seed, t0, fps: 6, frames: 48, xfade: 12, dissolveStart: 0, page: DARK, ...TUNE }
  await page.evaluate(c => { document.body.classList.add('notext'); setup(c) }, H)
  const jpegs = []
  for (let i = 0; i < H.frames; i++) jpegs.push(await page.evaluate(i => { frame(i); return document.getElementById('out').toDataURL('image/webp', 0.8) }, i))
  writeFileSync(join(here, 'frames.json'), JSON.stringify({ ...H, jpegs }))
  if (process.env.SKIP_B) { await browser.close(); process.exit(0) }
  // B: full-size frames with the type baked in
  const B = { w: 1280, h: 440, seed, t0, fps: 12, frames: 96, xfade: 24, dissolveStart: 0, page: DARK, ...TUNE }
  mkdirSync(join(here, 'b-frames'), { recursive: true })
  await page.evaluate(c => { document.body.classList.remove('notext'); setup(c) }, B)
  for (let i = 0; i < B.frames; i++) {
    await page.evaluate(i => frame(i), i)
    await stage.screenshot({ path: join(here, 'b-frames', `f${String(i).padStart(3, '0')}.png`) })
  }
}
await browser.close()
console.log('done', mode)
