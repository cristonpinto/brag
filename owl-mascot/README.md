# Owl mascot

A vector owl that sits in the corner of a page, idles (drifting gaze, blinking), follows the pointer,
and reacts: it winks, hops, celebrates, falls asleep, shows a notification badge, and answers a Like.
Built for a Moodle LMS, usable on any web page. One file, no dependencies.

- Drawing: traced from your reference owl (`tools/owl-reference.webp`). Average pixel difference from
  the reference is about 3/255; render both side by side with `demo/compare.html`.
- Motion: the catalogue and timings of [jeremy-prt/bloub](https://github.com/jeremy-prt/bloub) (MIT), applied to the owl.
- Plain JavaScript and SVG. `dist/owl-mascot.js` is about 50 KB, no network requests.

## Try it

Open these in a browser (no server needed):

| File | What it shows |
|---|---|
| `demo/index.html` | A big owl with a button for every state, a full tour, and a Like button |
| `demo/moodle-sim.html` | A fake Moodle course page with the owl pinned bottom-right, and buttons that trigger its reactions |
| `demo/board.html` | Every state frozen mid-animation, side by side |
| `demo/compare.html` | The vector owl next to your reference image |

## The states

bloub has 14 states built around a morphing blob. An owl cannot become a hexagon, so each state keeps
bloub's **timing and role** and gets an owl-native performance. Durations are bloub's measured hold times.

| State | bloub original | What the owl does | Hold |
|---|---|---|---|
| `idle` | idle | Gaze drifts and jumps between targets, blinks every 1.9 to 4.6 s (sometimes twice), breathes 0.4% | 2.4 s |
| `thinking` | thinking | Head tilts, eyes look up-left, three dots pulse in a wave above | 2.6 s |
| `wink` | wink | Left eye closes into an arc, head tips | 1.6 s |
| `wide` | wide eyes | Eyes and highlights widen, ear tufts lift, small rise | 1.8 s |
| `alert` | alert | Back-hop, ears up, a thin "!" pops in and wobbles, gaze snaps then relaxes | 2.4 s |
| `notify` | notification | Red badge with a count pops in (with a 14% spring), owl turns to look at it | 2.2 s |
| `exclaim` | exclamation | Leans away, a large slanted "!" shakes in | 2.0 s |
| `sleep` | sleep | Eyes become arcs, head droops, slow breathing, "z" glyphs float up | 2.4 s |
| `hop` | egg | Crouch, jump, land: squash and stretch with happy eyes | 1.8 s |
| `shake` | hexagon | Head shake "no": quick side to side, eyes squint, ears flatten | 1.6 s |
| `play` | play | Bobs to a beat, a play button pops beside it | 2.0 s |
| `orbit` | orbit | Three stars circle the head (front and back), eyes trace a small circle | 3.4 s |
| `swirl` | swirl | A quick look-around, used as a transition | 1.3 s |
| `burst` | burst | Confetti bursts outward past the frame, owl hops with happy eyes | 2.6 s |
| `comet` | comet | A comet trail runs around the frame while the eyes follow it (a loading look) | 2.4 s |
| `like` | (new) | Hop, happy eyes, three hearts float up | 1.8 s |

Behaviours carried over from bloub: transitions are exponential ease-outs and the body never overshoots;
most entries are hidden by a quick forced blink (0.2 s); a state change landing inside a fade blends from the
frame that was on screen, so nothing jumps; at rest the life is only gaze drift and blinking; the engine is a
pure function of time, so a frozen frame always renders identically.

Not literally reproduced: the shape-morphing (egg, hexagon, triangle, swirl body) because it makes no sense
on an owl, and bloub's studio, timeline editor and GIF/MP4 export, which are separate apps.

## Use it

```html
<script src="owl-mascot.js"></script>
<script>
  const owl = OwlMascot.mount({ corner: 'bottom-right', size: 112 });   // pinned to the page

  owl.react('wink');        // play once, then back to idle
  owl.state('thinking');    // hold until changed
  owl.like();               // heart pops, counter goes up
  owl.setBadge(3);          // number shown by the next 'notify'
  owl.say('Quiz saved');    // small speech bubble
  owl.tour();               // play the whole catalogue
  owl.destroy();
</script>
```

Inside any container instead of the corner: `OwlMascot.create(el, { size: 240 })`.
One frozen frame (thumbnails, tests): `OwlMascot.frame(el, 'orbit', 1.5, { size: 200 })`.

`mount()` options: `corner` (`bottom-right`, `bottom-left`, `top-right`, `top-left`), `offset` `[x, y]` px,
`size` px, `shape` (`rounded`, `circle`, `square`), `like` (show the heart button), `onLike(count)`,
`follow` (eyes follow the pointer), `autoSleep` (seconds before dozing off; 0 = never), `label` (accessible name),
`moodle` (`'auto'`, `true`, `false`).

Interactions: hover widens its eyes, click plays a rotating reaction (wink, hop, like, play, look-around),
double-click celebrates, the heart that appears on hover is Like. It falls asleep after 90 s of nothing
and wakes when the pointer comes near.

## Install on Moodle

Two ways. Both put the owl on every page for logged-in users.

**A. Plugin (Moodle 4.4 or newer).** Upload `dist/local_owlmascot.zip` at
*Site administration > Plugins > Install plugins*, then configure it at
*Site administration > Plugins > Local plugins > Owl mascot* (corner, size, shape, Like button, hide during
quiz attempts). It uses the 4.4 hooks API. Rebuild the zip with `tools/package-moodle.sh`.

**B. No plugin, any Moodle.** Copy `dist/owl-mascot.js` somewhere your site serves files from, then paste this at
*Site administration > Appearance > Additional HTML > Before BODY end*:

```html
<script src="/path/to/owl-mascot.js"></script>
<script>OwlMascot.mount({ corner: 'bottom-right', size: 112 });</script>
```

### What it reacts to in Moodle

It reads the page; it does not call Moodle APIs. A theme that renames a class only loses that one reaction.

| Page event | Owl |
|---|---|
| First page of the session | winks once |
| Navbar notification count goes up | `notify` with the new count, plus a speech bubble |
| `.alert-success` / toast appears | `hop` |
| `.alert-danger` / `.alert-error` appears | `alert` |
| `.alert-warning` appears | `exclaim` |
| Activity marked done (`[data-action="toggle-manual-completion"]`, button turns `btn-success`) | `burst` |
| Quiz review page (`#page-mod-quiz-review`) | `burst` |
| A form is submitted | `thinking` until the page changes |

Add your own: `owl.react('burst')` from any script.

### Please note

- **Not tested inside a real Moodle.** I could not run one here. The plugin code is syntax-checked (`php -l`)
  and the JavaScript is tested against `demo/moodle-sim.html`, but the Moodle class names above are from
  memory of Moodle 4.x themes and can differ on yours. Try it on a staging site first.
- **Quizzes:** the plugin hides the owl during quiz attempts by default. Keep that on: an animated character
  next to an assessed question is a distraction and can raise accessibility complaints.
- **Accessibility:** the owl is a keyboard-focusable button with an accessible name; speech bubbles use
  `aria-live="polite"`; with `prefers-reduced-motion` it stops animating (no drift, blinking or loops); a
  reaction shows one still frame of its pose instead of moving. The like counter is plain text.
- **Performance:** one small SVG, one `requestAnimationFrame` loop that pauses when the tab is hidden,
  and no timers while idle other than the sleep timer.
- **Artwork:** the owl is a trace of the reference image you supplied. Make sure you hold the rights to that
  image before publishing the mascot, and add your own licence file; none is included.

## Rebuilding

```
pip install pillow numpy opencv-python-headless
python3 tools/trace.py     # reference image -> src/shapes.generated.js
python3 tools/build.py     # -> dist/owl-mascot.js
tools/package-moodle.sh    # -> dist/local_owlmascot.zip
```

`src/owl.js` is the engine and the renderer, `src/shapes.generated.js` the traced paths.
To add a state, add an entry to `STATES` in `src/owl.js`: a `pose(s)` function of seconds-since-entry that
returns numbers (gaze, tilt, squash, eye lids, ear tufts) and named decor slots (`dot0`, `bang`, `badge`, ...).
