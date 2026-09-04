# Setup

1. Copy everything in this folder into your profile repository:
   `Programmer-MukeshKrishnaaNK/Programmer-MukeshKrishnaaNK`
2. Commit and push.
3. Open **Actions → Update animated profile SVGs → Run workflow** once.
4. After that, the workflow updates the stats and contribution SVGs daily.

## Why SVG instead of GIF?

This version intentionally uses self-contained SVGs with native SMIL animation (`<animate>`, `<animateTransform>`). The reference you supplied uses the same approach: its SVG contains animated clip-path widths and an animated cursor, rather than a GIF. The font is embedded directly into each SVG so the display font does not depend on a web-font request.

The README only embeds the SVG files with `<img>`. There is no JavaScript and no GIF conversion.
