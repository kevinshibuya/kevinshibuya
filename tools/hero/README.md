# Hero

`assets/readme/hero.svg` is one animated SVG. The paint is the FluidWaves fragment shader from my portfolio, rendered to 48 frames and cross-faded in CSS. The type is live text in an embedded subset of Plus Jakarta Sans.

To regenerate it:

```sh
npm i playwright-core
node capture.mjs loop 0.37 12          # writes frames.json, about 1 MB
python3 gen-svg.py frames.json ../../assets/fonts/PlusJakartaSans-subset.woff2 ../../assets/readme/hero.svg
```

`capture.mjs` expects Playwright's headless Chromium in the default cache folder. Set `SKIP_B=1` to skip the full-size frames it can also write.
