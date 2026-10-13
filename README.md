# Halcyon Ridge — luxury builder landing page

A single-file, scroll-driven 3D site (`index.html`) built with Three.js r160 and GSAP 3.12 + ScrollTrigger, both loaded from CDNs. No build step and no external assets: terrain, materials, sky and sea are generated in the page.

Open `index.html` in a browser, or serve the folder (`npx serve .`).

## How it works
- **Hero (640vh, pinned):** a scrubbed GSAP timeline builds the house in five phases (survey, foundation, structure, envelope, finish & landscape). A tower crane works the site, the camera orbits, and the light moves from morning to golden hour. The construction log tracks progress.
- **Five chapters** (Materials, Craft, Engineering, Experience, Commission): each one triggers at a fixed scroll position. It moves the camera to its own frame, shifts the time of day (dusk, then night with the interior lit), and reveals its content panel.

## Performance
- The shadow map re-renders only when something in the scene moves (`shadowMap.autoUpdate = false`).
- Repeated parts (mullions, louvres, columns, light strips, trees) are instanced.
- The reflection environment is re-baked from the sky only when the time of day changes noticeably.
- Pixel ratio is capped at 1.75 (1.5 on phones) and steps down automatically if frames take longer than 20 ms.
- The render loop runs on `gsap.ticker`, so it shares a frame with scroll tweens. It honours `prefers-reduced-motion`.
