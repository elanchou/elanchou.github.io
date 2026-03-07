---
title: "The AHR999 Indicator: A Dead-Simple Way to Stop Panic-Buying Bitcoin"
date: 2024-03-20
description: "A single number that tells you whether to go all-in, dollar-cost average, or touch grass and wait."
tags: ["Bitcoin", "Trading", "Technical Analysis", "Cryptocurrency"]
categories: ["Investment"]
showToc: true
---

## I Used to Be That Guy

You know the type. Sees Bitcoin dump 20% — buys. Sees it pump 40% — buys more. Checks the price every 11 minutes while pretending to work. Ends up down 60% wondering what went wrong.

That was me. Then I found the AHR999 indicator, and at least now my bad decisions are *informed* bad decisions.

---

## So What Is It?

AHR999 is a Bitcoin market timing indicator created by a Chinese analyst who goes by — you guessed it — "ahr999." The concept is simple: it tells you whether Bitcoin is cheap, fair, or expensive relative to two baselines:

1. **200-day geometric moving average** (what you'd have paid if you'd been dollar-cost averaging for the past 200 days)
2. **Exponential growth model** (where Bitcoin "should" be based on how old it is)

Divide price by both, multiply them together, and you get a single number.

---

## The Formula

```
AHR999 = (Price / 200-day MA) × (Price / Exponential Growth Valuation)
```

Where:
```
Exponential Growth Valuation = 10^[5.84 × log(coin_age_in_days) - 17.01]
```

`coin_age` is measured from Bitcoin's genesis block: January 3, 2009.

The resulting index typically falls between 0.45 and 7. Here's the cheat sheet:

| Value | Meaning | Action |
|-------|---------|--------|
| < 0.45 | Screaming deal | Go all in (or close to it) |
| 0.45 – 1.2 | Reasonable | Regular DCA |
| 1.2 – 5 | Fair to rich | Hold and watch |
| > 5 | Expensive | Consider taking profits |
| > 7 | Bubble territory | Pray |

---

## TradingView Pine Script

If you want this on your charts, here's the full script:

```pinescript
// © elanchou
//@version=5
indicator('Hodl Bitcoin: AHR999 Investment Index', shorttitle='AHR999 Index', overlay=false)

birth_day = '2009-01-03'
coin_age = (math.round(time_close / 1000) - 1230912000) / (60 * 60 * 24)
coin_price = math.pow(10, 5.84 * math.log10(coin_age) - 17.01)

price = input(title='Source', defval=close)
per = input(title='Length', defval=200)
lmean = math.log(price)
smean = math.sum(lmean, per)
gma = math.exp(smean / per)

index = close / coin_price * (close / gma)
plot(index, title = "AHR999 Index", color = index > 1 ? color.lime : index > 0.45 ? color.orange : color.red)

h0 = hline(0, title='', linewidth=0)
h1 = hline(0.45, title='Bottom Fishing Range', linewidth=2)
h2 = hline(1.2, title='Investment Range', linewidth=2)
fill(h1, h2, color=color.new(color.green, 90))
fill(h0, h1,color=color.new(color.red, 90))

dt = time - time[1]
if barstate.islast
    label1 = label.new(time + 400 * dt, 1.20, text='DCA Benchmark: 1.2', xloc=xloc.bar_time)
    label2 = label.new(time + 400 * dt, 0.45, text='All-in Benchmark: 0.45', xloc=xloc.bar_time)

    label.set_style(label1, label.style_label_down)
    label.set_style(label2, label.style_label_down)
    label.set_color(label1, color.black)
    label.set_textcolor(label1, color.lime)
    label.set_color(label2, color.black)
    label.set_textcolor(label2, color.lime)

    if 0.45 < index and index <= 1.2
        label3 = label.new(time, index + 0.05, text='Index: ' + str.tostring(index) + '\nDCA Zone', xloc=xloc.bar_time)
        label.set_color(label3, color.green)
        label.set_textcolor(label3, color.white)

    if index <= 0.45
        label3 = label.new(time, index + 0.05, text='Index: ' + str.tostring(index) + '\nALL IN', xloc=xloc.bar_time)
        label.set_color(label3, color.red)
        label.set_textcolor(label3, color.white)

    if index > 1.2
        label3 = label.new(time, index + 0.05, text='Index: ' + str.tostring(index) + '\nHOLD / TRIM', xloc=xloc.bar_time)
        label.set_color(label3, color.blue)
        label.set_textcolor(label3, color.white)
```

Paste that into TradingView on the BTC/USD chart. Green zone = buy more. Red zone = stop buying. Blue = sit on your hands and feel smug.

---

## Does It Actually Work?

Historically? Pretty well. It's not magic — no indicator is — but it does a good job of keeping you from buying at obvious peaks and nudging you toward obvious bottoms.

The real value isn't the formula. It's the *discipline*. Having a number removes the emotional guesswork. Instead of "vibes say buy," you get "index says 0.38, so I'm buying." Huge difference.

---

## The Honest Caveat

This is not financial advice. I'm a developer who got into crypto and built a TradingView script. AHR999 is one lens among many. Past performance, future results, you know the drill.

But if you're the kind of person who panic-buys and panic-sells, having *any* systematic framework is better than none. Start here.
