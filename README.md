# Campaign Arena

A visual, browser-based marketing simulation for MRK 2123, based on the supplied Week 9 (website marketing), Week 10 (website design), and Week 11 (social media marketing) decks. Email composition, CRM segmentation, and campaign scheduling extend those concepts into practical exercises.

## Play

Open **dist/campaign-arena.html** in a modern desktop browser. It contains the entire game, including its photorealistic campaign imagery, and works without an internet connection or installation. Use a desktop or tablet for the most comfortable creative workspace; mobile layouts are also supported.

For development, from `/workspace/Takeshi-Test-` run:

```sh
npm start
```

This starts the dependency-free Python server on port 3000. Python 3.10+ is sufficient; Node 18+ is only needed for JavaScript checks and tests. Change the server port with `PORT=3001 npm start` if required. No package installation, API keys, database, paid service, or live marketing account is needed.

## Student workflow

1. Choose solo or a two-person team using the top-right player control. Pair mode is collaboration on one device, not network multiplayer.
2. Investigate CRM profiles, select a target audience, set an eight-week objective, and justify the strategy.
3. Repair the landing page using imagery, responsive layout, clear copy, an appropriate CTA, SEO intent, and verifiable proof.
4. Build discovery and follow-up emails. Select artwork, colours, typography, copy direction and send-time evidence; optionally write original subject lines and headings.
5. Build a discovery Instagram creative and an action Story, including captions, hashtags, and a response to a customer concern.
6. Schedule at least twelve touchpoints across eight weeks inside AED 2,400. Drag calendar cards between weeks or use the accessible week selector. Handle the Week 4 transport disruption.
7. Watch the animated campaign journey, analyse simulated conversion results and an A/B test, then give the board an evidence-backed recommendation.
8. Save all six missions and complete at least 40 active minutes before final submission. A score of 80% passes. A lower score requires restarting from Mission 1; export the diagnostic first.

Progress automatically saves in this browser. The timer counts only in mission views while the tab is visible and the user has interacted in the previous 60 seconds. Idle time does not count. The suggested lesson takes about 50 minutes; there is no maximum time. A restart clears the entire campaign and timer and increments the attempt number.

## Assessment and limitations

The visible field guide explains the theory and rules. The automated rubric allocates 15 points to audience/objective, 20 to website/journey, 20 to email, 15 to social, 20 to campaign coherence, and 10 to analysis/revision. Each earned or missed criterion appears in the final diagnostic.

Multiple audiences and visual treatments can succeed. Colour, typography, and image tastes are not assigned arbitrary right/wrong scores. Structured strategic choices are automatically assessed. Written justifications and custom wording are exported for instructor review; this game does not claim to understand or grade the meaning of free text. The export includes all work, the active time, the attempt, and criterion-level feedback.

All customer data, performance metrics, and A/B results are fictional teaching materials. Simulated campaign outcomes respond deterministically to strategic alignment; they are not real-world forecasts. No emails, posts, advertisements, or bookings are sent or published. Students make real choices in an educational simulation, not in a live CRM.

This is a local classroom game, not an examination platform. Browser storage and the timer can be modified using developer tools. There is no authentication, server-side anti-tamper enforcement, cross-device sync, or instructor dashboard. Clearing browser storage removes progress. Each failed attempt starts blank with the same teaching scenario; it is not randomised.

## Validation and build

```sh
npm run check
npm test
npm run build
```

Tests cover coherent strategies for all three audiences, the 40-minute submission guard, completion requirements, calendar coverage and budget, timing evidence, A/B interpretation, weak-strategy failure, simulation arithmetic, and restart state.

`build.py` embeds the local artwork, CSS, and JavaScript into the portable HTML. Rebuild after source changes. No external fonts, CDNs, or network requests are required by the game.

In the managed cloud workspace, use the existing checkout. Each task is already isolated; do not create another worktree unless explicitly requested. Live server processes must be restarted after restoring an environment.

## Campaign photography

The six PNG campaign assets are photorealistic AI-generated images created for this fictional client: a camel caravan, family camp visit, young adult sandboarding group, private desert dining, camp at dusk, and a couple watching sunset. They replace the earlier stylised SVG scenes. They are not documentary photographs of an actual tour operator and should not be used as evidence that a real business offers the depicted facilities or inclusions. Students should still match each image to a truthful package promise.
