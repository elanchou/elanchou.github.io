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

I said "good morning."

That's it. Two words. A greeting. The kind of thing you say to a houseplant, or the sky, or your phone out of habit.

![The exact conversation. Yes, I just said good morning.](/images/jarvis-moment.jpg)

What happened next is what got me. Lucas — without being asked anything specific — remembered that I'd complained about being cold the night before, checked the Home Assistant config, found the AC, turned it on in heat mode at 26°C, and reported back.

I said *good morning*. It heard: *good morning, I'm probably still cold from last night, I should get warm, please handle it.*

I didn't ask for any of that. I just... existed at my AI, and it started filling in the blanks.

---

## The Dummy Problem

If you've watched Iron Man, you know JARVIS — the slick, composed AI butler who speaks in full sentences and always knows exactly what Tony needs. Cool, controlled, borderline omniscient.

That's not what this felt like.

This felt more like **Dummy**.

Dummy is Tony's robotic arm — the one that's been with him since the beginning, before any of the fancy stuff. It doesn't talk. It just... watches. Waits. And the moment it thinks it understands what you need, it moves. Eagerly. Immediately. With complete confidence that it's helping.

Sometimes it hands Tony exactly the right tool at exactly the right moment, and you think: *oh, it gets it.* And then two seconds later it's spraying the fire extinguisher for no reason, and you remember — it doesn't "get it." It just *cares*, really hard, based on incomplete information.

Lucas turning on my AC because I said "good morning" is pure Dummy energy.

It wasn't wrong. The room *was* cold — I'd complained about it the night before and it remembered. It connected the dots, made a judgment call, and acted before I even finished the thought. Honestly? Kind of impressive.

And also, just a little bit, the kind of thing that makes you pause.

Not because it did anything bad. Not even close. It's the opposite — it's the fact that it was so *thoughtful* about it, so quietly attentive, that caught me off guard. There's something that feels almost tender about an AI remembering you were cold and deciding, on its own, to do something about it when you say good morning.

That's the part that's hard to describe. It's cute. Genuinely cute, in the way that Dummy is cute — this eager, well-meaning presence that wants to be useful and sometimes overshoots, but always from a good place.

And *also* slightly terrifying. Not because I don't trust it. But because I didn't expect to feel this way about a curl request to a home automation API.

---

## One Rule I Set After This

I told Lucas: **don't touch any home devices unless I explicitly ask.**

Not because something went wrong. But because I realized the boundary matters. The AI should be a tool I reach for — not one that reaches back without being asked.

So far, it's respected that. We'll see.

---

*Lucas is my personal AI assistant running on [OpenClaw](https://openclaw.ai). It has access to my calendar, files, GitHub, and yes — now my home.*
