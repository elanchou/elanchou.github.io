---
title: "Exploring the AHR999 Indicator: A Personal Journey in Bitcoin Market Timing"
date: 2024-03-20
description: "Join me as I delve into the AHR999 indicator, its calculation, and how it can be applied to Bitcoin trading."
tags: ["Bitcoin", "Trading", "Technical Analysis", "Cryptocurrency"]
categories: ["Investment"]
showToc: true
---

## Introduction

Hey there, fellow crypto enthusiasts! Today, I want to share my journey exploring the AHR999 indicator, a fascinating tool for timing the Bitcoin market. Created by the insightful Chinese analyst "ahr999", this indicator has piqued my interest due to its unique approach to identifying market tops and bottoms.

## Understanding the AHR999 Indicator

The AHR999 indicator is a market timing tool specifically designed for Bitcoin. It combines Bitcoin's price and moving averages to help investors identify potential market bottoms and tops, making it particularly useful for long-term investment decisions.

## The Mathematics Behind AHR999

Here's the formula that powers the AHR999 indicator:

```
AHR999 = (Bitcoin Price) / (200-day Moving Average × 200-day Moving Average × 200-day Moving Average)^(1/3)
```

This formula creates a normalized value that typically ranges between 0.45 and 7:

- Values below 0.45: Extremely undervalued, strong buy signal
- Values around 0.45-1.2: Undervalued, good accumulation zone
- Values between 1.2-5: Fair value range
- Values above 5: Overvalued, consider taking profits
- Values above 7: Extremely overvalued, strong sell signal

## My Experience with AHR999

In my own trading adventures, I've found the AHR999 indicator to be a reliable companion. It has helped me navigate the volatile waters of Bitcoin trading by providing clear signals on when to buy, hold, or sell.

## TradingView Pine Script

For those of you who love visualizing data, here's a Pine Script for TradingView that brings the AHR999 indicator to life:

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © elanchou

//@version=5
indicator('Hodl Bitcoin: AHR999 Investment Index', shorttitle='AHR999 Index', overlay=false)

//ahr999 = (Bitcoin Price/200-day Investment Cost) * (Bitcoin Price/Exponential Growth Valuation)
//• Exponential Growth Valuation = 10^[5.84 * log(Coin Age) - 17.01]
//• Coin Age = Number of days since January 3, 2009

birth_day = '2009-01-03'
// Coin Age
coin_age = (math.round(time_close / 1000) - 1230912000) / (60 * 60 * 24)
// Exponential Growth Valuation
coin_price = math.pow(10, 5.84 * math.log10(coin_age) - 17.01)

//200-day Investment Cost, using geometric mean
price = input(title='Source', defval=close)
per = input(title='Length', defval=200)
lmean = math.log(price)
smean = math.sum(lmean, per)
gma = math.exp(smean / per)

// Index
index = close / coin_price * (close / gma)
plot(index, title = "AHR999 Index", color = index > 1 ? color.lime : index > 0.45 ? color.orange : color.red)

// Investment Range Plotting
h0 = hline(0, title='', linewidth=0)
h1 = hline(0.45, title='Bottom Fishing Range', linewidth=2)
h2 = hline(1.2, title='Investment Range', linewidth=2)
fill(h1, h2, color=color.new(color.green, 90))
fill(h0, h1,color=color.new(color.red, 90))

dt = time - time[1]
if barstate.islast
    label1 = label.new(time + 400 * dt, 1.20, text='Investment Benchmark: 1.2', xloc=xloc.bar_time)
    label2 = label.new(time + 400 * dt, 0.45, text='All-in Benchmark: 0.45', xloc=xloc.bar_time)
    label4 = label.new(time + 200 * dt, 0.7, text='Investment Range', xloc=xloc.bar_time)
    label5 = label.new(time + 200 * dt, 3.0, text='Hodl Range', xloc=xloc.bar_time)
    label6 = label.new(time + 200 * dt, 0.05, text='All-in Range', xloc=xloc.bar_time)

    label.set_style(label1, label.style_label_down)
    label.set_style(label2, label.style_label_down)
    label.set_style(label4, label.style_none)
    label.set_textcolor(label4, color.red)
    label.set_style(label5, label.style_none)
    label.set_textcolor(label5, color.red)
    label.set_style(label6, label.style_none)
    label.set_textcolor(label6, color.red)

    label.set_color(label1, color.black)
    label.set_textcolor(label1, color.lime)

    label.set_color(label2, color.black)
    label.set_textcolor(label2, color.lime)


    if 0.45 < index and index <= 1.2
        label3 = label.new(time, index + 0.05, text='Current Index: ' + str.tostring(index) + '\n Fixed Investment', xloc=xloc.bar_time)
        label.set_color(label3, color.green)
        label.set_textcolor(label3, color.white)

    if index <= 0.45
        label3 = label.new(time, index + 0.05, text='Current Index: ' + str.tostring(index) + '\n All IN', xloc=xloc.bar_time)
        label.set_color(label3, color.red)
        label.set_textcolor(label3, color.white)

    if index > 1.2
        label3 = label.new(time, index + 0.05, text='Current Index: ' + str.tostring(index) + '\n HOLD OR SALE', xloc=xloc.bar_time)
        label.set_color(label3, color.blue)
        label.set_textcolor(label3, color.white)

// Add Range Plotting
    if index < 0.45
        index
```