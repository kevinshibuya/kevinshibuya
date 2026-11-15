# Hero

`assets/readme/hero.svg` is one animated SVG. The paint is the FluidWaves fragment shader from my portfolio, rendered to 48 frames and cross-faded in CSS. The type is live text in an embedded subset of Plus Jakarta Sans.

Since version 4 of the portfolio the frames are stills of the site's own hero, not of a copy of the shader kept here: 60 frozen frames of the built site (`?perf-seed=0.37&perf-freeze=<t>`, from 12 s, 6 a second, 832×286, the type and the band under the first screen taken out, so the paint is at full strength, without the cap the site holds under its own type), the first 12 blended out of the last 12 so the loop closes. They are written to `frames.json` in the shape `gen-svg.py` reads:

```sh
python3 gen-svg.py frames.json ../../assets/fonts/PlusJakartaSans-subset.woff2 ../../assets/readme/hero.svg
```

`capture.mjs` and `render.html` are the earlier pipeline, with the shader and palette of the site before version 4. They no longer match the site and are kept for reference.
