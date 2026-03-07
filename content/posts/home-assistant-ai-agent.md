---
title: "I Let My AI Control My Home — And It's Kind of Terrifying"
date: 2026-03-07
description: "A practical guide to integrating Home Assistant with an AI agent, and why the result scared me a little."
tags: ["Home Assistant", "AI", "Smart Home", "OpenClaw", "Automation"]
categories: ["Tech"]
showToc: true
cover:
  image: ""
  alt: "Smart home AI control"
---

## The Setup

I've been running [Home Assistant](https://www.home-assistant.io/) at home for a while — smart lights, switches, air conditioner, the whole deal. Nothing too crazy. The usual story: you set up a few automations, feel like a genius, then forget they exist.

But recently I gave my AI assistant (Lucas, built on OpenClaw + Claude) direct access to the Home Assistant API. The idea was simple: instead of opening an app, I just tell it what I want.

Here's how to set it up yourself.

---

## Prerequisites

- A running Home Assistant instance (local network or cloud)
- An AI assistant with tool access (OpenClaw, or any agent that can make HTTP calls)
- 5 minutes

---

## Step 1: Generate a Long-Lived Access Token

1. Open Home Assistant → click your profile (bottom left)
2. Scroll to **Long-Lived Access Tokens**
3. Click **Create Token**, give it a name like `AI Assistant`
4. Copy the token — **you won't see it again**

---

## Step 2: Find Your Entity IDs

Every device in Home Assistant has an entity ID like `climate.living_room_ac` or `switch.bedroom_lamp`.

To list all climate entities:

```bash
curl -s http://YOUR_HA_IP:8123/api/states \
  -H "Authorization: Bearer YOUR_TOKEN" | \
  python3 -c "
import json, sys
for s in json.load(sys.stdin):
    if s['entity_id'].startswith('climate.'):
        print(s['entity_id'], s['state'])
"
```

---

## Step 3: Give Your AI the API Details

In your AI agent config (e.g. `TOOLS.md` for OpenClaw):

```
### Home Assistant
- URL: http://192.168.x.x:8123
- Token: YOUR_LONG_LIVED_TOKEN
```

That's it. Your AI can now call the HA REST API directly.

---

## Step 4: Test It

Try something simple:

> "Turn on the air conditioner in heat mode at 26°C"

The AI translates that to:

```bash
# Turn on
curl -X POST http://HA_IP:8123/api/services/climate/turn_on \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.your_ac"}'

# Set heat mode
curl -X POST http://HA_IP:8123/api/services/climate/set_hvac_mode \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.your_ac", "hvac_mode": "heat"}'

# Set temperature
curl -X POST http://HA_IP:8123/api/services/climate/set_temperature \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.your_ac", "temperature": 26}'
```

All of this happens in seconds, triggered by a single natural language message.

---

## What Actually Happened

This morning I messaged Lucas:

![The exact conversation that made me feel like Tony Stark](/images/jarvis-moment.jpg)

*Yes, this is the actual chat log. Yes, I was complaining about being cold. Yes, the AI just... handled it.*

If you've seen Iron Man, you know the scene — Tony mumbles something half-asleep, and JARVIS has already adjusted the temperature, dimmed the lights, and queued up AC/DC. I used to think that was movie magic. Turns out it's just a REST API and a language model with tool access.

The difference between JARVIS and what I have running? About 70 years of fictional technology and a slightly worse voice.

> "I'm in the master bedroom, it's freezing"

Without me asking it to do anything specific, it pulled the Home Assistant config, found the AC entity, turned it on in heat mode at 26°C, and told me it was done.

I didn't say "turn on the AC." I just complained about being cold.

Then I said "actually, turn it off" — and it did, immediately.

The whole thing took maybe 10 seconds.

---

## The Terrifying Part

Here's what got me.

There's something deeply unsettling about realizing your home now *listens and responds* — not to scheduled automations, not to button taps, but to *intent*. I didn't configure a rule. I didn't build a flow. I just expressed a feeling, and the house reacted.

It's the difference between a smart home and a home that understands you.

The practical implications are obvious — convenience, accessibility, speed. But the feeling it left me with was something closer to unease. Not because I don't trust the system. But because it worked *too well*, too naturally, too fast.

A few weeks ago I would've said "smart home + AI = overhyped." Now I'm sitting here wondering what other parts of my life I've been manually operating that don't need to be.

That's either progress or a slippery slope. Probably both.

---

## One Rule I Set After This

I told Lucas: **don't touch any home devices unless I explicitly ask.**

Not because something went wrong. But because I realized the boundary matters. The AI should be a tool I reach for — not one that reaches back without being asked.

So far, it's respected that. We'll see.

---

*Lucas is my personal AI assistant running on [OpenClaw](https://openclaw.ai). It has access to my calendar, files, GitHub, and yes — now my home.*
